from qbay.models import register, login


def test_r1_1_user_register():
    '''
    Testing R1-1: Both the email and password cannot be empty
    '''

    assert register('u0', '', '123456') is False
    assert register('u0', '', '123456') is False
    assert register('u0', 'test0@test.com', '') is False
    assert register('u0', 'test0@test.com', '') is False
    assert register('u0', '', '') is False


def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified by his/her email address.
    '''

    # Being unable to add a new user with the same email ensures that all 
    # users are uniquely identified by their email
    assert register('u0', 'test0@test.com', '123456') is True
    assert register('u1', 'test0@test.com', '123456') is False

def test_r1_3_user_register():
    '''
    Testing R1-3: The email has to follow addr-spec defined in RFC 5322
    '''

    # no @
    assert register('u0', 'test0.test.com', '123456') is False
    # too many @
    assert register('u0', 'test0@test@.com', '123456') is False
    # illegal local part characters
    assert register('u0', ':;<>[]@test.com', '123456') is False
    # illegal space
    assert register('u0', 'test 0@test.com', '123456') is False
    # illegal domain characters
    assert register('u0', 'test0@*$&test_test.com', '123456') is False
    # local too short
    assert register('u0', '@test.com', '123456') is False
    # domain DNS segments too short
    assert register('u0', 'test@..', '123456') is False
    # no . in domain
    assert register('u0', 'test@test', '123456') is False
    # no . in domain
    assert register('u0', 'test@test', '123456') is False
    # local name too long
    assert register('u0',
                    '11111111111111111111111111111111111111111111111111'\
                    '11111111111111@test', '123456') is False


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    # Users with the same username can be added but not the same email.
    # test0@test.com was used in R1-2
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
