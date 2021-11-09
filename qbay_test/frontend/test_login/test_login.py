from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


def single_test(name):
    '''
    This implements a series of blackbox
    tests for login functionality. Note that
    there is an
    All cases are tested here, this includes
    but not limited to:
        login non-existant user
        login failure for user
        login logout login
        login logout login fail
        login logout login different user
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        '{}.in'.format(name)))
    expected_out = open(current_folder.joinpath(
        '{}.out'.format(name))).read()

    print(expected_out)

    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True
    ).stdout

    assert output.strip() == expected_out.strip()


def test_all():
    tests = {'test_login', }
    for test in tests:
        single_test(test)
