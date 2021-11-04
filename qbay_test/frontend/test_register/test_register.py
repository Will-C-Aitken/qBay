from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent

NUM_REQS = 10

def test_register():

    expected_out = open(current_folder.joinpath("test_register.out")).read()

    #for i in range(1, NUM_REQS+1):
    for i in range(1, 2):
        # read expected in/out
        expected_in = open(current_folder.joinpath("test_register_" + str(i)
                           + ".in")) 

        # pip the input
        output = subprocess.run(
            ['python', '-m', 'qbay'],
            stdin=expected_in,
            capture_output=True,
            text=True
        ).stdout.decode()
        
        assert output.strip() == expected_out.strip()
