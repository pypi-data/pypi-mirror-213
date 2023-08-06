from AccessControl import AuthEncoding
from plone.app.testing import TEST_USER_NAME, SITE_OWNER_NAME
from plone.testing.z2 import Browser
from wcs.adminauth.tests import FunctionalTestCase
from wcs.adminauth.tests.utils import get_data
from zope.component import getMultiAdapter
import os
import responses
import six
import unittest


class TestAuthView(FunctionalTestCase):

    def get_auth_view(self):
        return getMultiAdapter((self.portal, self.request), name=u'adminauth')

    @unittest.skipUnless(six.PY3, 'only run with python 3 and plone 6')
    def test_redirect_to_cas_login_url_plone6(self):
        browser = Browser(self.portal)
        browser.followRedirects = False
        browser.open(self.portal.absolute_url() + '/adminauth')
        browser.headers['Location']
        self.assertEqual('302 Found', browser.headers['Status'])
        location = (os.environ.get('ADMIN_AUTH_CAS_SERVER_URL', None) + 'login?service=' +
                    self.portal.absolute_url() + '/adminauth')
        self.assertEqual(location,
                         browser.headers['Location'])

    @unittest.skipUnless(six.PY2, 'only run with python 2 and plone < 5.1.x')
    def test_redirect_to_cas_login_url(self):
        from urllib2 import HTTPError
        browser = Browser(self.portal)
        browser.mech_browser.set_handle_redirect(False)
        with self.assertRaises(HTTPError) as cm:
            browser.open(self.portal.absolute_url() + '/adminauth')
        self.assertEqual(302, cm.exception.getcode())
        location = (os.environ.get('ADMIN_AUTH_CAS_SERVER_URL', None) + 'login?service=' +
                    self.portal.absolute_url() + '/adminauth')
        self.assertEqual(location,
                         cm.exception.hdrs['location'])

    def test_find_userfolder_for_not_existing_user(self):
        self.assertEqual(None, self.get_auth_view().find_userfolder('god'))

    def test_find_userfolder_with_user_in_plone_site(self):
        self.assertEqual(self.portal.acl_users,
                         self.get_auth_view().find_userfolder(TEST_USER_NAME))

    def test_find_userfolder_with_user_in_app_root(self):
        self.assertEqual(self.layer['app'].acl_users,
                         self.get_auth_view().find_userfolder(SITE_OWNER_NAME))

    def test_installation_of_session_plugin_in_root_userfolder(self):
        self.assertIn('session_adminauth',
                      self.get_auth_view().pas_userfolder(self.layer['app']))

    def test_initial_admimuser_password_is_not_working(self):
        uf = self.layer['app']['acl_users']
        user_manager = uf['users']
        user_manager.addUser('adminuser', 'adminuser', 'secret')
        stored_pw = user_manager._user_passwords.get('adminuser')
        self.assertTrue(AuthEncoding.pw_validate(stored_pw, 'secret'))
        self.get_auth_view().pas_userfolder(self.layer['app'])
        stored_pw = user_manager._user_passwords.get('adminuser')
        self.assertFalse(AuthEncoding.pw_validate(stored_pw, 'secret'))

    def test_service_url(self):
        view_url = self.portal.absolute_url() + '/adminauth'
        self.request.URL = view_url
        self.assertEqual(view_url,
                         self.get_auth_view().service_url())

    def test_service_url_with_userid(self):
        view_url = self.portal.absolute_url() + '/adminauth'
        self.request.URL = view_url
        self.request.form.update({'userid': 'james'})
        self.assertEqual(view_url + '%3Fuserid%3Djames',
                         self.get_auth_view().service_url())

    def test_admin_user_can_be_changed_via_env(self):
        uf = self.layer['app']['acl_users']
        user_manager = uf['users']
        user_manager.addUser('hans', 'hans', 'secret')
        original = os.environ['ADMIN_AUTH_USERID']
        os.environ['ADMIN_AUTH_USERID'] = 'hans'
        
        try:
            self.get_auth_view().pas_userfolder(self.layer['app'])
            stored_pw = user_manager._user_passwords.get('hans')
            self.assertFalse(AuthEncoding.pw_validate(stored_pw, 'secret'))
        finally:
            os.environ['ADMIN_AUTH_USERID'] = original

    @responses.activate
    def test_validate_ticket_success(self):
        cas_client = self.get_auth_view().cas_client
        responses.add(
            responses.GET,
            '{}{}?ticket=test&service={}'.format(cas_client.server_url, cas_client.url_suffix, cas_client.service_url),
            body=get_data('service_validate_success.xml'), status=200
        )

        self.assertEqual('hugo', self.get_auth_view().validate_ticket('test'))

    @responses.activate
    def test_validate_invalid_ticket(self):
        cas_client = self.get_auth_view().cas_client
        responses.add(
            responses.GET,
            '{}{}?ticket=test&service={}'.format(cas_client.server_url, cas_client.url_suffix, cas_client.service_url),
            body=get_data('service_validate_invalid_ticket.xml'), status=200
        )

        self.assertFalse(self.get_auth_view().validate_ticket('test'))

    @responses.activate
    def test_validate_ticket_invalid_response(self):
        cas_client = self.get_auth_view().cas_client
        responses.add(
            responses.GET,
            '{}{}?ticket=test&service={}'.format(cas_client.server_url, cas_client.url_suffix, cas_client.service_url),
            body='invalid', status=200
        )

        self.assertFalse(self.get_auth_view().validate_ticket('test'))
