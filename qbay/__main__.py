from qbay import *
from qbay.cli import login_page, register_page, home_page


def main():
    while True:

        # Upon starting app, user can login, register or quit
        selection = input('Welcome. Please type 1 to login, 2 to register, ' 
                          'or 3 to quit\n')
        selection = selection.strip()

        # Login
        if selection == '1':
            user = login_page()
            if user:
                print(f'Welcome {user.username}')
                home_page()
            else:
                print('Login failed')

        # Register
        elif selection == '2':
            register_page()

        # Quit
        elif selection == '3':
            break

        else:
            print('Invalid option')


if __name__ == '__main__':
    main()
