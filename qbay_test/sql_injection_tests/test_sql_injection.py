# Import functions to test
from qbay.models import *

# Read data from SQL Injection file
all_payloads = open("./qbay_test/sql_injection_tests/Generic_SQLI.txt", "r")

# Create user for testing
register("InjectionTestUser",
         "injection_test@qbay.com",
         "Password99@")


def test_cp_title_sql_injection():
    error_causing_inputs = []
    for payload in all_payloads:
        payload = payload.strip()
        legal_desc = "a" * (len(payload) + 1)
        try:
            create_product(payload,
                           legal_desc,
                           11.0,
                           "injection_test@qbay.com")
        except Exception as e:
            print("Error from description {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
    assert not error_causing_inputs


def test_cp_description_sql_injection():
    error_causing_inputs = []
    product_num = 1
    for payload in all_payloads:
        payload = payload.strip()
        try:
            create_product("DescInjection" + str(product_num),
                           payload,
                           11.0,
                           "injection_test@qbay.com")
        except Exception as e:
            print("Error from description {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        product_num += 1
    assert not error_causing_inputs


def test_cp_user_email_sql_injection():
    error_causing_inputs = []
    product_num = 1
    for payload in all_payloads:
        payload = payload.strip()
        try:
            create_product("EmailInjection" + str(product_num),
                           "24 character description",
                           11.0,
                           "injection_test@qbay.com")
        except Exception as e:
            print("Error from user email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        product_num += 1
    assert not error_causing_inputs


# Test username
def test_register_username_sql_injection():
    error_causing_inputs = []
    user_num = 1
    for payload in all_payloads:
        try:
            register(payload,
                     "injection_test@qbay.com",
                     "Password99@")
        except Exception as e:
            print("Error from username {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        user_num += 1
    assert not error_causing_inputs


# Test email
def test_register_email_sql_injection():
    error_causing_inputs = []
    user_num = 1
    for payload in all_payloads:
        try:
            register("InjectionTestUser" + str(user_num),
                     payload + "@qbay.com",
                     "Password99@")
        except Exception as e:
            print("Error from email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        user_num += 1
    assert not error_causing_inputs


# Test password
def test_register_password_sql_injection():
    error_causing_inputs = []
    user_num = 1
    for payload in all_payloads:
        try:
            register("InjectionTestUser" + str(user_num),
                     "injection_test@qbay.com",
                     payload)
        except Exception as e:
            print("Error from password {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        user_num += 1
    assert not error_causing_inputs
