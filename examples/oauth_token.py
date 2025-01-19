import os
import getpass
import simplejson as json
from oauth2flow import OAuth2


def clear_screen():
    print("\n" * os.get_terminal_size().lines)
    print("\x1b[2J\x1b[1;1H")

def token_client_credentials(auth:OAuth2,scope:str) -> str:
    token_response = auth.token_client_credentials(scope)
    if token_response.get('access_token'):
        return token_response.get('access_token')
    return json.dumps(token_response, indent=4)

def token_client_password(auth:OAuth2,username:str,password:str,scope:str) -> str:
    token_response = auth.token_password(username,password,scope)
    if token_response.get('access_token'):
        return token_response.get('access_token')
    return json.dumps(token_response, indent=4)

if __name__ == "__main__":
    """Create a token"""
    clear_screen()
    print("Criando um token ...")
    auth = OAuth2()
    type: str = input("Enter type of(client-credentials / password) : ")
    if type == 'client-credentials':
        access_token = token_client_credentials(auth,scope='openid')
        print("")
    elif type == 'password':
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        access_token = token_client_password(auth,username,password,scope='openid')
        print("")
    else:
        print("Invalid type")
        exit()
    print(access_token)
    print("")
