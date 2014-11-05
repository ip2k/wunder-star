'''Utility for storing a wunderlist token.'''

import json
import getpass
import os.path

from wunderpy import Wunderlist


def setup():
    '''Prompt the user for a wunderlist login, authenticate
    and save the token.
    '''

    def prompt_login():
        '''Ask the user for login info.
        Returns a tuple with email, password'''

        email = raw_input("Input your Wunderlist username (email): ")
        password = getpass.getpass(prompt="Input your Wunderlist password: ")
        print("Logging in...")
        wunderlist = Wunderlist()
        try:
            wunderlist.login(email, password)
        except:
            again = raw_input("Login failed, try again? (y/n) ")
            if again == "y" or again == "Y":
                prompt_login()
            else:
                exit()

        return wunderlist

    print("It appears this is your first time using wunderpy "
          "on the command line.")
    print("All that's needed is a one-time login with Wunderlist.\n")

    wunderlist = prompt_login()
    token = wunderlist.token
    save_token(token)


def save_token(token):
    '''Save a token to the config file.'''

    with open(os.path.expanduser("~/.wunderpyrc"), "w") as store:
        json.dump({"token": token}, store)


def get_token():
    '''Get the token from the config file'''

    with open(os.path.expanduser("~/.wunderpyrc"), "r") as store:
        token = json.load(store)
        return token["token"]
