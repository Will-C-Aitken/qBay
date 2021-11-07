# from os import popen
from pathlib import Path
from qbay.models import *
import subprocess

# Set the current folder
current_folder = Path(__file__).parent

# Creating a user object for frontend testing
register("TestUser",
         "create_product_test@qbay.com",
         "Password99@")


# Helper function called in each testing block
def compare_input_output(input_file, output_file):
    """
    A function that compares the output generated from
    running the qbay frontend (on a given an input file),
    to the expected output found in a text file.
    Parameters:
        input_file (string):    file with expected input
        output_file (string):   file with expected output
    """
    expected_in = open(current_folder.joinpath(
        'input_output/' + input_file))
    expected_out = open(current_folder.joinpath(
        'input_output/' + output_file)).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout
    assert output.strip() == expected_out.strip()


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


# ----- TEST 1: TITLE ALPHANUM/NON-ALPHANUM (R4-1) ------ #
def test_cp_title_alphanumeric():
    """
    There are two partitions:
    Case 1: title is alphanumeric (expect
            successful product creation)
    Case 2: title is non-alphanumeric (expect
            product creation to fail
    """
    # list of input/output files used to test each partition
    input_files = ['t1a_title_alphanumeric.in',
                   't1b_title_not_alphanumeric.in']
    output_files = ['product_creation_success.out',
                    'product_creation_fail.out']
    for i in range(0, 2):
        compare_input_output(input_files[i], output_files[i])


# ----------- TEST 2: TITLE LENGTH (R4-2) ------------ #
def test_cp_title_length():
    """
    There are two partitions:
    Case 1: title length <= 80 (expect
            successful product creation)
    Case 2: title length > 80 (expect
            product creation to fail
    """
    # list of input/output files used to test each partition
    input_files = ['t2a_title_within_80.in',
                   't2b_title_over_80.in']
    output_files = ['product_creation_success.out',
                    'product_creation_fail.out']
    for i in range(0, 2):
        compare_input_output(input_files[i], output_files[i])


# ------ PARTITION 3: DESCRIPTION LENGTH (R4-3) ------- #
def test_cp_desc_length():
    """
    There are three partitions:
    Case 1: description length < 20 (expect
            product creation to fail)
    Case 2: description length in bounds 20 <= x <= 2000
            (expect successful product creation)
    Case 3: description length > 2000 (expect
            product creation to fail)
    """
    # list of input/output files used to test each partition
    input_files = ['t3a_desc_under_20.in',
                   't3b_desc_within_20_2000.in',
                   't3c_desc_over_2000.in']
    output_files = ['product_creation_fail.out',
                    'product_creation_success.out',
                    'product_creation_fail.out']
    for i in range(0, 3):
        compare_input_output(input_files[i], output_files[i])


# ---- TEST 4: DESCRIPTION LENGTH RELATIVE TO TITLE (R4-4) ---- #
def test_cp_description_vs_title():
    """
    There are two partitions:
    Case 1: description longer than title (expect
            product creation to fail
    Case 2: description shorter than title (expect
            successful product creation)
    """
    # list of input/output files used to test each partition
    input_files = ['t4a_desc_gt_title.in',
                   't4b_desc_lt_title.in']
    output_files = ['product_creation_success.out',
                    'product_creation_fail.out']
    for i in range(0, 2):
        compare_input_output(input_files[i], output_files[i])


# ----------------  TEST 5: PRICE (R4-5) ---------------- #
def test_cp_price_under_10():
    """
    There are 3 partitions:
    Case 1: Price under 10$ lower bound (expect product
            creation to fail)
    Case 2: Price within 10-10000$ bound (expect successful
            product creation)
    Case 3: Price over 10000$ upper bound (expect product
            creation to fail)
    """
    # list of input/output files used to test each partition
    input_files = ['t5a_price_under_10.in',
                   't5b_price_within_10_10000.in',
                   't5c_price_over_10000.in']
    output_files = ['product_creation_fail.out',
                    'product_creation_success.out',
                    'product_creation_fail.out']
    for i in range(0, 3):
        compare_input_output(input_files[i], output_files[i])


# -------- TEST 6: PRODUCT IN/NOT IN DB  (R4-8) -------- #
def test_cp_product_is_duplicate():
    """
    There are 2 partitions:
    Case 1: Product is  already in the database
            (expect product creation to fail)
    Case 2: Product is not already in the database
            (expect successful product creation)
    """
    # list of input/output files used to test each partition
    input_files = ['t6a_product_is_duplicate.in',
                   't6b_product_not_duplicate.in']
    output_files = ['product_creation_fail.out',
                    'product_creation_success.out']
    for i in range(0, 2):
        compare_input_output(input_files[i], output_files[i])


# Date field is not accessible to user, so we cannot partition
# date input on the frontend. But we can verify that the
# products created through the frontend are within accepted
# range.

# ------------ TEST 7: CHECK DATES  (R4-6) ------------ #
def test_cp_date():
    """
    Tests to see whether the products created through the
    frontend all have dates within the allowed range
    (2021.01.02 - 2025.01.02).
    """


# Product's "seller email" field is automatically set upon
# creation, so we cannot partition it based on user input.
# However, we can verify that the products created via
# the frontend all have seller emails attached.

# ------------ TEST 8: CHECK SELLER EMAIL  (R4-7) ------------ #
def test_cp_user_exists():
    """
    Tests that the products created through the frontend
    all have a seller email attribute.
    """
    all_products_in_db = Product.filter_by().all()

