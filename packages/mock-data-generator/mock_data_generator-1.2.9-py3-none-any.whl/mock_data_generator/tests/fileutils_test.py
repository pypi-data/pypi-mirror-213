from utils.fileutils import read_json_file_as_string, json_str_to_json_object


def test_read_valid_json_file_as_string():
    sample_file_path = "mock_data_generator/resources/schema.json"
    file_content = read_json_file_as_string(sample_file_path)
    assert type(file_content) == str


def test_json_str_to_json_object_should_return_json_object():
    json_string = """{
    "type" : "object",
    "properties" :
        {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"}
        }
        }
    """
    result = json_str_to_json_object(json_schema=json_string)
    assert type(result) == dict
