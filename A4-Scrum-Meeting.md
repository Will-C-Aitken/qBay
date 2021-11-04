### Meeting Updates for A4 Sprint

Will:
1. branch `register_ui_test`
2. Test cases completed for two register requirements using output partition
3. No
4. Finish up the test cases for register 

Max:
1. branch `create_product_blackbox_testing_input_partition`
2. Test cases completed for three create product requirements using input partition
3. Was attempting to register the same user each test case, but that fails due to requirements. Fixing now
4. Change previous test cases to login instead of register and finish cases

Alex:
1. branch `test_updateproduct`
2. One test case for update product using boundary method
3. Yes, test cases were delayed due to OS bug in code provided by instructor. Without `text=True` parameter when running subprocesses on different OS, the end of line character sequence is different which was causing tests to fail for Windows users.
4. Added parameter to subprocess to elimiate OS dependencies. Finish remaining test cases

Eissa: `output-test`
1. branch
2. No test cases
3. Yes, test cases were delayed due to OS bug in code provided by instructor. Without `text=True` parameter when running subprocesses on different OS, the end of line character sequence is different which was causing tests to fail for Windows users.
4. Write test cases now that OS bug has been fixed
