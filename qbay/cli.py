from qbay.models import login, register, create_product, \
    update_product, Product, \
    update_user


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
    user = input('Please input username: ')
    password = input('Please input password: ')
    password_twice = input('Please input the password again: ')
    if password != password_twice:
        print('Passwords entered are not the same')
    elif register(user, email, password):
        print('Registration succeeded')
    else:
        print('Registration failed')


# based on user and current products, select product and update element(s)
def update_product_page(user):
    '''
    Product Update Page: User can update information from a
                         previous product they have created.

    Returns: Product is updated assuming that title, description
             or price entered are correctly entered.
    '''

    # Find existing product
    product_title = input('Please input product title:').strip()
    product = Product.query.filter_by(seller_email=user.email,
                                      title=product_title).first()

    # Check if user's product exists
    if product is None:
        print('Error - Product does not exist. You will '
              'be taken back to the homepage.')
        return
    else:
        product_price = product.price

    while True:

        # Users can only update one parameter at a time.
        # Can choose from options below to update information.
        print()
        print('Please choose from the following options:')
        print('(1) Update title')
        print('(2) Update description')
        print('(3) Update price')
        print('(4) Return to login page')
        selection = input()
        selection = selection.strip()

        # Update title
        if selection == '1':
            new_title = input('Please enter new title: ').strip()
            update_params = {'title': new_title}

        # Update description
        elif selection == '2':
            new_description = input('Please enter new description: ').strip()
            update_params = {'description': new_description}

        # Update price
        elif selection == '3':
            new_price = input('Please enter new price: ').strip()
            try:
                new_price = float(new_price)
            except ValueError:
                print("Invalid price")
                return
            update_params = {'price': new_price}

        # Return to login
        elif selection == '4':
            break

        else:
            print('Invalid option.')

        if update_product(product_title, product_price,
                          user.email, update_params):

            if input('Product successfully updated.\n'
                     'Press Y if you would like to update '
                     'another product parameter, '
                     'or press any key to continue '
                     'to the homepage.').strip() == 'Y':
                # Return to update product page
                update_product_page(user)

            else:
                # Return to homepage
                return

        else:
            # Return to homepage
            print('Failed to update product.')
            return


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
    10-10,000 CAD). Each new product's title must be unique, and its
    description must be longer than the given title.''')

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


def update_profile_page(user):
    new_username = input('''
        Please input your new username [blank for no updates]:
    ''')
    new_postal_code = input('''
        Please input your new postal code [blank for no updates]:
    ''')
    new_shipping_address = input('''
        Please input your new shipping address [blank for no updates]:
    ''')

    updates = {}
    if len(new_username) > 0:
        updates['username'] = new_username
    if len(new_postal_code) > 0:
        updates['postal_code'] = new_postal_code
    if len(new_shipping_address) > 0:
        updates['shipping_address'] = new_shipping_address

    if update_user(user.email, user.password, updates):
        print('Update Successful!')
    else:
        print('Update Failed')
    return
