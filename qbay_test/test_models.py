from qbay.models import register, login, \
    create_product, update_user, update_product, order, get_products
import datetime


def test_r1_1_user_register():
    '''
    Testing R1-1: Both the email and password cannot be empty
    '''

    assert register('user0', '', 'Legalpass!') is False
    assert register('user0', '', 'Legalpass!') is False
    assert register('user0', 'test@test.com', '') is False
    assert register('user0', 'test@test.com', '') is False
    assert register('user0', '', '') is False


def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified by his/her email address.
    '''

    # Being unable to add a new user with the same email ensures that all
    # users are uniquely identified by their email
    assert register('user', 'test0@test.com', 'Legalpass!') is True
    assert register('user1', 'test0@test.com', 'Legalpass!') is False


def test_r1_3_user_register():
    '''
    Testing R1-3: The email has to follow addr-spec defined in RFC 5322
    '''

    # no @
    assert register('user0', 'test0.test.com', 'Legalpass!') is False
    # too many @
    assert register('user0', 'test0@test@.com', 'Legalpass!') is False
    # illegal local part characters
    assert register('user0', ':;<>[]@test.com', 'Legalpass!') is False
    # illegal space
    assert register('user0', 'test 0@test.com', 'Legalpass!') is False
    # illegal domain characters
    assert register('user0', 'test0@*$&test_test.com', 'Legalpass!') is False
    # local too short
    assert register('user0', '@test.com', 'Legalpass!') is False
    # domain DNS segments too short
    assert register('user0', 'test@..', 'Legalpass!') is False
    # no . in domain
    assert register('user0', 'test@test', 'Legalpass!') is False
    # no . in domain
    assert register('user0', 'test@test', 'Legalpass!') is False
    # local name too long
    assert register('user0',
                    ('11111111111111111111111111111111111111111111111111'
                     '11111111111111@test'), 'Legalpass!') is False


def test_r1_4_user_register():
    '''
    Testing R1-4: Password has to meet the required complexity: minimum length
    6, ar least one upper case, at least one lower case, and at least one
    special character.
    '''

    # Length 5
    assert register('user0', 'test@test.com', 'Lega!') is False
    # No upper case
    assert register('user0', 'test@test.com', 'legalpass!') is False
    # No lower case
    assert register('user0', 'test@test.com', 'LEGALPASS!') is False
    # No special character
    assert register('user0', 'test@test.com', 'legalpass') is False


def test_r1_5_user_register():
    '''
    Testing R1-5: User name has to be non-empty, alphanumeric-only, and space
    allowed only if it is not as the prefix or suffix
    '''

    # empty
    assert register('', 'test@test.com', 'Legalpass!') is False
    # special characters
    assert register('user0!', 'test@test.com', 'Legalpass!') is False
    # space at the start
    assert register(' user0', 'test@test.com', 'Legalpass!') is False
    # space at the end
    assert register('user0 ', 'test@test.com', 'Legalpass!') is False
    # space in the middle
    assert register('user 0', 'test2@test.com', 'Legalpass!') is True


def test_r1_6_user_register():
    '''
    Testing R1-6: User name has to be longer than 2 characters and less than 20
    characters.
    '''

    # too short
    assert register('u0', 'test@test.com', 'Legalpass!') is False

    # too long
    assert register('u1111111111111111111',
                    'test@test.com', 'Legalpass!') is False


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    # Users with the same username can be added but not the same email.
    # test0@test.com was used in R1-2
    assert register('user', 'test1@test.com', 'Legalpass!') is True
    assert register('user1', 'test0@test.com', 'Legalpass!') is False


def test_r1_8_user_register():
    '''
    Testing R1-8: Shipping address is empty at the time of registration.
    '''

    # If email test0@test.com, registered without a shipping address,
    # still has an empty shipping address, the condition is satisfied
    user = login('test0@test.com', 'Legalpass!')
    assert user.shipping_address == ''


def test_r1_9_user_register():
    '''
    Testing R1-9: Postal code is empty at the time of registration.
    '''

    # If email test0@test.com, registered without a postal code,
    # still has an empty postal code, the condition is satisfied
    user = login('test0@test.com', 'Legalpass!')
    assert user.postal_code == ''


def test_r1_10_user_register():
    '''
    Testing R1-10: Balance should be initialized as 100 at time of
    registration.
    '''

    # If email test0@test.com, registered without a balance,
    # is automatically loaded with 100 dollars, the condition is satisfied
    user = login('test0@test.com', 'Legalpass!')
    assert user.balance == 100.00


# Users that have been inserted from register test cases:
# - 'user', 'test0@test.com', 'Legalpass!'
# - 'user', 'test1@test.com', 'Legalpass!'
# - 'user 0', 'test2@test.com', 'Legalpass!'

def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    (will be tested after the previous test, so we already have user0,
      user1 in database)
    '''

    user = login('test0@test.com', 'Legalpass!')
    assert user is not None
    assert user.username == 'user'

    user = login('test0@test.com', 'Unusedpass!')
    assert user is None


