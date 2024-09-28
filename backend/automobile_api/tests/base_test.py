from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

UserModel = get_user_model()


class BaseTestCase(TestCase):
    """Class provides prearranged data."""
    @classmethod
    def setUpTestData(cls):
        cls.auth_user = UserModel.objects.create_user(
            username='username',
            first_name='user',
            last_name='surname',
            password='Strong_password1',
            email='mailmail@gmail.com',
        )
        cls.auth_client = APIClient()
        token = Token.objects.create(user=cls.auth_user)
        cls.auth_client.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key)


class CommonTestCase(TestCase):
    """Class contains common assertions methods."""

    def assert200Response(self, response: HttpResponse,
                          verbose=True):
        msg = 'Response status code must be 200.'
        if verbose:
            msg += f'\n Response data: {response.data}'
        self.assertEqual(response.status_code, 200,
                         msg)

    def assert201Response(self, response: HttpResponse,
                          verbose=True):
        msg = 'Response status code must be 201.'
        if verbose:
            msg += f'\n Response data: {response.data}'
        self.assertEqual(response.status_code, 201,
                         msg)

    def assert400Response(self, response: HttpResponse,
                          expected_reason: str | None = None):
        '''
        expected_reason is the reason that must cause 400 response in
        failure tests.
        '''
        msg = 'Response status code must be 400.'
        if expected_reason:
            msg += (f'Because: \n'
                    f'{expected_reason}')
        self.assertEqual(response.status_code, 400,
                         msg)

    def assertJSONFormatResponse(self, response: HttpResponse):
        self.assertEqual(response.headers['Content-Type'],
                         'application/json',
                         'Response format must be a JSON.')
