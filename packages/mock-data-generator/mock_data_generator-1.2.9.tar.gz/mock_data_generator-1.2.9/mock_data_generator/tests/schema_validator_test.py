
from schema_handler.schema_validator import is_valid_json_schema_file


def test_schema_validator_for_valid_json():
    json_schema = """{
    "type" : "object",
    "properties" :
        {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"}
        }
        }
    """
    result = is_valid_json_schema_file(json_schema=json_schema, file_name="test.json")
    assert result


def test_schema_validator_for_invalid_json():
    json_schema = """{
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
        }
        }
    """
    result = is_valid_json_schema_file(json_schema=json_schema, file_name="test.json")
    assert result == False
