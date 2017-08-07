"""Testing serializers"""

import pytest
from mixer.backend.django import mixer

from ..serializers import CreateUserSerializer, UserSerializer
from ..models import User

pytestmark = pytest.mark.django_db


class TestDataCases(object):

    data_email_missing = {
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'en',
        'currency': 'usd'
    }
    data_email_wrong_format = {
        'email': 'johndoe@gmail.c',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'en',
        'currency': 'usd'
    }
    data_email_field_empty = {
        'email': '',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'en',
        'currency': 'usd'
    }
    data_email_already_exists = {
        'email': 'johndoe@gmail.com',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'en',
        'currency': 'usd'
    }
    data_phone_number_longer_than_15 = {
        'email': 'johndoe@gmail.com',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234-567-890',
        'language': 'en',
        'currency': 'usd'
    }
    data_language_longer_than_7 = {
        'email': 'johndoe@gmail.com',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'portuguese',
        'currency': 'usd'
    }
    data_language_does_not_exist = {
        'email': 'johndoe@gmail.com',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'lan123',
        'currency': 'usd'
    }
    data_currency_longer_than_3 = {
        'email': 'johndoe@gmail.com',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'en',
        'currency': 'usd_'
    }
    data_valid = {
        'email': 'johndoe@gmail.com',
        'password': '123456',
        'name': 'John Doe',
        'phone_number': '123-123-1234',
        'language': 'en',
        'currency': 'usd'
    }


class TestCreateUserSerializer(TestDataCases):

    serializer_class = CreateUserSerializer

    def test_is_valid_email_missing(self):
        serializer = self.serializer_class(data=self.data_email_missing)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_email_missing(self):
        serializer = self.serializer_class(data=self.data_email_missing)
        serializer.is_valid()
        assert 'email' in serializer.errors, 'Should has email key'
        assert 'This field is required.' in serializer.errors['email']

    def test_is_valid_email_wrong_format(self):
        serializer = self.serializer_class(data=self.data_email_wrong_format)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_email_wrong_format(self):
        serializer = self.serializer_class(data=self.data_email_wrong_format)
        serializer.is_valid()
        assert 'email' in serializer.errors, 'Should has email key'
        assert 'Enter a valid email address.' in serializer.errors['email']

    def test_is_valid_email_field_empty(self):
        serializer = self.serializer_class(data=self.data_email_field_empty)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_email_field_empty(self):
        serializer = self.serializer_class(data=self.data_email_field_empty)
        serializer.is_valid()
        assert 'email' in serializer.errors, 'Should has email key'
        assert 'This field may not be blank.' in serializer.errors['email']

    def test_is_valid_email_already_exists(self):
        mixer.blend(User, email='johndoe@gmail.com')
        serializer = self.serializer_class(data=self.data_email_already_exists)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_email_already_exists(self):
        mixer.blend(User, email='johndoe@gmail.com')
        serializer = self.serializer_class(data=self.data_email_already_exists)
        serializer.is_valid()
        assert 'email' in serializer.errors, 'Should has email key'
        error_message = 'user with this email already exists.'
        assert error_message in serializer.errors['email']

    def test_is_valid_phone_number_longer_than_15(self):
        serializer = self.serializer_class(
            data=self.data_phone_number_longer_than_15)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_phone_number_longer_than_15(self):
        serializer = self.serializer_class(
            data=self.data_phone_number_longer_than_15)
        serializer.is_valid()
        assert 'phone_number' in serializer.errors, (
            'Should has phone_number key')
        error_message = 'Ensure this field has no more than 15 characters.'
        assert error_message in serializer.errors['phone_number']

    def test_is_valid_language_does_not_exist(self):
        serializer = self.serializer_class(
            data=self.data_language_does_not_exist)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_language_does_not_exist(self):
        serializer = self.serializer_class(
            data=self.data_language_does_not_exist)
        serializer.is_valid()
        assert 'language' in serializer.errors, 'Should has language key'
        error_message = '"lan123" is not a valid choice.'
        assert error_message in serializer.errors['language']

    def test_is_valid_language_longer_than_7(self):
        serializer = self.serializer_class(
            data=self.data_language_longer_than_7)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_language_longer_than_7(self):
        serializer = self.serializer_class(
            data=self.data_language_longer_than_7)
        serializer.is_valid()
        assert 'language' in serializer.errors, 'Should has language key'
        error_message = '"portuguese" is not a valid choice.'
        assert error_message in serializer.errors['language']

    def test_is_valid_currency_longer_than_3(self):
        serializer = self.serializer_class(
            data=self.data_currency_longer_than_3)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_currency_longer_than_3(self):
        serializer = self.serializer_class(
            data=self.data_currency_longer_than_3)
        serializer.is_valid()
        assert 'currency' in serializer.errors, 'Should has currency key'
        error_message = 'Ensure this field has no more than 3 characters.'
        assert error_message in serializer.errors['currency']

    def test_save_return_a_user_instance(self):
        serializer = self.serializer_class(data=self.data_valid)
        serializer.is_valid()
        obj = serializer.save()
        assert isinstance(obj, User), 'Should return a User instance'

    def test_save_create_user_in_database(self):
        serializer = self.serializer_class(data=self.data_valid)
        serializer.is_valid()
        user = serializer.save()
        assert isinstance(user.id, int), (
            'Should create a user in database getting an id')

    def test_save_user_with_hash_password(self):
        serializer = self.serializer_class(data=self.data_valid)
        serializer.is_valid()
        user = serializer.save()
        raw_password = self.data_valid['password']
        assert user.check_password(raw_password), (
            'Should create a user with a hash password')

    def test_returned_data_without_password_key(self):
        serializer = self.serializer_class(data=self.data_valid)
        serializer.is_valid()
        assert 'password' not in serializer.data, (
            'Should not return password key given password is a write '
            'only field in this serializer'
        )


class TestUserSerializer(object):

    serializer_class = UserSerializer

    def test_update_email_already_exists(self):
        jane_user = mixer.blend(User, email='janedoe@gmail.com')
        john_user = mixer.blend(User, email='johndoe@gmail.com')
        serializer = self.serializer_class(
            jane_user, data={'email': john_user.email}, partial=True)
        assert not serializer.is_valid(), 'Should not be valid email to update'

    def test_update_email_already_exists_message(self):
        jane_user = mixer.blend(User, email='janedoe@gmail.com')
        john_user = mixer.blend(User, email='johndoe@gmail.com')
        serializer = self.serializer_class(
            jane_user, data={'email': john_user.email}, partial=True)
        serializer.is_valid()
        error_message = 'user with this email already exists.'
        assert error_message in serializer.errors['email']

    def test_update_password_not_received(self):
        old_password = '123456'
        new_password = 'new password'
        user = mixer.blend(User, password=old_password)
        user.set_password(user.password)
        user.save()
        serializer = self.serializer_class(
            user, data={'password': new_password}, partial=True)
        serializer.is_valid()
        updated_user = serializer.save()
        assert not updated_user.check_password(new_password)
        assert updated_user.check_password(old_password), (
            'The password should not be updated')
