from qbay.models import login, register, create_product


def home_page(user):
    """
    Home page user is greeted with after login. User object is passed
    in as a parameter, so that the User's attributes and products can
    be accessed for update/add operations.
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
            create_product_page(user)

        # Update product
        elif selection == '2':
            update_product_page(user)
            
        # Update profile
        elif selection == '3':
            update_profile_page(user)
            
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


def create_product_page(user):
    """
    Product creation page, where a user can add a new sellable product
    to their account.

    :return: None, but a product will be created (assuming product
    details are entered correctly)
    """

    print('''
    You will now be prompted to enter information about your new product. 
    Each product requires [1] a title (<80 alphanumeric characters), [2] 
    a description (within 20-2000 characters), and [3] a price (within 
    10-10,000 CAD). Furthermore, each new product's name must be unique.
    ''')
    title = input("Please enter product title: ").strip()
    description = input("Please enter product's description: ").strip()
    price = input("Please enter product's price: ").strip()
    try:
        price = float(price)
    except ValueError:
        print("Invalid price")
        return
    if create_product(title, description, price, user.email):
        print("Product successfully created")
        return
    else:
        print("Product creation failed")
        return


def update_product_page(user):
    return


def update_profile_page(user):
    return
