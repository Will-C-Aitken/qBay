from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


# read expected in/out
expected_in = open(current_folder.joinpath(
    'test_user_update.in'))
expected_out = open(current_folder.joinpath(
    'test_user_update.out')).read()

print(expected_out)


def test_login():
    """
    The rest of this document contains front-end tests for
    user profile updates.

    A series of input partition black-box tests are implemented.
    This single test contains all permutations for user updates.
    This includes input partitions:
        no changes
        all 3 successfull changes
        invalid changes for each parameter
    """

    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True
    ).stdout

    assert output.strip() == expected_out.strip()