def test_r3_update_user():
    '''
    Testing:

        R3-1: A user is only able to update his/her
        user name, shipping_address, and postal_code.
        R3-2: Shipping_address should be non-empty, alphanumeric-only,
        and no special characters such as !.
        R3-3: Postal code has to be a valid Canadian postal code.
        R3-4: User name follows the requirements above.

    (will be tested after the previous test, so we already have u0,
      u1 in database)
    '''

    # R3-1
    result = update_user('test0@test.com', 'WRONGPASS', {'username': 'apache'})
    assert result is False
    result = update_user('test0@test.com', 'Legalpass!',
                         {'password': 'apache'})
    assert result is False

    # R3-4
    result = update_user('test0@test.com', 'Legalpass!',
                         {'username': 'apache'})
    assert result is not False
    result = update_user('test0@test.com', 'Legalpass!',
                         {'username': ''})
    assert result is False

    # R3-3
    result = update_user('test0@test.com', 'Legalpass!',
                         {'postal_code': 'N2P 4M1'})
    assert result is not False
    result = update_user('test0@test.com', 'Legalpass!',
                         {'postal_code': 'aaa 123'})
    assert result is False

    # R3-2
    result = update_user('test0@test.com', 'Legalpass!',
                         {'shipping_address': '123 fake st'})
    assert result is not False
    result = update_user('test0@test.com', 'Legalpass!',
                         {'shipping_address': '123 fake st!'})
    assert result is False


# create_product tests also make use of the users created in register tests
# ('test0@test.com', 'test1@test.com', 'test2@test.com')
def test_r4_1_create_product():
    """
    Testing R4-1: The title of the product is alphanumeric-only,
    and spaces cannot appear as a prefix or a suffix.
    """
    # Not alphanumeric
    assert create_product("notAlphanumeric$%^",
                          "24 character description",
                          11.0, "test0@test.com") is False
    # Illegal leading space
    assert create_product(" leading space",
                          "24 character description",
                          11.0, "test0@test.com") is False
    # Illegal trailing space
    assert create_product("trailing space ",
                          "24 character description",
                          11.0, "test0@test.com") is False
    # Meets specifications
    assert create_product("product 0",
                          "24 character description",
                          11.0, "test0@test.com") is True


def test_r4_2_create_product():
    """
    Testing R4-2: The title of the product is no longer than 80
    characters.
    """
    # Long string to test 80 char limit
    over_80_chars = """veeeeeeerrrrryyyyyy
                    looooooooooooooooooooooooooonnnnnnnnnnnnnnnnnng
                    tiiiiiiittttle"""

    # Too many chars
    assert create_product(over_80_chars,
                          "24 character description",
                          11.0, "test0@test.com") is False


def test_r4_3_create_product():
    """
    Testing R4-3: Description must have a minimum length 20 characters and
    a maximum length of 2000 characters.
    """
    # Generate description over 2000 chars for testing
    over_two_thousand = ""
    for i in range(0, 2001):
        over_two_thousand += "a"

    # Description too short
    assert create_product("product 1",
                          "desc under 20", 11.0,
                          "test1@test.com") is False
    # Description too long
    assert create_product("product 1",
                          over_two_thousand,
                          11.0, "test1@test.com") is False


def test_r4_4_create_product():
    """
    Testing R4-4: Description has to be longer than the product's title.
    """
    # Description is too short relative to title
    assert create_product("title longer than description",
                          "24 character description",
                          11.0, "test1@test.com") is False


def test_r4_5_create_product():
    """
    Testing R4-5: Price has to be in range [10, 10000].
    """
    # Product cost too low
    assert create_product("product 1",
                          "24 character description",
                          9.0, "test1@test.com") is False
    # product cost too high
    assert create_product("product 1",
                          "24 character description",
                          10001.0, "test1@test.com") is False


def test_r4_6_create_product():
    """
    Testing R4-6: last_modified_date must be after 2021-01-02 and
    before 2025-01-02.
    """
    # Disallowed date - too early
    assert create_product("product 1",
                          "24 character description",
                          11.0, "test1@test.com",
                          datetime.date(2020, 9, 29)) is False
    # Disallowed date - too late
    assert create_product("product 1",
                          "24 character description",
                          11.0, "test1@test.com",
                          datetime.date(2030, 9, 29)) is False
    # Date in appropriate range
    assert create_product("product 1",
                          "24 character description",
                          11.0, "test1@test.com",
                          datetime.date(2022, 9, 29)) is True


def test_r4_7_create_product():
    """
    Testing R4-7: The owner of the corresponding product
    must exist in the database.
    """
    # Empty seller email
    assert create_product("product 2",
                          "24 character description",
                          11.0, "") is False
    # Seller email (notinDB@test.com) is not in the database
    assert create_product("product 2",
                          "24 character description",
                          11.0, "notinDB@test.com") is False


