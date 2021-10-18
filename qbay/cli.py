from qbay.models import login, register


def home_page():
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
            update_product_page()
            
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


def create_product_page():
    return


def update_product_page():
    return


def update_profile_page():
    return
