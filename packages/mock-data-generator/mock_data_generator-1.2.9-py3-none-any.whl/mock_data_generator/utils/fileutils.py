import os
from mock_data_generator.schema_handler.schema_validator import (
    is_valid_json_schema_file,
)
from mock_data_generator.generator.generate import runner
from argparse import Namespace
import logging
import json


def read_json_file_as_string(file_path: str):
    with open(file_path) as f:
        return f.read()


def make_path_if_not_exists(file_path: str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def mk_run_call(schema_file_path: str, output_path: str, output_file_format: str):
    logging.info(f"Generating data for {schema_file_path}")
    json_schema_string = read_json_file_as_string(schema_file_path)
    if is_valid_json_schema_file(
        json_schema=json_schema_string, file_name=schema_file_path
    ):
        json_schema = json_str_to_json_object(json_schema=json_schema_string)
        runner(
            json_schema=json_schema,
            num_of_rows=json_schema["number_of_rows"],
            output_path=output_path,
            file_format=output_file_format,
        )


def proceed(args: Namespace):
    json_schema_path = args.input_json_schema_path
    if os.path.isdir(json_schema_path):
        for each_file in os.listdir(json_schema_path):
            if each_file.endswith(".json"):
                out_path = f'{args.output_path}/{each_file.replace(".json","")}'
                make_path_if_not_exists(file_path=out_path)
                file_path = f"{json_schema_path}/{each_file}"
                mk_run_call(
                    schema_file_path=file_path,
                    output_path=out_path,
                    output_file_format=args.output_file_format,
                )
    else:
        make_path_if_not_exists(args.output_path)
        mk_run_call(
            schema_file_path=json_schema_path,
            output_path=args.output_path,
            output_file_format=args.output_file_format,
        )


def json_str_to_json_object(json_schema: str):
    return json.loads(json_schema)