def test_r4_8_create_product():
    """
    Testing R4-8: A user cannot create products that have the same title.
    """
    # repeat existing product name ('product 0') for user test0@test.com
    assert create_product("product 0",
                          "24 character description",
                          11.0, "test0@test.com") is False


# Products that have been inserted from create_product test cases:
# - "product 0", "24 character description", 11.0, "test0@test.com"
# - "product 1", "24 character description", 11.0, "test1@test.com",
#   datetime.date(2022, 9, 29)


def test_r5_1_update_product():
    '''
    Testing R5-1: Can update all attributes of the product except owner_email \
        and last_modified_date.
    NOTE: Seller_email cannot be updated and is not in "updated_params".
    '''

    # Changing last_date_modified manually is false - not possible
    result = update_product(
        'product 0',
        11.00,
        'test0@test.com',
        {'last_modified_date': (datetime.date(2021, 3, 4))})
    assert result is False

    # Changing seller_email manually is false - not possible
    result = update_product(
        'product 0',
        11.00,
        'test0@test.com',
        {'seller_email': 'test3@test.com'})
    assert result is False


def test_r5_2_update_product():
    '''
    Testing R5-2: Price can only be increased but cannot be decreased.
    '''

    # Price of product that did not change is True (no change to instance)
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'price': 11.00})
    assert result is True

    # updating price to $0.00 does not follow requirement R5-2
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'price': 0.00})
    assert result is False

    # decreasing price to $10.00 does not follow requirement R5-2
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'price': 10.00})
    assert result is False

    # increasing price of product to 13.00 is successful
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'price': 13.00})
    assert result is True


def test_r5_3_update_product():
    '''
    Testing R5-3: last_modified_date should be updated when
    the updated operation is successful.
    '''

    # if last_date_modified was updated successfully, then true
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'title': 'product 1'})
    assert result is True


def test_r5_4_update_product():
    '''
    Testing R5-4: When updating an attribute, one has to make sure
    that it follows the same requirements as "create_product".
    '''

    # a title that is not alphanumeric-only is false
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'title': 'abcd123!@#'})
    assert result is False

    # a title that is longer than 80 characters is false
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'title': 'serhfh diusfhiuo sdufyhdsiuyf '
                                      'fudisyhfuidsy '
                                      'fdssedfhgjdsuiafgrugf '
                                      'udigphuiofsdghiuf'})
    assert result is False

    # A description with a length of characters
    # less than 20 (or larger than 2000) is false.
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'description': 'abcdefghijkl'})
    assert result is False

    # A description with a length  less than its title is false.
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'description': 'hi'})
    assert result is False

    # A price outside the range of [10, 10000] is false.
    result = update_product('product 0',
                            11.00,
                            'test0@test.com',
                            {'price': 1000000.00})
    assert result is False


def test_r6_1_order():
    '''
    Testing R6-1: A user can place an order on the products
    '''

    # login two users
    user0 = login('test0@test.com', 'Legalpass!')
    user1 = login('test1@test.com', 'Legalpass!')

    # create a new product for user 0
    result = create_product("trans product",
                            "24 character description",
                            12.0, "test0@test.com")
    assert result is True

    user0_old_balance = user0.balance
    user1_old_balance = user1.balance

    # have user 1 buy that product
    result = order("trans product", "test0@test.com", "test1@test.com")
    assert result is True
    assert user0.balance == user0_old_balance + 12.0
    assert user1.balance == user1_old_balance - 12.0


def test_r6_2_order():
    '''
    Testing R6-2: A user cannot place an order
    for his/her products
    '''

    # login two users
    user0 = login('test0@test.com', 'Legalpass!')  # seller

    # create a new product for user 0
    result = create_product("my product",
                            "24 character description",
                            12.0, "test0@test.com")
    assert result is True

    user0_old_balance = user0.balance

    # have user 0 buy their own product
    result = order("my product", "test0@test.com", "test0@test.com")
    assert result is False
    assert user0.balance == user0_old_balance


def test_r6_3_order():
    '''
    Testing R6-3: A user cannot place an order
    that costs more than his/her balance
    '''

    # login two users
    user0 = login('test0@test.com', 'Legalpass!')  # seller
    user1 = login('test1@test.com', 'Legalpass!')  # buyer

    # create a new product for user 0,
    # where price is greater than user1's balance
    result = create_product("high cost product",
                            "24 character description",
                            100.0, "test0@test.com")
    assert result is True

    user0_old_balance = user0.balance
    user1_old_balance = user1.balance

    # user 1 buys that product and returns False -
    # price is greater than their balance
    result = order("high cost product", "test0@test.com", "test1@test.com")
    assert result is False
    assert user0.balance == user0_old_balance
    assert user1.balance == user1_old_balance


def test_r7_1_get_products():
    '''
    Testing R7-1: get list of available products
    '''
    
    # Three products currently created, all three are visible to user0
    user0_products = get_products("test0@test.com")
    assert len(user0_products) == 3

    # The last is invisible to user1 because it was just bought by them
    user1_products = get_products("test1@test.com")
    assert len(user1_products) == 2
