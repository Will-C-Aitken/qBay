from qbay.models import login

from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


def test_register():
    '''
    Testing register function requirements specified in A2, this time from the
    frontend.

    R1-1 - R1-7 are tested with the output partition blackbox method. The three
    possible outputs for registering are strings that correspond to FAILURE,
    SUCCESS, and ERROR in typing password again. The sequence of console 
    outputs corresponding to these outputs are in order in 'test_register.out'.
    For each register requirement, inputs that will cause each of the possible
    outputs to occur are in 'test_register_i.in', where i is [1-7] describing 
    which requirement it covers. The program is run with each set of inputs and
    tested to see if the output matches the static expectation.

    Blackbox output partition does not make sense to test requirements R1-8 -
    R1-10 since any valid registration input should yield the expected results.
    Instead, a user registered with the UI is tested to ensure that these
    requirements are still met.
    '''

    expected_out = open(current_folder.joinpath("test_register.out")).read()

    # Register requirements R1-1 through R1-7
    for i in range(1, 8):
        # read expected in/out
        expected_in = open(current_folder.joinpath("test_register_" + str(i)
                           + ".in")) 

        # pip the input
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
            text=True
        ).stdout
        
        assert output.strip() == expected_out.strip()

    # Verify R1-8 through R1-10 are still covered after registering through
    # frontend
    user = login('ui-test7@test.com', 'Legalpass!7')

    # R1-8: Shipping address is empty at the time of registration
    assert user.shipping_address == ''

    # R1-9: Postal code is empty at the time of registration
    assert user.postal_code == ''

    # R1-10: Balance should be initialized as 100 at the time of registration
    assert user.balance == 100.00
