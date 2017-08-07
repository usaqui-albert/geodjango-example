"""Testing views"""

import pytest
from mixer.backend.django import mixer

from django.test import RequestFactory
from rest_framework.test import force_authenticate, APIRequestFactory

from .. import views
from ..models import User
from .test_serializers import TestDataCases

pytestmark = pytest.mark.django_db


class TestUserView(TestDataCases):

    factory = RequestFactory()
    tested_view = views.UserView

    def test_put_request_not_allowed(self):
        req = self.factory.put('/')
        resp = self.tested_view.as_view()(req)
        assert 'detail' in resp.data
        assert resp.data['detail'] == 'Method "PUT" not allowed.'
        assert resp.status_code == 405

    def test_patch_request_not_allowed(self):
        req = self.factory.patch('/')
        resp = self.tested_view.as_view()(req)
        assert 'detail' in resp.data
        assert resp.data['detail'] == 'Method "PATCH" not allowed.'
        assert resp.status_code == 405

    def test_delete_request_not_allowed(self):
        req = self.factory.delete('/')
        resp = self.tested_view.as_view()(req)
        assert 'detail' in resp.data
        assert resp.data['detail'] == 'Method "DELETE" not allowed.'
        assert resp.status_code == 405

    def test_get_request_return_http_200(self):
        req = self.factory.get('/')
        resp = self.tested_view.as_view()(req)
        assert resp.status_code == 200, 'Should return status 200 OK'

    def test_get_request_return_users_list(self):
        req = self.factory.get('/')
        resp = self.tested_view.as_view()(req)
        assert isinstance(resp.data, list), 'Should return a list of users'

    def test_post_request_successful(self):
        req = self.factory.post('/', self.data_valid)
        resp = self.tested_view.as_view()(req)
        assert 'id' in resp.data, 'Should be created and return an id'
        assert resp.status_code == 201, 'Should return status 201 CREATED'

    def test_post_request_successful_return_token(self):
        req = self.factory.post('/', self.data_valid)
        resp = self.tested_view.as_view()(req)
        assert 'token' in resp.data, 'Should return the authentication token'
        assert resp.status_code == 201, 'Should return status 201 CREATED'

    def test_post_request_email_missing(self):
        req = self.factory.post('/', self.data_email_missing)
        resp = self.tested_view.as_view()(req)
        assert 'email' in resp.data
        assert 'This field is required.' in resp.data['email']
        assert resp.status_code == 400, 'Should return status 400 BAD REQUEST'

    def test_post_request_wrong_format(self):
        req = self.factory.post('/', self.data_email_wrong_format)
        resp = self.tested_view.as_view()(req)
        assert 'email' in resp.data
        assert 'Enter a valid email address.' in resp.data['email']
        assert resp.status_code == 400, 'Should return status 400 BAD REQUEST'

    def test_post_request_email_field_empty(self):
        req = self.factory.post('/', self.data_email_field_empty)
        resp = self.tested_view.as_view()(req)
        assert 'email' in resp.data
        assert 'This field may not be blank.' in resp.data['email']
        assert resp.status_code == 400, 'Should return status 400 BAD REQUEST'

    def test_post_request_email_already_exists(self):
        mixer.blend(User, email='johndoe@gmail.com')
        req = self.factory.post('/', self.data_email_already_exists)
        resp = self.tested_view.as_view()(req)
        assert 'email' in resp.data
        assert 'user with this email already exists.' in resp.data['email']
        assert resp.status_code == 400, 'Should return status 400 BAD REQUEST'


class TestUserDetailView(TestDataCases):

    factory = RequestFactory()
    tested_view = views.UserDetailView
    api_factory = APIRequestFactory()

    def test_post_request_not_allowed(self):
        user = mixer.blend(User, pk=1)
        req = self.factory.post('/')
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert 'detail' in resp.data
        assert resp.data['detail'] == 'Method "POST" not allowed.'
        assert resp.status_code == 405

    def test_get_request_allow_any_user_exists(self):
        mixer.blend(User, pk=1)
        req = self.factory.get('/')
        resp = self.tested_view.as_view()(req, pk=1)

        assert resp.status_code == 200, 'Should return status 200 OK'
        assert isinstance(resp.data, dict)

    def test_get_request_allow_any_user_not_found(self):
        mixer.blend(User, pk=1)
        req = self.factory.get('/')
        resp = self.tested_view.as_view()(req, pk=2)

        assert 'detail' in resp.data
        assert 'Not found.' == resp.data['detail']
        assert resp.status_code == 404, 'Should return status 404 NOT FOUND'

    def test_delete_request_not_account_owner(self):
        mixer.blend(User, pk=1)
        user = mixer.blend(User, pk=2)
        req = self.factory.delete('/')
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert 'detail' in resp.data
        message_error = 'You do not have permission to perform this action.'
        assert message_error in resp.data['detail']
        assert resp.status_code == 403, 'Should return status 403 FORBIDDEN'

    def test_delete_request_account_owner(self):
        user = mixer.blend(User, pk=1)
        req = self.factory.delete('/')
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert resp.data is None, 'Should not return any content'
        assert resp.status_code == 204, 'Should return status 204 NO CONTENT'

    def test_patch_request_not_account_owner(self):
        mixer.blend(User, pk=1)
        user = mixer.blend(User, pk=2)
        req = self.api_factory.patch('/')
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert 'detail' in resp.data
        message_error = 'You do not have permission to perform this action.'
        assert message_error in resp.data['detail']
        assert resp.status_code == 403, 'Should return status 403 FORBIDDEN'

    def test_patch_request_account_owner(self):
        user = mixer.blend(User, pk=1, name='John Doe')
        name_to_update = 'Jane Doe'
        req = self.api_factory.patch('/', data={'name': name_to_update})
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert 'name' in resp.data
        assert not 'John Doe' == resp.data['name']
        assert 'Jane Doe' == resp.data['name'], (
            'The name should be updated from John Doe to Jane Doe')
        assert resp.status_code == 200, 'Should return status 200 OK'

    def test_put_request_not_account_owner(self):
        mixer.blend(User, pk=1)
        user = mixer.blend(User, pk=2)
        req = self.api_factory.put('/')
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert 'detail' in resp.data
        message_error = 'You do not have permission to perform this action.'
        assert message_error in resp.data['detail']
        assert resp.status_code == 403, 'Should return status 403 FORBIDDEN'

    def test_put_request_account_owner(self):
        user = mixer.blend(User, pk=1, name='Peter Parker')
        req = self.api_factory.patch('/', data=self.data_valid)
        force_authenticate(req, user)
        resp = self.tested_view.as_view()(req, pk=1)

        assert 'name' in resp.data
        assert not 'Peter Parker' == resp.data['name']
        assert 'John Doe' == resp.data['name'], (
            'The name should be updated from Peter Parker to John Doe')
        assert resp.status_code == 200, 'Should return status 200 OK'
