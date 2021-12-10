# from os import popen
from pathlib import Path
from qbay.models import *
import subprocess

# Set the current folder
current_folder = Path(__file__).parent

# Creating two Users for testing of order functionality
register("OrderUser1",
         "order_user1@qbay.com",
         "Password99@")

register("OrderUser2",
         "order_user2@qbay.com",
         "Password99@")

# Create four products for testing of order functionality
create_product("order product1",
               "24 character description",
               11.0, "order_user1@qbay.com",
               datetime.date(2022, 9, 29))

create_product("order product2",
               "24 character description",
               101.0, "order_user2@qbay.com",
               datetime.date(2022, 9, 29))

create_product("order product3",
               "24 character description",
               11.0, "order_user2@qbay.com",
               datetime.date(2022, 9, 29))

create_product("order product4",
               "24 character description",
               11.0, "order_user2@qbay.com",
               datetime.date(2022, 9, 29))


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


def test_buyer_not_seller():
    """
    Blackbox input partition test for "user cannot place
    an order for his/her products" requirement of order().
    There are two partitions:

    Case 1: Prospective buyer is seller (expect failure)
    Case 2: Prospective buyer is not seller (expect success)
    """
    # list of input/output files used to test each partition
    input_files = ['buyer_is_seller.in',
                   'buyer_not_seller.in']
    output_files = ['buyer_is_seller.out',
                    'buyer_not_seller.out']
    for i in range(0, 2):
        compare_input_output(input_files[i], output_files[i])


def test_price_vs_balance():
    """
    Blackbox input partition test for "user cannot place an
    order that costs more than his/her balance" requirement
    of order(). There are two partitions:

    Case 1: User balance is less than cost (expect failure)
    Case 2: User balance is great than cost (expect success)
    """
    # list of input/output files used to test each partition
    input_files = ['price_over_balance.in',
                   'price_under_balance.in']
    output_files = ['price_over_balance.out',
                    'price_under_balance.out']
    for i in range(0, 2):
        compare_input_output(input_files[i], output_files[i])


def test_sold_products_hidden():
    """
    Tests that a previously purchased product does not appear
    in the lists of products available for sale.
    """
    input_file = "sold_products_hidden.in"
    output_file = "sold_products_hidden.out"
    compare_input_output(input_file, output_file)


def test_sold_visible_for_seller():
    """
    Tests that a User can view the products that they have sold.
    """
    input_file = "sold_visible_for_seller.in"
    output_file = "sold_visible_for_seller.out"
    compare_input_output(input_file, output_file)


