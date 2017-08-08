"""Testing models"""

import pytest
from mixer.backend.django import mixer

from rest_framework.authtoken.models import Token

from ..models import User

pytestmark = pytest.mark.django_db


class TestUser(object):
    def test_create_user_in_database(self):
        obj = mixer.blend(User, pk=1)
        assert obj.pk == 1, 'Should create a user in database getting an id'

    def test_create_user_instance(self):
        obj = mixer.blend(User)
        assert isinstance(obj, User), 'Should create an instance of User model'

    def test__str__method(self):
        email = 'johndoe@gmail.com'
        obj = mixer.blend(User, email=email)
        assert str(obj) == email, 'Should return the email of a User'

    def test_signal_create_auth_token(self):
        obj = mixer.blend(User)
        assert isinstance(obj.auth_token, Token)

    def test_post_save_is_authenticated(self):
        obj = mixer.blend(User)
        assert obj.is_authenticated(), (
            'After a user is created should keep the authentication')
