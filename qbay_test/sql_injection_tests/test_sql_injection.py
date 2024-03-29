# Import functions to test
from qbay.models import *

# Read data from SQL Injection file
all_payloads = open("./qbay_test/sql_injection_tests/Generic_SQLI.txt", "r")

# Create user for testing
register("InjectionTestUser",
         "injection_test@qbay.com",
         "Password99@")


# Following Professor Ding's instruction, we only test fields that accept
# string input. Non-String fields (like price or date for create_product())
# are not amenable to the current testing methods.


def test_cp_title_sql_injection():
    """
    A function that tests whether the title field of the create_product
    function is vulnerable to SQL injection attacks. For each payload
    (from the Generic_SQLI.txt file opened above), we run the
    create_product function with the payload as the title. All other
    parameters in create_product are set to a legal value.

    :raise: AssertionError if one or more payloads cause an error in
            create_product.
    """
    # a list that will be populated with any error-causing payloads
    error_causing_inputs = []
    for payload in all_payloads:
        t_length = len(payload)
        # Legal description has to be longer than title and >=20 chars
        legal_desc = "a" * (t_length + 1) if t_length >= 20 else "a" * 20
        try:
            create_product(payload,
                           legal_desc,
                           11.0,
                           "injection_test@qbay.com",
                           datetime.date(2022, 9, 29))
        except Exception as e:
            # Print payload that caused error, along with error message
            print("Error from title {" + payload + "}: " + str(e))
            # Add the payload to the list of error-causing inputs
            error_causing_inputs.append(payload)
    # The test will fail if there are one or more error-causing inputs
    assert not error_causing_inputs


def test_cp_description_sql_injection():
    """
    A function that tests whether the description field of the create_product
    function is vulnerable to SQL injection attacks. For each payload, we run
    the create_product function with the payload as the description. All other
    parameters are set to a legal value.

    :raise: AssertionError if one or more payloads cause an error in
            create_product.
    """
    error_causing_inputs = []
    # product_num used to create a unique title for each run of create_product
    product_num = 1
    for payload in all_payloads:
        try:
            create_product("DescInjection" + str(product_num),
                           payload,
                           11.0,
                           "injection_test@qbay.com",
                           datetime.date(2022, 9, 29))
        except Exception as e:
            print("Error from description {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        product_num += 1
    assert not error_causing_inputs


def test_cp_seller_email_sql_injection():
    """
    A function that tests whether the seller_email field of the create_product
    function is vulnerable to SQL injection attacks. For each payload, we run
    the create_product function with the payload as the seller email. All other
    parameters are set to a legal value.

    :raise: AssertionError if one or more payloads cause an error in
            create_product.
    """
    error_causing_inputs = []
    # product_num used to create a unique title for each run of create_product
    product_num = 1
    for payload in all_payloads:
        try:
            create_product("EmailInjection" + str(product_num),
                           "24 character description",
                           11.0,
                           payload,
                           datetime.date(2022, 9, 29))
        except Exception as e:
            print("Error from seller email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        product_num += 1
    assert not error_causing_inputs


def test_register_username_sql_injection():
    """
       A function that tests whether the username field of the register
       function is vulnerable to SQL injection attacks. For each payload,
       we run the register function with the payload as the username.
       All other parameters are set to a legal value.

       :raise: AssertionError if one or more payloads cause an error in
               register.
       """
    error_causing_inputs = []
    user_num = 1
    for payload in all_payloads:
        try:
            register(payload,
                     "injection_test" + str(user_num) + "@qbay.com",
                     "Password99@")
        except Exception as e:
            print("Error from username {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        user_num += 1
    assert not error_causing_inputs


def test_register_email_sql_injection():
    """
        A function that tests whether the email field of the register
        function is vulnerable to SQL injection attacks. For each payload,
        we run the register function with the payload as the email.
        All other parameters are set to a legal value.

        NOTE: Since assignment instructions say to run the function with
        the payload as the parameter's value, we did not include the "@..."
        portion of the email field below.

        :raise: AssertionError if one or more payloads cause an error in
                register.
        """
    error_causing_inputs = []
    user_num = 1
    for payload in all_payloads:
        try:
            register("InjectionTestUser" + str(user_num),
                     payload,
                     "Password99@")
        except Exception as e:
            print("Error from email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        user_num += 1
    assert not error_causing_inputs


def test_register_password_sql_injection():
    """
        A function that tests whether the password field of the register
        function is vulnerable to SQL injection attacks. For each payload,
        we run the register function with the payload as the password.
        All other parameters are set to a legal value.

        :raise: AssertionError if one or more payloads cause an error in
                register.
        """
    error_causing_inputs = []
    user_num = 1
    for payload in all_payloads:
        try:
            register("InjectionTestUser" + str(user_num),
                     "injection_test" + str(user_num) + "@qbay.com",
                     payload)
        except Exception as e:
            print("Error from password {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
        user_num += 1
    assert not error_causing_inputs


def test_order_prod_sql_injection():
    """
         A function that tests whether the product title field of the
         order function is vulnerable to SQL injection attacks. For
         each payload, we run the order function with the payload as
         the product title.
         All other parameters are set to a legal value.

         :raise: AssertionError if one or more payloads cause an error in
                 order.
         """
    error_causing_inputs = []
    for payload in all_payloads:
        try:
            order(payload,
                  "test0@test.com",
                  "test1@test.com",
                  datetime.date(2022, 9, 29))
        except Exception as e:
            print("Error from product title {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
    assert not error_causing_inputs


def test_order_seller_sql_injection():
    """
         A function that tests whether the seller email field of the
         order function is vulnerable to SQL injection attacks. For
         each payload, we run the order function with the payload as
         the seller email.
         All other parameters are set to a legal value.

         :raise: AssertionError if one or more payloads cause an error in
                 order.
         """
    error_causing_inputs = []
    for payload in all_payloads:
        try:
            order("trans product",
                  payload,
                  "test1@qbay.com",
                  datetime.date(2022, 9, 29))
        except Exception as e:
            print("Error from seller email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
    assert not error_causing_inputs


def test_order_buyer_sql_injection():
    """
         A function that tests whether the buyer email field of the
         order function is vulnerable to SQL injection attacks. For
         each payload, we run the order function with the payload as
         the buyer email.
         All other parameters are set to a legal value.

         :raise: AssertionError if one or more payloads cause an error in
                 order.
         """
    error_causing_inputs = []
    for payload in all_payloads:
        try:
            order("trans product",
                  "test0@qbay.com",
                  payload,
                  datetime.date(2022, 9, 29))
        except Exception as e:
            print("Error from buyer email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
    assert not error_causing_inputs


def test_sp_email_sql_injection():
    """
         A function that tests whether the seller email field of the
         get_sold_products function is vulnerable to SQL injection attacks.
         For each payload, we run the get_sold_products function with
         the payload as the password.

         :raise: AssertionError if one or more payloads cause an error in
                 get_sold_products.
         """
    error_causing_inputs = []
    for payload in all_payloads:
        try:
            get_sold_products(payload)
        except Exception as e:
            print("Error from seller email {" + payload + "}: " + str(e))
            error_causing_inputs.append(payload)
    assert not error_causing_inputs
