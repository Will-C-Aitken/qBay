from qbay.models import login, register, update_product, Product


def home_page(user_email):
    """
    Home page user is greeted with after login
    """

    while True:

        # Upon signing in, user can create or update a product, update their
        # profile or exit to login page
        print()
        print('Please choose from the following options:')
        print('(1) Create product')
        print('(2) Update product')
        print('(3) Update profile')
        print('(4) Return to login page')
        selection = input()
        selection = selection.strip()

        # Create product
        if selection == '1':
            create_product_page()

        # Update product
        elif selection == '2':
            update_product_page(user_email)
            
        # Update profile
        elif selection == '3':
            update_profile_page()
            
        # Return to login
        elif selection == '4':
            break
            
        else:
            print('Invalid option')


def login_page():
    email = input('Please input email: ')
    password = input('Please input password: ')
    return login(email, password)


def register_page():
    email = input('Please input email: ')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')
    if password != password_twice:
        print('Passwords entered are not the same')
    elif register('default name', email, password):
        print('Registration succeeded')
    else:
        print('Registration failed')


# based on user and current products, select product and update element(s)
def create_product_page():
    return


def update_product_page(user_email):
    product_title = Product(seller_email=user_email).title
    product_price = Product(seller_email=user_email).price

    new_title = input('Please enter new title: ')
    new_description = input('Please enter new description: ')
    new_price = input('Please enter new price: ')
    update_params = {new_title, new_description, new_price}

    if update_product(product_title, product_price, user_email, update_params):
        print('Product successfully updated.')
    else:
        print('Failed to update.')


def update_profile_page():
    return
