# from os import popen
from pathlib import Path
import subprocess

# Set the current folder
current_folder = Path(__file__).parent

"""
This document contains front-end tests for the 
create product function.

What follows is a series of input partition black-box tests. 
For each test, non-partitioned variables are set to a legal
value. For instance, when partitioning the title variable--e.g.
title is either (i) alphanumeric or (ii) non-alphanumeric--
other variables, such as price and description, will be 
given legal values. 
"""


# -- PARTITION 1: TITLE ALPHANUM/NON-ALPHANUM --- #
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


# ------ PARTITION 2: TITLE LENGTH ------- #
def test_cp_title_within_80():
    """
    Case A: title length is less than
    (or equal to) 80 characters
    Expect successful product creation
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/title_within_80.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/title_within_80.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_title_over_80():
    """
    Case B: title length is over 80
    characters
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/title_over_80.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/title_over_80.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


# ------ PARTITION 3: DESCRIPTION LENGTH ------- #
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
    Case B: Description within the accepted bounds:
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


# - PARTITION 4: DESCRIPTION LENGTH RELATIVE TO TITLE - #
def test_cp_description_longer_than_title():
    """
    Case A: Description is longer than title
    Expect successful product creation
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/desc_gt_title.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/desc_gt_title.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_description_shorter_than_title():
    """
    Case A: Description is shorter than title
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/desc_lt_title.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/desc_lt_title.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


# --------- PARTITION 5: PRICE --------- #
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


# ------ PARTITION 6: PRODUCT IN/NOT IN DB  ------ #
def test_cp_product_is_duplicate():
    """
    Case B: Product is  already in the database
    Expect product creation to fail
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/product_is_duplicate.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/product_is_duplicate.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()


def test_cp_product_not_duplicate():
    """
    Case B: Product is not already in the database
    Expect successful product creation
    """
    # Fetch the expected input/output
    expected_in = open(current_folder.joinpath(
        'input_output/product_not_duplicate.in'))
    expected_out = open(current_folder.joinpath(
        'input_output/product_not_duplicate.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    print('outputs', output)
    assert output.strip() == expected_out.strip()
