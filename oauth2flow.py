import os
import requests
from attrs import define, field

@define
class OAuth2:
    """Class to handle flow OAuth2.0

    Flow OAuth2.0 app end generation token for client-credentials and password:
    includes Environment Variables in the .env file:
    Attributes:
        client_id: str [required]
        client_secret: str [required]
        redirect_uri: str [required]
        authorization_base: str [required]
        token_url: str [required]
        introspection_url: str [required]
        user_info_url: str [required]
    """
    client_id: str = field(default=os.environ.get('CLIENT_ID'))
    client_secret: str = os.environ.get('CLIENT_SECRET')
    redirect_uri: str = os.environ.get('REDIRECT_URI')
    authorization_base: str = os.environ.get('AUTHORIZATION_BASE_URL')
    token_url: str = os.environ.get('TOKEN_URL')
    introspection_url:str = os.environ.get('INTROSPECTION_URL')
    user_info_url:str = os.environ.get('USERINFO_URL')

    def token_client_credentials(self, scope=''):
        """Get access token using client-credentials flow"""
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': scope,
        }
        if scope == '':
            data.pop('scope')
        response = requests.post(self.token_url, data=data)
        if response.status_code != 200:
            return {'status_code': response.status_code,'error': response.reason, 'content': response.content}
        return response.json()
    
    def token_password(self, username, password, scope=''):
        """Get access token using password flow"""
        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': username,
            'password': password,
            'scope': scope,
        }
        if scope == '':
            data.pop('scope')
        response = requests.post(self.token_url, data=data)
        if response.status_code != 200:
            return {'status_code': response.status_code,'error': response.reason, 'content': response.content}
        return response.json()
      
    def introspect_token(self,access_token):
        """Get the token information"""
        data = {
            'token': access_token,
        }
        response = requests.post(self.introspection_url, data=data, auth=(self.client_id, self.client_secret))
        if response.status_code != 200 or not response.json().get('active'):
            return {'status_code': response.status_code,'error': response.reason, 'content': response.content}
        return response.json()

    def token_validation(self, access_token):
        """Validate the token"""
        data_introspect = self.introspect_token(access_token)
        return data_introspect
    
    def token_roles(self, access_token):
        """Get the roles of the token"""
        roles = self.introspect_token(access_token)
        if roles.get('active'):
            return roles.get('resource_access')
        else:
            return roles

    def user_info(self, access_token):
        """Get user information"""
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(self.user_info_url, headers=headers)
        if response.status_code != 200:
            return {'status_code': response.status_code,'error': response.reason, 'content': response.content}
        return response.json()
