from tests.base_test import BaseTestCase, CommonTestCase


class JWTTokenTestCase(BaseTestCase):
    '''Test endpoints related to token manipulations.'''

    def setUp(self):
        '''Log in the user and store the refresh token.'''
        super().setUp()
        url = '/api/auth/jwt/create/'
        # Act
        user_credentials = {
            'username': 'username',
            'password': 'Strong_password1',
        }
        response = self.client.post(url, user_credentials)
        CommonTestCase.assert200Response(self, response)

        # Store the tokens for use in other tests
        self.access_token = response.data.get('access')
        self.refresh_token = response.data.get('refresh')

    def test_token_create(self):
        '''Test JWT token creation.'''
        # Arrange
        url = '/api/auth/jwt/create/'
        # Act
        user_credentials = {
            'username': 'username',
            'password': 'Strong_password1',
        }
        response = self.client.post(url, user_credentials)
        # Assert
        CommonTestCase.assert200Response(self, response)
        self.assertIn('access', response.data,
                      'Response must contain access token')
        self.assertIn('refresh', response.data,
                      'Response must contain refresh token')

    def test_token_refresh(self):
        '''Test refreshing the JWT token.'''
        url = '/api/auth/jwt/refresh/'
        # Act
        refresh_token_data = {
            'refresh': self.refresh_token
        }
        response = self.client.post(url, refresh_token_data)
        # Assert
        CommonTestCase.assert200Response(self, response)
        self.assertIn('access', response.data,
                      'Response must contain access token')

    def test_token_verify(self):
        '''Test verifying the JWT token.'''
        url = '/api/auth/jwt/verify/'
        # Act
        token_data = {
            'token': self.access_token
        }
        response = self.client.post(url, token_data)
        # Assert
        CommonTestCase.assert200Response(self, response)
