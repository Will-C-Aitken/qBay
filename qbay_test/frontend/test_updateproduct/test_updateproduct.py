from os import popen
from pathlib import Path
from qbay_test.conftest import pytest_sessionstart

import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


# read expected in/out

'''
Testing R5-1: Can update all attributes of the product except owner_email \
         and last_modified_date.
'''
expected_in_r5_1 = open(current_folder.joinpath(
    'test_updateproduct.in_r5_1'))
expected_out_r5_1 = open(current_folder.joinpath(
    'test_updateproduct.out_r5_1')).read()
expected_in_in_r5_2 = open(current_folder.joinpath(
    'test_updateproduct.in_r5_2'))
expected_out_r5_2 = open(current_folder.joinpath(
    'test_updateproduct.out_r5_2')).read()

print(expected_out_r5_1)
print(expected_out_r5_2)


# Using Black-Box Boundary Testing
def test_updateproduct():
    """capsys -- object created by pytest to
    capture stdout and stderr"""

    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()
