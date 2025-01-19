import os
import simplejson as json
from oauth2flow import OAuth2

def clear_screen():
    print("\n" * os.get_terminal_size().lines)
    print("\x1b[2J\x1b[1;1H")

def introspect_token(auth:OAuth2,access_token:str) -> dict:
    introspect = auth.introspect_token(access_token)
    return introspect

if __name__ == "__main__":
    """Introspect a token"""
    clear_screen()
    auth = OAuth2()
    access_token = input("Enter access_token: ")
    print("")
    introspect = introspect_token(auth,access_token)
    formatted = json.dumps(introspect.get('resource_access'), indent=4)
    print(formatted)