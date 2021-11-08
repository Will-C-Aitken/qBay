# Review_and_Retrospect

## 1. Register User Tests (Output partition)
Located in qbay_test/frontend/test_register/test_register.py

### Test functions
test_resigter()

## 2. Product Creation Tests (Input partition)
Located in qbay_test/frontend/test_create_product/test_create_product.py

### Test functions
test_cp_title_alphanumeric()
test_cp_title_length()
test_cp_desc_length()
test_cp_description_vs_title()
test_cp_price_under_10()
test_cp_product_is_duplicate()

### Extra test functions (not input partition)
These tests were included to test the extra requirements not accessible from the frontend (R4-6, R4-7)
test_cp_date()
test_cp_user_exists()

## 3. Product Update Tests (Boundary testing)
Located in qbay_test/frontend/test_updateproduct/test_updateproduct.py

### Test functions
test_up_title_alphanumeric()
test_up_title_non_alphanumeric()
test_up_title_no_chars()
test_up_title_in_range_chars()
test_up_title_max_range()
test_up_description_min_range()
test_up_description_mid_range()
test_up_description_max_range()
test_up_description_overmax_range()
test_up_desc_equals_title()
test_up_desc_less_than_title()
test_up_desc_larger_than_title()
test_up_price_under_min()
test_up_price_min()
test_up_price_max()
test_up_price_over_max()
test_up_price_decrease()
test_up_price_unchanged()
test_up_price_decrease()

