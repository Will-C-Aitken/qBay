from qbay.models import register, login


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u0', 'test0@test.com', '123456') is True
    assert register('u0', 'test1@test.com', '123456') is True
    assert register('u1', 'test0@test.com', '123456') is False


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    user = login('test0@test.com', 123456)
    assert user is not None
    assert user.username == 'u0'

    user = login('test0@test.com', 1234567)
    assert user is None

def test_r3_update():
    '''
    Testing:

        R3-1: A user is only able to update his/her user name, shipping_address, and postal_code.
        R3-2: Shipping_address should be non-empty, alphanumeric-only, and no special characters such as !.
        R3-3: Postal code has to be a valid Canadian postal code.
        R3-4: User name follows the requirements above.

    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    result = login('test0@test.com', 123456, {'username': 'apache'})
    assert result is not False
    result = login('test0@test.com', 123456, {'username': ''})
    assert result is False

    result = login('test0@test.com', 123456, {'postal_code': 'N2P 4M1'})
    assert result is not False
    result = login('test0@test.com', 123456, {'postal_code': 'aaa 123'})
    assert result is False

    result = login('test0@test.com', 123456, {'shipping_address': '123 fake st'})
    assert result is not False
    result = login('test0@test.com', 123456, {'shipping_address': '123 fake st!'})
    assert result is False
