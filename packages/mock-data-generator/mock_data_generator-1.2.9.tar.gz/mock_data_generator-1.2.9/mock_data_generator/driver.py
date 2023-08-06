import argparse
from mock_data_generator.utils.constants import FILE_FORMATS
from mock_data_generator.utils.fileutils import proceed


def validate_file_format(value):
    if value.upper() not in FILE_FORMATS:
        raise argparse.ArgumentTypeError(
            f"Unsupported output file format {value} detected. Supported file formats are {FILE_FORMATS}"
        )
    return value


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_json_schema_path",
        help="Input absolute path of the schema json, schema file or schema folder",
        required=True,
    )
    parser.add_argument(
        "--output_file_format",
        type=validate_file_format,
        help="Expected output file format(csv,json,xml,excel,parquet)",
        required=True,
    )
    parser.add_argument(
        "--output_path", help="Output path for mock dataset.", required=True
    )
    args = parser.parse_args()
    proceed(args=args)


if __name__ == "__main__":
    run()
