# OAuth2flow Client
Authorization protocol that allows applications to access resources from other applications on the user's behalf.   
Allows applications to gain limited access to user information without sharing credentials.  

## Implements Flow
- [ ] Authorization Code (future)
- [x] Resource Owner Password Credentials
- [ ] Implicit (future)
- [x] Client Credentials

# Quick Started
Install usign pip:  
```bash
pip install oauth2flow 
```
configure variables before using , let's code.  

## Variables
Environment variables are mandatory for oauth2flow to work in your project, use exports linux or dotenv pypi    
to make them available in the development environment.

**env.file** 
```bash
CLIENT_ID="client" 
CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
REDIRECT_URI=""
AUTHORIZATION_BASE_URL=https://provider.com/auth/realms/{RELM}/protocol/openid-connect/auth
TOKEN_URL=https://provider.com/auth/realms/{RELM}/protocol/openid-connect/token
USERINFO_URL=https://provider.com/auth/realms/{RELM}/protocol/openid-connect/userinfo
INTROSPECTION_URL=https://provider.com/auth/realms/{RELM}/protocol/openid-connect/token/introspect
OPENID_CONFIGURATION_URL=https://provider.com/auth/realms/{RELM}/.well-known/openid-configuration
```

## Project in devcontainer
Project was built on top of python 3.12 dockenized devcontainer vscode microsoft environment  
```json
"runArgs": ["--env-file",".env"],
```
