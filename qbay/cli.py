from qbay.models import *


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
        print('(5) View products available for purchase')
        print('(6) View products you sold')
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

        # View available products
        elif selection == '5':
            available_products_page(user)

        # View products you sold
        elif selection == '6':
            sold_products_page(user)

        else:
            print('Invalid option')


def login_page():
    """
    Login page prompts user for their email and password and returns the
    result of the attempted login.
    """

    email = input('Please input email: ')
    password = input('Please input password: ')
    return login(email, password)


def register_page():
    """
    Registration page prompts user for the required registration information
    and returns the result of the attempted registration.
    """

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
    description must be longer than the given title.\n''')

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


def available_products_page(user):
    """
    Available products page, where a user can view products that
    are still available for purchase, and then navigate to the
    order page.
    """
    # Get available products
    available_products = get_avail_products()

    # Print the list of products
    print("Products available for purchase.\n")
    for i in range(0, len(available_products)):
        print(str(i + 1) + ". " + available_products[i].title +
              " ($" + str(available_products[i].price) + ")")

    print("\nTo view a product, enter the number to its left.")
    print("Or hit enter (without input) to return to the main menu.")
    # User selection
    selection = input()
    selection = selection.strip()

    # Get product from list, and navigate to order page
    if selection.isdigit() and 1 <= int(selection) <= len(available_products):
        product = available_products[int(selection) - 1]
        order_page(user, product)
    else:
        print("Returning to main menu.")
        return


def order_page(user, product):
    """
    Order page, where a User can see the detailed information about
    a product, and place an order.
    """
    # Print product details
    print("Title: " + product.title)
    print("Price: " + str(product.price))
    print("Seller: " + product.seller_email)
    print("Description: " + product.description)

    print("\nTo order this product, enter 'order'.")
    print("Or hit enter (without input) to return to the main menu.")
    # Get User input
    choice = input()
    choice = choice.strip()

    # Place order
    if choice.lower() == "order":
        result = order(product.title,
                       product.seller_email,
                       user.email)
        if result is True:
            print("Product successfully ordered!")
            print("Your new balance is " + str(user.balance))
            return
        else:
            print("Order was unsuccessful.")
            return

    else:
        print("returning to main menu.")
        return


def sold_products_page(user):
    """
    Page where a User can view the products that they sold.
    Note that Users can only ever see their own sold products.
    """
    sold_products = get_sold_products(user.email)
    print("Your sold products:\n")

    # Display sold products
    for i in range(0, len(sold_products)):
        print(str(i + 1) + ". " + sold_products[i].title +
              " ($" + str(sold_products[i].price) + ")")

    print("\nTo view a product's details, enter the number to its left.")
    print("Or hit enter (without input) to return to the main menu.")
    # Get user input
    selection = input()
    selection = selection.strip()
    if selection.isdigit() and 1 <= int(selection) <= len(sold_products):
        product = sold_products[int(selection) - 1]
        print("Title: " + product.title)
        print("Price: " + str(product.price))
        print("Seller: " + product.seller_email)
        print("Description: " + product.description)
        escape = input("\nHit enter (without input) to return to the "
                       "main menu.")
        return
    else:
        return







