from pandas import DataFrame


def save_output_as_csv(pd: DataFrame, output_path: str):
    pd.to_csv(f"{output_path}/data.csv")


def save_output_as_json(pd: DataFrame, output_path: str):
    pd.to_json(
        f"{output_path}/data.json", orient="records", date_format="iso", lines=True
    )


def save_output_as_xml(pd: DataFrame, output_path: str):
    pd.to_xml(f"{output_path}/data.xml")


def save_output_as_excel(pd: DataFrame, output_path: str):
    pd.to_excel(f"{output_path}/data.xlsx", header=True)


def save_output_as_parquet(pd: DataFrame, output_path: str):
    pd.to_parquet(f"{output_path}/data.parquet", compression="snappy")


def save_output_as_orc(pd: DataFrame, output_path: str):
    pd.to_orc(f"{output_path}/data.orc")
