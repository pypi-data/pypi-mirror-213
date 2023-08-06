# Data Generator - WIP

## Overview
During every data project I came across a very basic common problem where we have to wait for the test data. For fewer columns it's quite easy to generate the data using online utilities but those have certain limitations on the number of columns and rows.
To solve this, I’ve built a utility to generate the mock data based on the supplied json schema.
This utility is using Python Faker module to randomly generate the test data.
Step by step guide on [medium](https://medium.com/@rahulsmtauti/mock-data-generation-for-data-projects-3999865cb82c).

## How to use
Follow below steps to run the utility. I am open to your suggestions, please add comments or mail me your suggestions.

**Note: Data Types are case insensitive**
### Inputs
It accept valid json schema files only with supported data types: `"STRING","INT","INTEGER","NUMBER","FLOAT","DATE","BOOLEAN","BOOL","TIMESTAMP","ADDRESS","CITY","COUNTRY","COUNTRY_CODE","POSTCODE","LICENSE_PLATE","SWIFT","COMPANY","COMPANY_SUFFIX","CREDIT_CARD","CREDIT_CARD_PROVIDER","CREDIT_CARD_NUMBER","CURRENCY","DAY_NUM","DAY_NAME","MONTH_NUM","MONTH_NAME","YEAR","COORDINATE","LATITUDE","LONGITUDE","EMAIL","HOSTNAME","IPV4","IPV6","URI","URL","JOB","TEXT","PASSWORD","SHA1","SHA256","UUID","PASSPORT_NUMBER","NAME","LANGUAGE_NAME","LAST_NAME","FIRST_NAME","PHONE_NUMBER","SSN"`
#### Supported Input Parameters

- --input_json_schema_path: Provide absolute path of the json schema file/folder. It accepts folders(that contains valid json schema files) or absolute path of a json schema file.

> Json schema file format.
```json
{
  "type": "<object/record,etc>",
  "number_of_rows": "<positive number>",
  "properties": {
    "<column_name>": { "type": "<data_type>" },
    "<column_name>": { "type": "<data_type>" }
  }
}

```
> The sample json schema file would look like below.
```json
{
  "type": "object",
  "number_of_rows": "<positive number>",
  "properties": {
    "price": { "type": "number" },
    "name": { "type": "name" },
    "location": { "type": "COORDINATE" },
    "flt": { "type": "float" },
    "email_id": { "type": "EMAIL" },
    "dt": { "type": "date" },
    "ts": { "type": "timestamp" },
    "is_valid": { "type": "boolean" }
  }
}
```
The generator will skip the current json schema file if an error occurred. Mock data would get generated for rest of the valid schema files.

- --output_file_format: The output file format should be one of the `"CSV","JSON","XML","EXCEL","PARQUET","ORC"`

- --output_path: Absolute path to store the generated mock dataset. If an output path does not exists, it will create it and store the data inside the directory into data.<output file format> file.


### Pre-requisites
1. Python ^3.10


### Steps to execute the utility
1. pip install mock-data-generator
2. specify the parameters mentioned above
4. Sample command: `generate --input_json_schema_path=resources/schema.json --output_file_format=csv --output_path=output_data --number_of_rows=10 ` :

### Licensing
Distributed under the MIT license. See ``LICENSE`` for more information.
