import os
import simplejson as json
from oauth2flow import OAuth2

def clear_screen():
    print("\n" * os.get_terminal_size().lines)
    print("\x1b[2J\x1b[1;1H")

def user_info(auth:OAuth2,access_token:str) -> dict:
    user = auth.user_info(access_token)
    return user

if __name__ == "__main__":
    """user info a token"""
    clear_screen()
    auth = OAuth2()
    access_token = input("Enter access_token: ")
    print("")
    user = user_info(auth,access_token)
    formatted = json.dumps(user, indent=4)
    print(formatted)