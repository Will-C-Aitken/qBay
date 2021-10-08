from qbay.models import register, login, create_product
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

# create_product tests also make use of the users created in register tests
# ('test0@test.com', 'test1@test.com', 'test2@test.com')


def test_r4_1_create_product():
    """
    Testing R4-1: The title of the product is alphanumeric-only,
    and spaces cannot appear as a prefix or a suffix.
    """
    # Not alphanumeric
    assert create_product("notAlphanumeric$%^", "24 character description", 11.0, "test0@test.com") is False
    # Illegal leading space
    assert create_product(" leading space", "24 character description", 11.0, "test0@test.com") is False
    # Illegal trailing space
    assert create_product("trailing space ", "24 character description", 11.0, "test0@test.com") is False
    # Meets specifications
    assert create_product("product 0", "24 character description", 11.0, "test0@test.com") is True


def test_r4_2_create_product():
    """
    Testing R4-2: The title of the product is no longer than 80 characters.
    """
    # Long string to test 80 char limit
    over_80_chars = "veeeeeeerrrrryyyyyy looooooooooooooooooooooooooonnnnnnnnnnnnnnnnnng tiiiiiiittttle"

    # Too many chars
    assert create_product(over_80_chars, "24 character description", 11.0, "test0@test.com") is False


def test_r4_3_create_product():
    """
    Testing R4-3: Description must have a minimum length 20 characters and a maximum length of
    2000 characters.
    """
    # Generate description over 2000 chars for testing
    over_two_thousand = ""
    for i in range(0, 2001):
        over_two_thousand += "a"

    # Description too short
    assert create_product("product 1", "desc under 20", 11.0, "test1@test.com") is False
    # Description too long
    assert create_product("product 1", over_two_thousand, 11.0, "test1@test.com") is False


def test_r4_4_create_product():
    """
    Testing R4-4: Description has to be longer than the product's title.
    """
    # Description is too short relative to title
    assert create_product("title longer than description", "24 character description", 11.0, "test1@test.com") is False


def test_r4_5_create_product():
    """
    Testing R4-5: Price has to be in range [10, 10000].
    """
    # Product cost too low
    assert create_product("product 1", "24 character description", 9.0, "test1@test.com") is False
    # product cost too high
    assert create_product("product 1", "24 character description", 10001.0, "test1@test.com") is False


def test_r4_6_create_product():
    """
    Testing R4-6: last_modified_date must be after 2021-01-02 and before 2025-01-02.
    """
    # Disallowed date - too early
    assert create_product("product 1", "24 character description", 11.0, "test1@test.com",
                          datetime.date(2020, 9, 29)) is False
    # Disallowed date - too late
    assert create_product("product 1", "24 character description", 11.0, "test1@test.com",
                          datetime.date(2020, 9, 29)) is False
    # Date in appropriate range
    assert create_product("product 1", "24 character description", 11.0, "test1@test.com",
                          datetime.date(2022, 9, 29)) is True


def test_r4_7_create_product():
    """
    Testing R4-7: The owner of the corresponding product must exist in the database.
    """
    # Seller email (notinDB@test.com) is not in the database
    assert create_product("product 2", "24 character description", 11.0, "notinDB@test.com") is False


def test_r4_8_create_product():
    """
    Testing R4-8: A user cannot create products that have the same title.
    """
    # repeat existing product name ('product 0') for user with email 'test0@test.com'
    assert create_product("product 0", "24 character description", 11.0, "test0@test.com") is False


# Products that have been inserted from create_product test cases:
# - "product 0", "24 character description", 11.0, "test0@test.com"
# - "product 1", "24 character description", 11.0, "test1@test.com", datetime.date(2022, 9, 29)
