from qbay.models import register, login


def test_r1_1_user_register():
    '''
    Testing R1-1: Both the email and password cannot be empty
    '''

    assert register('u0', '', 'Legalpass!') is False
    assert register('u0', '', 'Legalpass!') is False
    assert register('u0', 'test0@test.com', '') is False
    assert register('u0', 'test0@test.com', '') is False
    assert register('u0', '', '') is False


def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified by his/her email address.
    '''

    # Being unable to add a new user with the same email ensures that all 
    # users are uniquely identified by their email
    assert register('u0', 'test0@test.com', 'Legalpass!') is True
    assert register('u1', 'test0@test.com', 'Legalpass!') is False


def test_r1_3_user_register():
    '''
    Testing R1-3: The email has to follow addr-spec defined in RFC 5322
    '''

    # no @
    assert register('u0', 'test0.test.com', 'Legalpass!') is False
    # too many @
    assert register('u0', 'test0@test@.com', 'Legalpass!') is False
    # illegal local part characters
    assert register('u0', ':;<>[]@test.com', 'Legalpass!') is False
    # illegal space
    assert register('u0', 'test 0@test.com', 'Legalpass!') is False
    # illegal domain characters
    assert register('u0', 'test0@*$&test_test.com', 'Legalpass!') is False
    # local too short
    assert register('u0', '@test.com', 'Legalpass!') is False
    # domain DNS segments too short
    assert register('u0', 'test@..', 'Legalpass!') is False
    # no . in domain
    assert register('u0', 'test@test', 'Legalpass!') is False
    # no . in domain
    assert register('u0', 'test@test', 'Legalpass!') is False
    # local name too long
    assert register('u0',
                    ('11111111111111111111111111111111111111111111111111'
                     '11111111111111@test'), 'Legalpass!') is False


def test_r1_4_user_register():                    
    '''
    Testing R1-4: Password has to meet the required complexity: minimum length
    6, ar least one upper case, at least one lower case, and at least one
    special character.
    '''

    # Length 5
    assert register('u0', 'test0.test.com', 'Lega!') is False
    # No upper case
    assert register('u0', 'test0.test.com', 'legalpass!') is False
    # No lower case
    assert register('u0', 'test0.test.com', 'LEGALPASS!') is False
    # No special character 
    assert register('u0', 'test0.test.com', 'legalpass') is False


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    # Users with the same username can be added but not the same email.
    # test0@test.com was used in R1-2
    assert register('u0', 'test1@test.com', 'Legalpass!') is True
    assert register('u1', 'test0@test.com', 'Legalpass!') is False


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    user = login('test0@test.com', 'Legalpass!')
    assert user is not None
    assert user.username == 'u0'

    user = login('test0@test.com', 'Unusedpass!')
    assert user is None
