import json
import re
import pytest

from tinybird.ndjson import JSONToRowbinary, extend_json_deserialization
from tinybird.sql import parse_table_structure
from tinybird.ch import CHTable
from tinybird.views.json_deserialize_utils import json_deserialize_merge_schema_jsonpaths, parse_augmented_schema


@pytest.mark.parametrize("_type, value", [
    ("Nullable(Date)", None),
    ("Nullable(Date)", "2023-05-30"),
    ("Date", "2023-05-30"),
    ("Date32", "2023-05-30"),
    ("Nullable(DateTime)", None),
    ("Nullable(DateTime)", "2023-05-30 00:00:00"),
    ("DateTime", "2023-05-30 00:00:00"),
    ("Nullable(DateTime('Europe/Moscow'))", None),
    ("Nullable(DateTime('UTC'))", "2023-05-30 00:00:00"),
    ("DateTime('UTC')", "2023-05-30 00:00:00"),
    ("String", "hola"),
    ("Nullable(String)", "hola"),
    ("Nullable(String)", None),
    ("Int8", 1),
    ("Int16", 1),
    ("Int32", 1),
    ("Int64", 1),
    ("Nullable(Int8)", 1),
    ("Nullable(Int16)", 1),
    ("Nullable(Int32)", 1),
    ("Nullable(Int64)", 1),
    ("Nullable(Int8)", None),
    ("Nullable(Int16)", None),
    ("Nullable(Int32)", None),
    ("Nullable(Int64)", None),
    ("UInt8", 1),
    ("UInt16", 1),
    ("UInt32", 1),
    ("UInt64", 1),
    ("Nullable(UInt8)", 1),
    ("Nullable(UInt16)", 1),
    ("Nullable(UInt32)", 1),
    ("Nullable(UInt64)", 1),
    ("Nullable(UInt8)", None),
    ("Nullable(UInt16)", None),
    ("Nullable(UInt32)", None),
    ("Nullable(UInt64)", None),
    ("Float32", 1.1),
    ("Float64", 1.1),
    ("Nullable(Float32)", 1.1),
    ("Nullable(Float64)", 1.1),
    ("Nullable(Float32)", None),
    ("Nullable(Float64)", None),
    ("Map(String, String)", {"key": "value1"}),
    ("Map(String, UInt32)", {"key": 1}),
    ("Map(String, Nullable(String))", {"key": None}),
    ("Map(String, Map(String, String))", {"key": {"subkey": "value"}}),
    ("Map(String, Map(String, String))", {"key1": {"subkey11": "value11", "subkey12": "value12"}, "key2": {"subkey21": "value21", "subkey22": "value22"}}),
    ("Map(String, Array(String))", {"key": ["value1", "value2"]}),
    ("Array(String)", []),
    ("Array(String)", ['value1', 'value2']),
    ("Array(Nullable(String))", []),
    ("Array(Nullable(String))", ['value1', None])
])
def test_convert_to_rowbinary(_type: str, value: any):
    if _type.startswith('Array'):
        json_path = 'json:$.value[:]'
    else:
        json_path = 'json:$.value'

    augmented_schema = f'`value` {_type} `{json_path}`'
    json_value = json.dumps({'value': value}).encode('utf-8')

    parsed_schema = parse_augmented_schema(augmented_schema)
    merged_schema = json_deserialize_merge_schema_jsonpaths(parse_table_structure(parsed_schema.schema), parsed_schema.jsonpaths)
    extended_schema = extend_json_deserialization(merged_schema)
    converter = JSONToRowbinary(extended_schema)

    converter.convert(json_obj=json_value)
    row_binary_value, _ = converter.flush()

    # tweak schema for compatibility with CHTable
    for item in merged_schema:
        item['normalized_name'] = item['name']
        del item['jsonpath']

    chlocal_str_value = CHTable(merged_schema).query(row_binary_value, 'select * from table', input_format='RowBinary', output_format='JSONEachRow')
    assert chlocal_str_value is not None, f'expected {value} got None for type {_type}'
    assert len(chlocal_str_value) > 0, f'expected {value} got empty string for type {_type}'

    chlocal_value = json.loads(chlocal_str_value).get("value", "error-value")

    # workaround to solve CH local returns string instead of int in some types for some reason...
    match = re.match(r'^(Nullable\()?(Int64|Int128|Int256|UInt64|UInt128|UInt256)(\))?', _type)
    if chlocal_value and match:
        chlocal_value = int(chlocal_value)

    assert value == chlocal_value, f'expected {value} got {chlocal_value} for type {_type}'
