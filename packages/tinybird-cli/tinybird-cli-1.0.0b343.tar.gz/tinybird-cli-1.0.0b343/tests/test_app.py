import asyncio
import unittest
import uuid
from typing import Optional
from unittest.mock import patch

import pytest
import tornado.testing
from tornado.testing import AsyncTestCase
from tests.conftest import ClusterPatches, DEFAULT_CLUSTER

from tinybird.app import uri_is_interna_or_from_api
from tinybird.job import JobExecutor
from tinybird.user import Users, User, public, UserAccount
from tinybird.internal_resources import init_metrics_tables, init_internal_tables
from tinybird.ch import ch_table_schema, ch_drop_table_sync, HTTPClient, ch_drop_view
from tinybird.ch_utils.exceptions import CHException
from tinybird.default_tables import DEFAULT_METRICS_TABLES, DEFAULT_METRICS_VIEWS, DEFAULT_TABLES, DefaultTable, \
    DEFAULT_METRICS_CLUSTER_TABLES, DEFAULT_METRICS_CLUSTER_VIEWS
from tinybird.redis_client import get_redis_test_client, get_redis_config
from tinybird.syncasync import async_to_sync
from tinybird.constants import BillingPlans


class BaseTestInitTables(AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        cls.original_public_user = public.get_public_email()
        cls.original_public_database = public.get_public_database()

        cls.workspace_name = f'r_test_internal_{uuid.uuid4().hex}'
        cls.user_email = f'{cls.workspace_name}@localhost'

        cls.user_account = UserAccount.register(cls.user_email, 'pass')
        cls.workspace = User.register(cls.workspace_name, cls.user_account.id, DEFAULT_CLUSTER)

        client = HTTPClient(cls.workspace.database_server, database=None)
        client.query_sync(f"CREATE DATABASE IF NOT EXISTS `{cls.workspace.database}` ON CLUSTER tinybird", read_only=False)
        public.set_public_user(cls.user_email, cls.workspace.database)
        redis_client = get_redis_test_client()
        cls.job_executor = JobExecutor(redis_client=redis_client, redis_config=get_redis_config(), consumer=True, import_workers=1, query_workers=1)

    @classmethod
    def tearDownClass(cls) -> None:
        database = cls.workspace.database
        client = HTTPClient(cls.workspace.database_server, database=None)
        client.query_sync(f"DROP DATABASE IF EXISTS `{database}` ON CLUSTER tinybird", read_only=False)
        User._delete(cls.workspace.id)
        UserAccount._delete(cls.user_account.id)
        public.set_public_user(cls.original_public_user, cls.original_public_database)

    def setUp(self):
        super().setUp()
        public.set_public_user(self.user_email, self.workspace.database)
        self.created_tables = []
        self.created_views = []

    def tearDown(self):
        pu = self.workspace
        for view in self.created_views:
            pipe = Users.get_pipe(pu, view)
            node = pipe.pipeline.last()
            if pipe:
                ch_drop_view_sync = async_to_sync(ch_drop_view)
                ch_drop_view_sync(pu.database_server, pu.database, node.id)
                Users.drop_pipe(pu, pipe.name)
        for table in self.created_tables:
            ds = Users.get_datasource(pu, table)
            if ds:
                ch_drop_table_sync(pu.database_server, pu.database, ds.id, exists_clause=True)
                Users.drop_datasource(pu, ds.name)
        self.job_executor._clean()
        super().tearDown()

    async def _init_tables(self, tables):
        await init_internal_tables(tables, populate_views=False, job_executor=self.job_executor)
        self.created_tables += [t.name for t in tables]


class TestInitInternalTables(BaseTestInitTables):

    @tornado.testing.gen_test
    async def test_happy_case(self):
        await self._init_tables(DEFAULT_TABLES)
        pu = public.get_public_user()
        for t in DEFAULT_TABLES:
            ds = pu.get_datasource(t.name)
            self.assertEqual(ds.name, t.name)
            self.assertEqual(ds.tags['__version'], len(t.migrations))
            schema = ch_table_schema(ds.id, pu.database_server, pu.database)
            self.assertIsNotNone(schema)


class TestInitInternalTablesMigration(BaseTestInitTables):
    @tornado.testing.gen_test
    async def test_migration_happy_case(self):
        pu = public.get_public_user()
        name = 'foo_table'
        schema_at0 = 'timestamp DateTime, event String'
        engine = 'MergeTree() PARTITION BY toYear(timestamp) ORDER BY (event, timestamp)'
        t_at0 = DefaultTable(name, schema_at0, engine)
        await self._init_tables([t_at0])

        ds = Users.get_datasource(pu, t_at0.name)
        schema = ch_table_schema(ds.id, pu.database_server, pu.database)
        self.assertEqual(len(schema), 2)
        self.assertEqual(schema[0]['name'], 'timestamp')
        self.assertEqual(schema[1]['name'], 'event')

        schema_at1 = 'timestamp DateTime, event String, error Nullable(String)'
        migration = 'ADD COLUMN IF NOT EXISTS error Nullable(String) AFTER timestamp'
        t_at1 = DefaultTable(name, schema_at1, engine, [[migration]])
        await self._init_tables([t_at1])

        schema = ch_table_schema(ds.id, pu.database_server, pu.database)
        self.assertEqual(len(schema), 3)
        self.assertEqual(schema[0]['name'], 'timestamp')
        self.assertEqual(schema[1]['name'], 'error')
        self.assertTrue(schema[1]['nullable'])
        self.assertEqual(schema[2]['name'], 'event')


class TestInitInternalTablesFailure(BaseTestInitTables):
    @tornado.testing.gen_test
    async def test_migration_failure(self):
        pu = public.get_public_user()
        name = 'bar_table'
        schema_at0 = 'timestamp DateTime, event String'
        engine = 'MergeTree() PARTITION BY toYear(timestamp) ORDER BY (event, timestamp)'
        t_at0 = DefaultTable(name, schema_at0, engine)
        await self._init_tables([t_at0])

        schema_at1 = 'timestamp DateTime, event Nullable(String)'
        migration = 'MODIFY COLUMN IF EXISTS event Nullable(String)'
        t_at1 = DefaultTable(name, schema_at1, engine, [[migration]])
        # trying to make nullable a column in the table index

        with self.assertRaises(CHException) as exception:
            await self._init_tables([t_at1])
            message = str(exception)
            old_pattern = r'ALTER of key column event.*'
            new_pattern = r'Sorting key cannot contain nullable columns.*'
            self.assertTrue(old_pattern.match(message) or new_pattern.match(message))

        # table still exists and works as initial version
        ds = Users.get_datasource(pu, t_at0.name)
        self.assertEqual(ds.tags['__version'], 0)
        schema = ch_table_schema(ds.id, pu.database_server, pu.database)
        self.assertEqual(len(schema), 2)
        self.assertEqual(schema[0]['name'], 'timestamp')
        self.assertEqual(schema[1]['name'], 'event')
        self.assertFalse(schema[1]['nullable'])


class TestInitInternalTablesMigrationsV1(BaseTestInitTables):

    def _test_expectations(self, expectations):
        pu = public.get_public_user()
        for ds_name, version, n_columns, columns in expectations:
            ds = Users.get_datasource(pu, ds_name)
            self.assertEqual(ds.tags['__version'], version)
            schema = ch_table_schema(ds.id, pu.database_server, pu.database)
            self.assertEqual(len(schema), n_columns)
            for c_index, c_name, *attrs in columns:
                self.assertEqual(schema[c_index]['name'], c_name)
                for k, v in attrs:
                    self.assertEqual(schema[c_index][k], v)

    @tornado.testing.gen_test
    async def test_migration_happy_case(self):
        tables_v0 = [
            DefaultTable(
                'data_guess',
                """
                    user_id LowCardinality(String),
                    datasource_id LowCardinality(String),
                    timestamp DateTime,
                    path LowCardinality(String),
                    type LowCardinality(String),
                    num Float64,
                    str String
                """,
                fixed_name=True),]

        await self._init_tables(tables_v0)

        self._test_expectations([
            ('data_guess', 0, 7, [
                (0, 'user_id'),
                (-1, 'str'),
            ]),
        ])

        TABLES = [
            DefaultTable(
                'data_guess',
                """
                    user_id LowCardinality(String),
                    datasource_id LowCardinality(String),
                    timestamp DateTime,
                    path LowCardinality(String),
                    type LowCardinality(String),
                    num Float64,
                    str String
                """,
                "MergeTree() ORDER BY (user_id, datasource_id, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 1 DAY",
                [
                    [
                        'MODIFY COLUMN IF EXISTS num Float32',
                    ]
                ],
                fixed_name=True),]

        tables_v1 = []
        for t in TABLES:
            if t.name in [t.name for t in tables_v0]:
                migrations = []
                if t.migrations:
                    migrations.append(t.migrations[0])
                tables_v1.append(DefaultTable(t.name, t.schema, engine=t.engine, migrations=migrations))

        await self._init_tables(tables_v1)

        self._test_expectations([
            ('data_guess', 1, 7, [
                (0, 'user_id'),
                (-2, 'num', ('type', 'Float32')),
            ]),
        ])


class TestInitMetricsTables(BaseTestInitTables):
    @patch.object(HTTPClient, 'query')
    @tornado.testing.gen_test
    async def test_query_templates_for_init_metrics_tables_for_internal(self, query_mock):
        empty_data_future = asyncio.Future()
        empty_data_future.set_result((None, '{"data": []}'))
        cluster_future = asyncio.Future()
        cluster_future.set_result((None,
                                   '{"data": [{"cluster": "cluster_1", "host_address": "127.0.0.1"},{"cluster": "cluster_2", "host_address": "127.0.0.2"}]}'))

        query_mock.side_effect = [
            empty_data_future,
            cluster_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
        ]

        public_user = public.get_public_user()
        public_user.clusters = ['internal']
        public_user.save()

        with patch.object(Users, 'add_datasource') as mock_add_datasource:
            await init_metrics_tables(
                host=public.get_public_user().database_server,
                metrics_cluster='metrics',
                metrics_database_server='http://127.0.0.1',
                metrics_cluster_tables=DEFAULT_METRICS_CLUSTER_TABLES,
                metrics_cluster_views=DEFAULT_METRICS_CLUSTER_VIEWS,
                metrics_tables=DEFAULT_METRICS_TABLES,
                metrics_views=DEFAULT_METRICS_VIEWS,
                metrics_database='default',
                add_datasources=True
            )

        self.assertEqual(mock_add_datasource.call_count, len(DEFAULT_METRICS_TABLES))

        queries = [' '.join(call.args[0].split()).replace(' ', '') for call in query_mock.call_args_list]

        self.assertTrue("CREATE DATABASE IF NOT EXISTS default on cluster metrics".replace(' ', '') in queries)
        self.assertTrue(
            """
            CREATE TABLE IF NOT EXISTS default.usage_metrics_log ON CLUSTER metrics(
                `date` Date,
                `database` String,
                `host` String,
                `read_bytes` UInt64,
                `written_bytes` UInt64
            )
            ENGINE = ReplicatedSummingMergeTree('/clickhouse/tables/{layer}-{shard}/default.usage_metrics_log', '{replica}') PARTITION BY toYYYYMM(date) ORDER BY (host, database, date)
            """.replace('\n', '').replace(' ', '') in queries, queries)

        self.assertTrue(f"CREATE DATABASE IF NOT EXISTS {public_user.database} ON CLUSTER {public_user.cluster}".replace(' ', '') in queries)
        self.assertTrue(
            f"""
            CREATE TABLE IF NOT EXISTS {public_user.database}.distributed_usage_metrics_processed_log ON CLUSTER {public_user.cluster} (
                `date` Date,
                `database` String,
                `host` String,
                `read_bytes` UInt64,
                `written_bytes` UInt64
            )
            ENGINE = Distributed('metrics', 'default', 'usage_metrics_log', rand())
            """.replace('\n', '').replace(' ', '') in queries, queries)

        self.assertTrue(
            f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {public_user.database}.usage_metrics_processed_log_view ON CLUSTER {public_user.cluster}
            TO {public_user.database}.distributed_usage_metrics_processed_log AS (
                SELECT
                    event_date as date,
                    current_database as database,
                    hostName() as host,
                    sum(read_bytes) as read_bytes,
                    sum(written_bytes) as written_bytes
                FROM system.query_log
                WHERE
                    type > 1
                    AND current_database not in ('default', 'system')
                    AND startsWith(http_user_agent, 'tb')
                    AND http_user_agent NOT IN ('tb-internal-query', 'tb-ui-query')
                GROUP BY host, database, date
            )
            """.replace('\n', '').replace(' ', '') in queries, queries)


class TestInitMetricsTables1(BaseTestInitTables):
    @patch.object(HTTPClient, 'query')
    # We disable the cluster checks in this test since we expect things to be created without cluster on purpose
    @patch.object(ClusterPatches, 'ENABLED', False)
    @tornado.testing.gen_test
    async def test_query_templates_for_init_metrics_tables_for_a_host(self, query_mock):
        empty_data_future = asyncio.Future()
        empty_data_future.set_result((None, '{"data": []}'))
        cluster_future = asyncio.Future()
        cluster_future.set_result((None,
                                   '{"data": [{"cluster": "cluster_1", "host_address": "127.0.0.1"},{"cluster": "cluster_2", "host_address": "127.0.0.2"}]}'))

        query_mock.side_effect = [
            empty_data_future,
            cluster_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future,
            empty_data_future
        ]

        public_user = public.get_public_user()
        public_user.clusters = ['internal']
        public_user.save()

        with patch.object(Users, 'add_datasource') as mock_add_datasource:
            await init_metrics_tables(
                host=public.get_public_user().database_server,
                metrics_cluster='metrics',
                metrics_database_server='http://127.0.0.1',
                metrics_cluster_tables=[],
                metrics_cluster_views=[],
                metrics_tables=DEFAULT_METRICS_TABLES,
                metrics_views=DEFAULT_METRICS_VIEWS,
                metrics_database='default',
                add_datasources=False
            )

        self.assertEqual(mock_add_datasource.call_count, 0)

        queries = [' '.join(call.args[0].split()).replace(' ', '') for call in query_mock.call_args_list]

        self.assertTrue(f"CREATE DATABASE IF NOT EXISTS {public_user.database}".replace(' ', '') in queries)
        self.assertTrue(
            f"""
            CREATE TABLE IF NOT EXISTS {public_user.database}.distributed_usage_metrics_processed_log (
                `date` Date,
                `database` String,
                `host` String,
                `read_bytes` UInt64,
                `written_bytes` UInt64
            )
            ENGINE = Distributed('metrics', 'default', 'usage_metrics_log', rand())
            """.replace('\n', '').replace(' ', '') in queries, queries)

        self.assertTrue(
            f"""
                CREATE MATERIALIZED VIEW IF NOT EXISTS {public_user.database}.usage_metrics_processed_log_view
                TO {public_user.database}.distributed_usage_metrics_processed_log AS (
                    SELECT
                        event_date as date,
                        current_database as database,
                        hostName() as host,
                        sum(read_bytes) as read_bytes,
                        sum(written_bytes) as written_bytes
                    FROM system.query_log
                    WHERE
                        type > 1
                        AND current_database not in ('default', 'system')
                        AND startsWith(http_user_agent, 'tb')
                        AND http_user_agent NOT IN ('tb-internal-query', 'tb-ui-query')
                    GROUP BY host, database, date
                )
                """.replace('\n', '').replace(' ', '') in queries, queries)


class TestInitMetricsTables2(BaseTestInitTables):
    @tornado.testing.gen_test
    async def test_query_templates_metrics_tables_as_internal(self):
        await init_internal_tables(
            tables=DEFAULT_METRICS_TABLES,
            metrics_cluster='tinybird',
            metrics_database='default',
            job_executor=self.job_executor
        )
        self.created_tables += [table.name for table in DEFAULT_METRICS_TABLES]

        workspace = User.get_by_id(self.workspace.id)
        datasource = workspace.get_datasource('distributed_usage_metrics_processed_log')
        engine, _ = await datasource.table_metadata(self.workspace)
        self.assertEqual(engine.engine_full, "Distributed('tinybird', 'default', 'usage_metrics_log', rand())")


class TestInitMetricsTables3(BaseTestInitTables):
    @tornado.testing.gen_test
    async def test_query_templates_metrics_cluster_tables_as_internal(self):
        await init_internal_tables(
            tables=DEFAULT_METRICS_CLUSTER_TABLES,
            metrics_cluster='tinybird',
            metrics_database='default',
            job_executor=self.job_executor
        )
        self.created_tables += [table.name for table in DEFAULT_METRICS_CLUSTER_TABLES]

        workspace = User.get_by_id(self.workspace.id)
        datasource = workspace.get_datasource('usage_metrics_log')
        engine, _ = await datasource.table_metadata(self.workspace)
        self.assertEqual(engine.engine_full, "SummingMergeTree() PARTITION BY toYYYYMM(date) ORDER BY (host, database, date)")


@pytest.mark.parametrize("uri,expected", [
    pytest.param("/v0/datasources/mine?query=value", True, id="If uri starts with /vX..., it comes from API"),
    pytest.param("/v32432/pipes", True, id="If uri starts with any version, it comes from API"),
    pytest.param("/internal/health", True, id="If uri starts with /internal, it is internal"),
    pytest.param("/login", False, id="Any other urls are not interal/api"),
    pytest.param(None, False, id="Empty url is not interal/api"),
])
def test_uri_is_internal_or_from_api(uri: Optional[str], expected: bool):
    result = uri_is_interna_or_from_api(uri)
    assert result == expected


class TestInternal(unittest.TestCase):
    def test_internal_workspace_plan(self):
        pu = public.get_public_user()
        self.assertEqual(pu.plan, BillingPlans.CUSTOM)
