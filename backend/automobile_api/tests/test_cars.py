from cars.models import Car, Comment
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tests.base_test import BaseTestCase, CommonTestCase
from time import sleep

UserModel = get_user_model()
'''Tests related to Cars API endpoints'''


class CarsAPITestCase(BaseTestCase):
    '''Test suite related to cars instances.'''
    BASE_URL = '/api/cars/'
    CAR_MODEL = Car

    def setUp(self):
        self.car = self.CAR_MODEL.objects.create(
            make='Toyota',
            model='Camry',
            year=2021,
            description=('Компактный седан с отличной экономией'
                         'топлива и современными технологиями безопасности.'),
            owner=self.auth_user
        )

        self.additional_user_info = {
            'username': 'aux_user',
            'first_name': 'aux_user',
            'last_name': 'surname',
            'password': 'Strong_password1',
            'email': 'aux_user@gmail.com',
        }
        self.additional_user = UserModel.objects.create(
            **self.additional_user_info
        )
        self.additional_auth_client = APIClient()
        token = Token.objects.create(user=self.additional_user)
        self.additional_auth_client.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key)

    def test_list_of_cars(self):
        '''Test that user can get list of cars.'''
        # Arrange
        url = self.BASE_URL
        # Act
        response = self.client.get(url)
        # Assert
        CommonTestCase.assert200Response(self, response)
        CommonTestCase.assertJSONFormatResponse(self, response)
        self.assertIn('results', response.data,
                      'Response should contains results list.')

    def test_get_specific_car(self):
        '''Test scenario when user trying to get specific car info.'''
        # Arrange
        existing_car_id = self.car.id
        non_existing_car_id = 9999
        correct_url = f'{self.BASE_URL}{existing_car_id}/'
        incorrect_url = f'{self.BASE_URL}{non_existing_car_id}/'
        test_cases = [
            (correct_url, 200, 'User must be able to get info about '
                               'existing car'),
            (incorrect_url, 404, 'User must get 404 reponse when '
                                 'attempting to reach non-existing car info')
        ]
        # Act
        for url, expected_status_code, err_msg in test_cases:
            with self.subTest(url=url,
                              expected_status_code=expected_status_code,
                              err_msg=err_msg
                              ):
                response = self.client.get(url)
                # Assert
                self.assertEqual(response.status_code,
                                 expected_status_code, err_msg)

    def test_creation_of_a_new_car_with_valid_data(self):
        """
        Test scenario when user trying to create a new car instance.
        User must successfully create a new car instance.
        """
        # Arrange
        url = self.BASE_URL
        car_info = {
            'make': 'Ford',
            'model': 'Mustang',
            'description': ('Спортивный автомобиль с мощным'
                            'двигателем и агрессивным дизайном.'),
        }
        counter_before_creation = (self.CAR_MODEL.objects
                                   .filter(**car_info).count())
        # Act
        response = self.auth_client.post(url, car_info)
        # Assert
        counter_after_creation = (self.CAR_MODEL.objects
                                  .filter(**car_info).count())
        CommonTestCase.assert201Response(self, response)
        CommonTestCase.assertJSONFormatResponse(self, response)
        self.assertEqual(int(counter_after_creation - counter_before_creation),
                         1,
                         'Amount of car after creation attempt must be '
                         'greater than amount of car before creation '
                         'exactly by 1.')

    def test_creation_of_a_new_car_with_invalid_data(self):
        """
        Test scenario when user trying to create a new car instance.
        User trying to provide invalid data.
        """
        # Arrange
        url = self.BASE_URL
        car_info = {
            'make': 'Ford',
            'model': 'Mustang',
            'year': 1967,
            'description': ('Спортивный автомобиль с мощным'
                            'двигателем и агрессивным дизайном.'),
        }
        test_cases = {
            'invalid year format': {**car_info,
                                    'year': 'nineteen sixty-seven'},
            'invalid make': {**car_info, 'make': ''},
            'invalid model': {**car_info, 'model': '&2>Mod~el^'},
            'invalid description': {**car_info, 'description': ''}
        }
        # Act
        for failure_reason, car_data in test_cases.items():
            with self.subTest(failure_reason=failure_reason,
                              car_data=car_data):
                response = self.auth_client.post(url, car_data)
                # Assert
                CommonTestCase.assert400Response(self, response,
                                                 failure_reason)

    def test_creation_of_multiple_cars_at_once(self):
        '''Test checks that user cannot change multiple cars at once'''
        # TODO
    def test_update_car_info_with_valid_data(self):
        """Test scenario when user trying to update a new car instance."""
        # Arrange
        url = f'{self.BASE_URL}{self.car.id}/'
        new_car_info = {
            'make': 'Ford',
            'model': 'Mustang Shelby',
            'description': ('Спортивный автомобиль с мощным'
                            'двигателем и агрессивным дизайном.'),
        }
        # Act
        response = self.auth_client.put(url, new_car_info)
        self.car.refresh_from_db()
        # Assert
        CommonTestCase.assert200Response(self, response)
        CommonTestCase.assertJSONFormatResponse(self, response)
        self.assertEqual(self.car.model, new_car_info['model'],
                         'Test Car must have new model field after update')
        # TearDown
        self.CAR_MODEL.objects.filter(**new_car_info).delete()

    def test_update_car_info_with_invalid_data(self):
        """
        Pre-failed test scenario when user
        trying to update a new car instance.
        """
        # Arrange
        url = f'{self.BASE_URL}{self.car.id}/'

        additional_car_info = {
            'make': 'Honda',
            'model': 'Civic',
            'year': 2020,
            'description': ('Надежный и экономичный седан, '
                            'идеален для городской эксплуатации.'),
            'owner': self.additional_user
        }
        additional_car = self.CAR_MODEL.objects.create(**additional_car_info)
        new_car_info = {
            'make': 'Ford',
            'model': 'Mustang Shelby',
            'description': ('Спортивный автомобиль с мощным'
                            'двигателем и агрессивным дизайном.'),
        }

        test_cases = [
            # Bad Request data - 400 error
            (self.auth_client, {**new_car_info, 'model': ''},
             400, 'Car with invalid data  cannot be update'),
            # Unauthenticated user - 401 Error
            (self.client, new_car_info,
             401, 'Unauthenticated user cannot update a new car instance'),
            # Update another user car - 403 Error
            (self.additional_auth_client, new_car_info,
             403, 'User cannot update anothers user car.'),
        ]
        # Act
        for client, car_data, expected_response_code, err_msg in test_cases:
            with self.subTest(client=client, car_data=car_data,
                              expected_response_code=expected_response_code,
                              err_msg=err_msg):
                response = client.put(url, car_data)
                # Assert
                self.assertEqual(response.status_code, expected_response_code,
                                 err_msg)
                self.assertEqual(
                    self.CAR_MODEL.objects.filter(**new_car_info).count(),
                    0,
                    'No car with new provided model title should be found'
                )
        # TearDown
        additional_car.delete()

    def test_delete_car_unsuccessfully(self):
        # Arrange
        url = f'{self.BASE_URL}{self.car.id}/'
        test_cases = [
            (self.client, 401,
             'Unauthenticated user cannot delete a car'),
            (self.additional_auth_client, 403,
             'User cannnot delete an another user car'),
        ]
        # Act
        for client, expected_status_code, err_msg in test_cases:
            with self.subTest(client=client, err_msg=err_msg,
                              expected_status_code=expected_status_code):
                response = client.delete(url)
                # Assert
                self.assertEqual(response.status_code, expected_status_code,
                                 err_msg)
                self.assertIsNotNone(self.car,
                                     'Test car instance must not be deleted')

    def test_user_delete_his_car_successfully(self):
        # Arrange
        url = f'{self.BASE_URL}{self.car.id}/'
        # Act
        response = self.auth_client.delete(url)
        try:
            self.car.refresh_from_db()
        except ObjectDoesNotExist:
            self.car = None
        # Assert
        self.assertEqual(response.status_code, 204,
                         'Car instance must be successfully deleted')
        self.assertIsNone(self.car, 'Test car instance must be deleted')

    def test_updated_at_field_of_car_model(self):
        '''Test that "updated_at" field updates dynamically.'''
        # Arrange
        url = f'{self.BASE_URL}{self.car.id}/'
        before_update = self.car.updated_at
        new_car_info = {
            'make': 'Ford',
            'model': 'Mustang Shelby',
            'description': ('Спортивный автомобиль с мощным'
                            'двигателем и агрессивным дизайном.'),
        }
        # Act
        response = self.auth_client.put(url, new_car_info)
        self.car.refresh_from_db()
        after_update = self.car.updated_at
        # Assert
        CommonTestCase.assert200Response(self, response)
        self.assertNotEqual(before_update, after_update,
                            '"updated_at field must be changed '
                            'after put request"')

    def test_created_at_field_of_a_car_model(self):
        '''Test that created_at field does not update after creation.'''
        # Arrange
        url = f'{self.BASE_URL}{self.car.id}/'
        before_update = self.car.created_at
        new_car_info = {
            'make': 'Ford',
            'model': 'Mustang Shelby',
            'description': ('Спортивный автомобиль с мощным'
                            'двигателем и агрессивным дизайном.'),
        }
        # Act
        response = self.auth_client.put(url, new_car_info)
        self.car.refresh_from_db()
        after_update = self.car.created_at
        # Assert
        CommonTestCase.assert200Response(self, response)
        self.assertEqual(before_update, after_update,
                         '"created_at field must remains te same '
                         'after put request"')

    def test_owner_of_a_car_is_request_user(self):
        '''
        Check that request user will be recorded as owner of new car instance.
        '''
        # Arrange
        url = self.BASE_URL
        new_car_info = {
            'make': 'Chevrolet',
            'model': 'Camaro',
            'description': ('Как в трансформерах.'),
        }
        # Act
        response = self.auth_client.post(url, new_car_info)
        # Assert
        CommonTestCase.assert201Response(self, response)
        new_car = self.CAR_MODEL.objects.latest('created_at')
        self.assertEqual(self.auth_user, new_car.owner)


