from unittest import TestCase
from datetime import datetime 
from oauth2flow import OAuth2

class TestOAuth2(TestCase):
    def setUp(self):
        self.oau = OAuth2()
    
    def test_class(self):
        self.assertIsInstance(self.oau, OAuth2)

    def test_token_client_credentials(self):
        token_response = self.oau.token_client_credentials(scope='openid')
        access_token = token_response.get('access_token')
        self.assertIsNotNone(access_token)
    
    def test_token_client_password(self):
        username = 'minio'
        password = 'clientminio'
        token_response = self.oau.token_password(username,password,scope='openid')
        access_token = token_response.get('access_token')
        self.assertIsNotNone(access_token)

    def test_introspect_token_credentials(self):
        auth = OAuth2()
        token_response = auth.token_client_credentials(scope='')
        access_token = token_response.get('access_token')
        introspect = self.oau.introspect_token(access_token)
        data = datetime.now()
        seq = int(data.timestamp())
        self.assertGreater(introspect.get('exp'),seq)
        self.assertGreaterEqual(introspect.get('iat'),seq)
        self.assertTrue(introspect.get('active'))

    def test_introspect_token_credentials_not_valid(self):
        access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJKUUZKUkFGQjQtQVY1ZHI2TE1RQV8xVEtJX2R0OVc3RnFvT2liRUtpLU13In0.eyJleHAiOjE3MzcyMzczOTEsImlhdCI6MTczNzIzNzA5MSwianRpIjoiMzU3MjUyZTUtZDM0NS00NDU2LWE3OTUtM2U5ZWExYjdmZTRkIiwiaXNzIjoiaHR0cHM6Ly9zc28uYXBwcy50amRmdC5qdXMuYnIvYXV0aC9yZWFsbXMvU1VERVMiLCJhdWQiOlsicGpldHJhbnNmZXItZnJvbnRlbmQiLCJhY2NvdW50Il0sInN1YiI6IjA5ZjAzMmYwLTYyNmUtNDM4OS04YWM3LTliNTE1MWQ3NGJhYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudC1taW5pbyIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3VkZXMiXX0sInJlc291cmNlX2FjY2VzcyI6eyJwamV0cmFuc2Zlci1mcm9udGVuZCI6eyJyb2xlcyI6WyJSZWFsbUFkbWluIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgdGpkZnRfcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMC4wLjE0Ni4xNjAiLCJjbGllbnRJZCI6ImNsaWVudC1taW5pbyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWNsaWVudC1taW5pbyIsImNsaWVudEFkZHJlc3MiOiIxMC4wLjE0Ni4xNjAifQ.PVecfG3sogMCf7pjUl5608QER3TwRkoBSX0SX256sTY9yxuf_E2Cyqj8jk86eVtSuC56bKaWTc1WW-MAXPsGvidgbm7TT0c7uALoGojICKP9jHsjLxynwQl0yiig9K2ipKIpoR1HhC4dVB3dNxNusiHy63JdsbJJCGhsqnWbYjGhh52EKlCQvIb3YLc8-AuzwOBFMTOcc9-Yn-9WH5liOwm6kTKCL7tGmb1laxk4ohKviqzdDYr1Nh475VUqs2ifa_PDoqbhYXJsFq2E9SLzgX9twJFdPmddcuRI4e9js--oYrsMEUu_-xVOBYr7bOb_MnMsL-A_xMga7UrYx8ANcg'
        introspect = self.oau.introspect_token(access_token)
        data = datetime.now()
        seq = int(data.timestamp())
        self.assertFalse(introspect.get('active'))

    def test_introspect_user_info(self):
        username = 'minio'
        password = 'clientminio'
        token_response = self.oau.token_password(username,password,scope='openid')
        access_token = token_response.get('access_token')
        user = self.oau.user_info(access_token)
        self.assertEqual(user.get('preferred_username'),'minio')

    def test_introspect_value(self):
        username = 'minio'
        password = 'clientminio'
        token_response = self.oau.token_password(username,password,scope='openid')
        access_token = token_response.get('access_token')
        introspect = self.oau.introspect_token(access_token)
        self.assertTrue(introspect.get('active'))

    def test_token_password_error(self):
        username = 'min'
        password = 'clientminio'
        token_response = self.oau.token_password(username,password,scope='')
        self.assertEqual(token_response.get('status_code'),401)
    
    def test_token_credential_error(self):
        self.oau.client_id = 'min'
        token_response = self.oau.token_client_credentials(scope='')
        self.assertEqual(token_response.get('status_code'),401)
    
    def test_token_validation(self):
        token_response = self.oau.token_client_credentials(scope='openid')
        access_token = token_response.get('access_token')
        token_validation = self.oau.token_validation(access_token)
        self.assertTrue(token_validation.get('active'))

    def test_token_validation_error(self):
        access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJKUUZKUkFGQjQtQVY1ZHI2TE1RQV8xVEtJX2R0OVc3RnFvT2liRUtpLU13In0.eyJleHAiOjE3MzcyMzczOTEsImlhdCI6MTczNzIzNzA5MSwianRpIjoiMzU3MjUyZTUtZDM0NS00NDU2LWE3OTUtM2U5ZWExYjdmZTRkIiwiaXNzIjoiaHR0cHM6Ly9zc28uYXBwcy50amRmdC5qdXMuYnIvYXV0aC9yZWFsbXMvU1VERVMiLCJhdWQiOlsicGpldHJhbnNmZXItZnJvbnRlbmQiLCJhY2NvdW50Il0sInN1YiI6IjA5ZjAzMmYwLTYyNmUtNDM4OS04YWM3LTliNTE1MWQ3NGJhYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudC1taW5pbyIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3VkZXMiXX0sInJlc291cmNlX2FjY2VzcyI6eyJwamV0cmFuc2Zlci1mcm9udGVuZCI6eyJyb2xlcyI6WyJSZWFsbUFkbWluIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgdGpkZnRfcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMC4wLjE0Ni4xNjAiLCJjbGllbnRJZCI6ImNsaWVudC1taW5pbyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWNsaWVudC1taW5pbyIsImNsaWVudEFkZHJlc3MiOiIxMC4wLjE0Ni4xNjAifQ.PVecfG3sogMCf7pjUl5608QER3TwRkoBSX0SX256sTY9yxuf_E2Cyqj8jk86eVtSuC56bKaWTc1WW-MAXPsGvidgbm7TT0c7uALoGojICKP9jHsjLxynwQl0yiig9K2ipKIpoR1HhC4dVB3dNxNusiHy63JdsbJJCGhsqnWbYjGhh52EKlCQvIb3YLc8-AuzwOBFMTOcc9-Yn-9WH5liOwm6kTKCL7tGmb1laxk4ohKviqzdDYr1Nh475VUqs2ifa_PDoqbhYXJsFq2E9SLzgX9twJFdPmddcuRI4e9js--oYrsMEUu_-xVOBYr7bOb_MnMsL-A_xMga7UrYx8ANcg'
        token_validation = self.oau.token_validation(access_token)
        self.assertFalse(token_validation.get('active'))

    def test_token_roles(self):
        token_response = self.oau.token_client_credentials(scope='openid')
        access_token = token_response.get('access_token')
        token_roles = self.oau.token_roles(access_token)
        self.assertIsNotNone(token_roles)

    def test_token_roles_error(self):
        access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJKUUZKUkFGQjQtQVY1ZHI2TE1RQV8xVEtJX2R0OVc3RnFvT2liRUtpLU13In0.eyJleHAiOjE3MzcyMzczOTEsImlhdCI6MTczNzIzNzA5MSwianRpIjoiMzU3MjUyZTUtZDM0NS00NDU2LWE3OTUtM2U5ZWExYjdmZTRkIiwiaXNzIjoiaHR0cHM6Ly9zc28uYXBwcy50amRmdC5qdXMuYnIvYXV0aC9yZWFsbXMvU1VERVMiLCJhdWQiOlsicGpldHJhbnNmZXItZnJvbnRlbmQiLCJhY2NvdW50Il0sInN1YiI6IjA5ZjAzMmYwLTYyNmUtNDM4OS04YWM3LTliNTE1MWQ3NGJhYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudC1taW5pbyIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3VkZXMiXX0sInJlc291cmNlX2FjY2VzcyI6eyJwamV0cmFuc2Zlci1mcm9udGVuZCI6eyJyb2xlcyI6WyJSZWFsbUFkbWluIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgdGpkZnRfcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMC4wLjE0Ni4xNjAiLCJjbGllbnRJZCI6ImNsaWVudC1taW5pbyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWNsaWVudC1taW5pbyIsImNsaWVudEFkZHJlc3MiOiIxMC4wLjE0Ni4xNjAifQ.PVecfG3sogMCf7pjUl5608QER3TwRkoBSX0SX256sTY9yxuf_E2Cyqj8jk86eVtSuC56bKaWTc1WW-MAXPsGvidgbm7TT0c7uALoGojICKP9jHsjLxynwQl0yiig9K2ipKIpoR1HhC4dVB3dNxNusiHy63JdsbJJCGhsqnWbYjGhh52EKlCQvIb3YLc8-AuzwOBFMTOcc9-Yn-9WH5liOwm6kTKCL7tGmb1laxk4ohKviqzdDYr1Nh475VUqs2ifa_PDoqbhYXJsFq2E9SLzgX9twJFdPmddcuRI4e9js--oYrsMEUu_-xVOBYr7bOb_MnMsL-A_xMga7UrYx8ANcg'
        token_roles = self.oau.token_roles(access_token)
        self.assertEqual(token_roles.get('resource_access'),None)

    def test_user_info_error(self):
        access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJKUUZKUkFGQjQtQVY1ZHI2TE1RQV8xVEtJX2R0OVc3RnFvT2liRUtpLU13In0.eyJleHAiOjE3MzcyMzczOTEsImlhdCI6MTczNzIzNzA5MSwianRpIjoiMzU3MjUyZTUtZDM0NS00NDU2LWE3OTUtM2U5ZWExYjdmZTRkIiwiaXNzIjoiaHR0cHM6Ly9zc28uYXBwcy50amRmdC5qdXMuYnIvYXV0aC9yZWFsbXMvU1VERVMiLCJhdWQiOlsicGpldHJhbnNmZXItZnJvbnRlbmQiLCJhY2NvdW50Il0sInN1YiI6IjA5ZjAzMmYwLTYyNmUtNDM4OS04YWM3LTliNTE1MWQ3NGJhYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudC1taW5pbyIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3VkZXMiXX0sInJlc291cmNlX2FjY2VzcyI6eyJwamV0cmFuc2Zlci1mcm9udGVuZCI6eyJyb2xlcyI6WyJSZWFsbUFkbWluIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgdGpkZnRfcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMC4wLjE0Ni4xNjAiLCJjbGllbnRJZCI6ImNsaWVudC1taW5pbyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWNsaWVudC1taW5pbyIsImNsaWVudEFkZHJlc3MiOiIxMC4wLjE0Ni4xNjAifQ.PVecfG3sogMCf7pjUl5608QER3TwRkoBSX0SX256sTY9yxuf_E2Cyqj8jk86eVtSuC56bKaWTc1WW-MAXPsGvidgbm7TT0c7uALoGojICKP9jHsjLxynwQl0yiig9K2ipKIpoR1HhC4dVB3dNxNusiHy63JdsbJJCGhsqnWbYjGhh52EKlCQvIb3YLc8-AuzwOBFMTOcc9-Yn-9WH5liOwm6kTKCL7tGmb1laxk4ohKviqzdDYr1Nh475VUqs2ifa_PDoqbhYXJsFq2E9SLzgX9twJFdPmddcuRI4e9js--oYrsMEUu_-xVOBYr7bOb_MnMsL-A_xMga7UrYx8ANcg'
        user = self.oau.user_info(access_token)
        self.assertEqual(user.get('preferred_username'),None)

    def test_introspector_error(self):
        access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJKUUZKUkFGQjQtQVY1ZHI2TE1RQV8xVEtJX2R0OVc3RnFvT2liRUtpLU13In0.eyJleHAiOjE3MzcyMzczOTEsImlhdCI6MTczNzIzNzA5MSwianRpIjoiMzU3MjUyZTUtZDM0NS00NDU2LWE3OTUtM2U5ZWExYjdmZTRkIiwiaXNzIjoiaHR0cHM6Ly9zc28uYXBwcy50amRmdC5qdXMuYnIvYXV0aC9yZWFsbXMvU1VERVMiLCJhdWQiOlsicGpldHJhbnNmZXItZnJvbnRlbmQiLCJhY2NvdW50Il0sInN1YiI6IjA5ZjAzMmYwLTYyNmUtNDM4OS04YWM3LTliNTE1MWQ3NGJhYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudC1taW5pbyIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3VkZXMiXX0sInJlc291cmNlX2FjY2VzcyI6eyJwamV0cmFuc2Zlci1mcm9udGVuZCI6eyJyb2xlcyI6WyJSZWFsbUFkbWluIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgdGpkZnRfcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMC4wLjE0Ni4xNjAiLCJjbGllbnRJZCI6ImNsaWVudC1taW5pbyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWNsaWVudC1taW5pbyIsImNsaWVudEFkZHJlc3MiOiIxMC4wLjE0Ni4xNjAifQ.PVecfG3sogMCf7pjUl5608QER3TwRkoBSX0SX256sTY9yxuf_E2Cyqj8jk86eVtSuC56bKaWTc1WW-MAXPsGvidgbm7TT0c7uALoGojICKP9jHsjLxynwQl0yiig9K2ipKIpoR1HhC4dVB3dNxNusiHy63JdsbJJCGhsqnWbYjGhh52EKlCQvIb3YLc8-AuzwOBFMTOcc9-Yn-9WH5liOwm6kTKCL7tGmb1laxk4ohKviqzdDYr1Nh475VUqs2ifa_PDoqbhYXJsFq2E9SLzgX9twJFdPmddcuRI4e9js--oYrsMEUu_-xVOBYr7bOb_MnMsL-A_xMga7UrYx8ANcg'
        introspect = self.oau.introspect_token(access_token)
        self.assertEqual(introspect.get('preferred_username'),None)