from qbay.models import register, login, update


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


def test_r3_update():
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

    result = update('test0@test.com', 'Legalpass!', {'username': 'apache'})
    assert result is not False
    result = update('test0@test.com', 'Legalpass!', {'username': ''})
    assert result is False

    result = update('test0@test.com', 'Legalpass!', {'postal_code': 'N2P 4M1'})
    assert result is not False
    result = update('test0@test.com', 'Legalpass!', {'postal_code': 'aaa 123'})
    assert result is False

    result = update('test0@test.com', 'Legalpass!',
                    {'shipping_address': '123 fake st'})
    assert result is not False
    result = update('test0@test.com', 'Legalpass!',
                    {'shipping_address': '123 fake st!'})
    assert result is False
