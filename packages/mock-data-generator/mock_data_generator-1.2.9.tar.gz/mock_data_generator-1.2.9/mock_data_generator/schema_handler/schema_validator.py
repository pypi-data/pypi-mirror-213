import json
import logging

from mock_data_generator.utils.constants import DATA_TYPES


class ValidationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def is_valid_json_schema_file(json_schema: str, file_name: str):
    try:
        json_object = json.loads(json_schema)
        schema_dict = json_object["properties"]
        number_of_rows = json_object["number_of_rows"]

        if number_of_rows <= 0:
            logging.error(
                f"Positive value expected for number_of_rows in the {file_name}"
            )
            raise (ValidationError(number_of_rows))

        for column_name in schema_dict:
            type_dict = schema_dict[column_name]
            data_type = type_dict["type"].upper()
            if data_type not in DATA_TYPES:
                logging.error(f"Skipping file {file_name}")
                logging.error(
                    f"Invalid data type {ex.value} detected in json. Supported data type {DATA_TYPES}"
                )
                raise (ValidationError(data_type))

    except ValueError as ex:
        logging.error(f"Skipping invalid schema file {file_name}")
        logging.error(f"Invalid json schema file({file_name}) provided: {ex}")
        return False

    except ValidationError as ex:
        return False

    except KeyError as kr:
        logging.error(
            f"Skipping file {file_name}. Mandatory key {kr} not found in the json file provided."
        )
        return False

    return True
