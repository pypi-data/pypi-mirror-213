from faker import Faker


def generate_string_data(fkr: Faker):
    return fkr.pystr()


def generate_integer_data(fkr: Faker):
    return fkr.random_int()


def generate_float_data(fkr: Faker):
    return fkr.pyfloat()


def generate_date_data(fkr: Faker):
    return fkr.date()


def generate_boolean_data(fkr: Faker):
    return fkr.pybool()


def generate_timestamp_data(fkr: Faker):
    return fkr.date_time()
