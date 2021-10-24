from qbay.models import login, register, update_product, Product


def home_page(user):
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
            update_product_page(user)
            
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


def update_product_page(user):
    '''
    Product Update Page: User can update information from a
                         previous product they have created.

    Returns: Product is updated assuming that title, description
             or price entered are correctly entered.
    '''

    # Find existing product
    product = Product.query.filter_by(seller_email=user.email).first()

    # Check if user's product exists
    if product is not None:
        product_title = product.title
        product_price = product.price
    else:
        print('Error - Product does not exist. You will '
              'be taken back to the homepage.')
        return

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

            if input('Product successfully updated. \n'
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


def update_profile_page():
    return
