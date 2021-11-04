# from os import popen
from pathlib import Path
import subprocess

# Set the current folder
current_folder = Path(__file__).parent

"""
What follows is a series of input partition black-box tests. 
For each test, non-partitioned variables are set to a legal
value. For instance, when partitioning the title variable--e.g.
title is either (i) alphanumeric or (ii) non-alphanumeric--
other variables, such as price and description, will be 
given legal values. 
"""


# PARTITION 1: TITLE ALPHANUMERIC/NON-ALPHANUMERIC
def test_cp_title_alphanumeric():
    """
    Case A: Title is alphanumeric.
    Expect successful product creation
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/title_alphanumeric.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/title_alphanumeric.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_title_not_alphanumeric():
    """
    Case B: title is not alphanumeric
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/title_not_alphanumeric.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/title_not_alphanumeric.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


# More tests go here . . .


# PARTITION 3: DESCRIPTION LENGTH
def test_cp_desc_under_20():
    """
    Case A: description under 20 characters
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/desc_under_20.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/desc_under_20.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_desc_within_20_2000():
    """
    Case B: Description with the accepted bounds:
    20-2000
    Expect successful product creation
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/desc_within_20_2000.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/desc_within_20_2000.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_desc_over_2000():
    """
    Case C: Description over 20000 Limit
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/desc_over_2000.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/desc_over_2000.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


# More tests go here . . .


# PARTITION 5: PRICE
def test_cp_price_under_10():
    """
    Case A: Price under 10$ lower bound
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/price_under_10.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/price_under_10.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_price_within_10_1000():
    """
    Case B: Price within 10-10000$ bound
    Expect successful product creation
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/price_within_10_10000.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/price_within_10_10000.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_price_over_10000():
    """
    Case C: Price over 10000$ upper bound
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/price_over_10000.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/price_over_10000.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()