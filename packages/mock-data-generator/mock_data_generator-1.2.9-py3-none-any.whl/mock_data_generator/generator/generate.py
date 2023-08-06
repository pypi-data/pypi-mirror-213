import pandas as pd
from faker import Faker
from tqdm import tqdm
from mock_data_generator.generator.predefined import *
from mock_data_generator.generator.misc import *
from mock_data_generator.generator.output import *
from mock_data_generator.generator.mappings import (
    data_type_to_func_map,
    file_format_to_func_map,
)


def runner(json_schema: any, num_of_rows: int, output_path: str, file_format: str):
    schema_dict = json_schema["properties"]
    fkr = Faker()
    pd_df = pd.DataFrame()
    for column_name in schema_dict:
        type_dict = schema_dict[column_name]
        column_type = type_dict["type"]
        for cnt in tqdm(
            range(num_of_rows), desc=f"Generating mock data for: {column_name}"
        ):
            function_name = data_type_to_func_map[column_type.upper()]
            pd_df.loc[cnt, column_name] = globals()[function_name](fkr=fkr)

    file_format_function_name = file_format_to_func_map[file_format.upper()]
    globals()[file_format_function_name](pd_df, output_path)
