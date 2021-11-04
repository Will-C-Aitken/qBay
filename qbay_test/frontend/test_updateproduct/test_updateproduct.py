from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent

'''
The tests below cover the same requirements as "create product"
as well as additional quantitative requirements. All tests are 
using the Black-Box Boundary Testing technique.

The boundary tests below test extreme ends of each requirement 
(e.g. minimum, middle/nominal value, maximum).
'''


# ------- BOUNDARY TEST 1: Alphanumeric vs. Non-Alphanumeric -------

'''
The title of the product is alphanumeric-only,
and spaces cannot appear as a prefix or a suffix.
'''


def test_up_title_alphanumeric():
    '''
    Case A: Title is alphanumeric (MAX Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_alphanumeric.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_alphanumeric.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_title_non_alphanumeric():
    '''
    Case B: Title is not alphanumeric (MIN Boundary)
    Expect product to fail.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_non_alphanumeric.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_non_alphanumeric.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# ----------------- BOUNDARY TEST 2: Title Length -------------------
    '''
    The title of the product is no longer than 80 characters.
    '''


def test_up_title_no_chars():
    '''
    Case A: Title is 1 character long (MIN Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_title_nochars.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_title_nochars.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_title_in_range_chars():
    '''
    Case B: Title is between 0-80 characters (MID Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_title_in_range_chars.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_title_in_range_chars.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_title_max_range():
    '''
    Case C: Title is exactly 80 characters (MAX Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_title_max_range.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_title_max_range.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# ----------------- BOUNDARY TEST 3: Description Length -------------------
    '''
    Description must have a minimum length 20 characters and
    a maximum length of 2000 characters.
    '''


def test_up_description_min_range():
    '''
    Case A: Description is exactly 20 characters (MIN Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_description_min_range.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_description_min_range.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_description_mid_range():
    '''
    Case B: Description is between 20-2000 characters (MID Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_description_mid_range.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_description_mid_range.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# 3c) Exactly 2000 chars (MAX range)
def test_up_description_max_range():
    '''
    Case C: Description is exactly 2000 characters (MAX Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_description_max_range.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_description_max_range.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_description_overmax_range():
    '''
    Case D: Description is just over 2000 characters (MAX+ Boundary)
    Expect product to fail.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_description_overmax_range.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_description_overmax_range.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# ------- BOUNDARY TEST 4: Description vs. Title Length -------
    '''
    Description has to be longer than the product's title.
    '''


def test_up_desc_equals_title():
    '''
    Case A: Title and description are of equal length (MIN Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_desc_equals_title.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_desc_equals_title.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# 4b) Description length is JUST under title's length (MIN- range)
def test_up_desc_less_than_title():
    '''
    Case B: Description length is just under title's length (MIN- Boundary)
    Expect product to fail.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_desc_less_than_title.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_desc_less_than_title.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_desc_larger_than_title():
    '''
    Case C: Description length is just over title's length (MAX Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_desc_larger_than_title.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_desc_larger_than_title.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# ----------------- BOUNDARY TEST 5: Price Range -------------------
    """
    Price has to be in range [10, 10000].
    """


# 5a) Price is JUST under 10 (MIN- range)
def test_up_price_under_min():
    '''
    Case A: Price is just under 10 (MIN- Boundary)
    Expect product to fail.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_under_min.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_under_min.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_price_min():
    '''
    Case B: Price is updated to 11 (MIN Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_min.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_min.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


def test_up_price_max():
    '''
    Case C: Price is updated to 10000 (MAX Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_max.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_max.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# 5d) Price is JUST over 10000 (MAX+ range)
def test_up_price_over_max():
    '''
    Case D: Price is just over 10000 (MAX+ Boundary)
    Expect product to fail.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_over_max.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_over_max.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# ----------------- BOUNDARY TEST 6: Price Increase -------------------
    """
    Price can only be increased but cannot be decreased.
    """


# 6a) Price is decrease by 1 (MIN range)
def test_up_price_decrease():
    '''
    Case A: Price is decrease by 1 (MIN Boundary)
    Expect product to fail.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_decrease.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_decrease.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# 6b) Price is unchanged (MID range)
def test_up_price_unchanged():
    '''
    Case B: Price is unchanged (MID Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_unchanged.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_unchanged.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()


# 6c) Price is increased (MAX range)
def test_up_price_decrease():
    '''
    Case C: Price is increased (MAX Boundary)
    Expect product to succeed.
    '''

    # read expected in/out
    expected_in = open(current_folder.joinpath(
        'test_up_price_decrease.in'))
    expected_out = open(current_folder.joinpath(
        'test_up_price_decrease.out')).read()
    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
        text=True,
    ).stdout

    print('outputs:', output)

    assert output.strip() == expected_out.strip()