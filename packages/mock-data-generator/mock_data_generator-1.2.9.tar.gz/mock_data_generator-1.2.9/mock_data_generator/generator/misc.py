from faker import Faker


def generate_address(fkr: Faker):
    return fkr.address()


def generate_city(fkr: Faker):
    return fkr.city()


def generate_country(fkr: Faker):
    return fkr.country()


def generate_country_code(fkr: Faker):
    return fkr.country_code()


def generate_postcode(fkr: Faker):
    return fkr.postcode()


def generate_license_plate(fkr: Faker):
    return fkr.license_plate()


def generate_swift(fkr: Faker):
    return fkr.swift()


def generate_company(fkr: Faker):
    return fkr.company()


def generate_company_suffix(fkr: Faker):
    return fkr.company_suffix()


def generate_credit_card(fkr: Faker):
    return fkr.credit_card_full()


def generate_credit_card_provider(fkr: Faker):
    return fkr.credit_card_provider()


def generate_credit_card_number(fkr: Faker):
    return fkr.credit_card_number()


def generate_currency(fkr: Faker):
    return fkr.pricetag()


def generate_day_num(fkr: Faker):
    return fkr.day_of_month()


def generate_day_name(fkr: Faker):
    return fkr.day_of_week()


def generate_month_num(fkr: Faker):
    return fkr.month()


def generate_month_name(fkr: Faker):
    return fkr.month_name()


def generate_year(fkr: Faker):
    return fkr.year()


def generate_coordinate(fkr: Faker):
    return fkr.coordinate()


def generate_latitude(fkr: Faker):
    return fkr.latitude()


def generate_longitude(fkr: Faker):
    return fkr.longitude()


def generate_email(fkr: Faker):
    return fkr.ascii_email()


def generate_hostname(fkr: Faker):
    return fkr.hostname()


def generate_ipv4(fkr: Faker):
    return fkr.ipv4()


def generate_ipv6(fkr: Faker):
    return fkr.ipv6()


def generate_uri(fkr: Faker):
    return fkr.uri()


def generate_url(fkr: Faker):
    return fkr.url()


def generate_job(fkr: Faker):
    return fkr.job()


def generate_text(fkr: Faker):
    return fkr.text()


def generate_password(fkr: Faker):
    return fkr.password(length=12)


def generate_sha1(fkr: Faker):
    return fkr.sha1(raw_output=False)


def generate_sha256(fkr: Faker):
    return fkr.sha256(raw_output=False)


def generate_uuid(fkr: Faker):
    return fkr.uuid4()


def generate_passport_number(fkr: Faker):
    return fkr.passport_number()


def generate_name(fkr: Faker):
    return fkr.name()


def generate_language_name(fkr: Faker):
    return fkr.language_name()


def generate_last_name(fkr: Faker):
    return fkr.last_name()


def generate_first_name(fkr: Faker):
    return fkr.first_name()


def generate_phone_number(fkr: Faker):
    return fkr.phone_number()


def generate_ssn(fkr: Faker):
    return fkr.ssn()