class CarsAPIManualChangeRestrictionTestCase(BaseTestCase):
    '''
    Test that user can not manually change fields
    that not purposed to be updated.
    '''


class CarsHTTPDisallowedMethodsTestCase(BaseTestCase):
    '''Test that there are no exessive methods are allowed.'''


class CommentsAPITestCase(BaseTestCase):
    '''Test suite related to comments instance.'''

    BASE_URL = '/api/cars/'
    COMMENT_MODEL = Comment
    CAR_MODEL = Car

    def setUp(self):
        self.car = self.CAR_MODEL.objects.create(
            make='Toyota',
            model='Camry',
            year=2021,
            description=('Компактный седан с отличной экономией'
                         'топлива и современными технологиями безопасности.'),
            owner=self.auth_user
        )

    def test_get_list_of_comments_of_specific_car(self):
        '''Test that user can get a list of comments realted to specific car'''
        # Arrange
        existing_url = f'{self.BASE_URL}{self.car.id}/comments/'
        non_existing_url = f'{self.BASE_URL}9999/comments/'

        test_cases = [
            (self.client, 200, existing_url,
             'User must be able to get list of comments'),
            (self.client, 404, non_existing_url,
             'User must get 404 error if requested car does not exist'),
        ]
        # Act
        for client, expected_status_code, url, err_msg in test_cases:
            with self.subTest(client=client, err_msg=err_msg, url=url,
                              expected_status_code=expected_status_code):
                response = client.get(url)
                # Assert
                self.assertEqual(response.status_code, expected_status_code,
                                 err_msg)
                CommonTestCase.assertJSONFormatResponse(response)

    def test_make_new_comment_to_specific_car(self):
        # Arrange
        existing_url = f'{self.BASE_URL}{self.car.id}/comments/'
        non_existing_url = f'{self.BASE_URL}9999/comments/'

        comment_data = {
            'content': ('Отличный автомобиль, но немного шумный '
                        'на высоких скоростях.')}
        test_cases = [
            (self.auth_client, 201, existing_url,
             'User must be able to make a new car comment.'),
            (self.client, 401, existing_url,
             'Unauthenticated user cannot make a new car comment.'),
            (self.auth_client, 404, non_existing_url,
             'User must get 404 error if requested car does not exist.'),
        ]
        # Act
        for client, expected_status_code, url, err_msg in test_cases:
            with self.subTest(client=client, url=url, err_msg=err_msg,
                              expected_status_code=expected_status_code):
                response = client.post(url, comment_data)
                # Assert
                self.assertEqual(response.status_code, expected_status_code,
                                 err_msg)
                if expected_status_code == 201:
                    self.assertEqual(self.CAR_MODEL.comments.count(), 1,
                                     ('There should be only one '
                                      'existing car comment'))

    def test_author_of_a_comment_is_request_user(self):
        '''
        Check that request user will be recorded
        as author of new comment instance.
        '''
        # TODO
        pass
