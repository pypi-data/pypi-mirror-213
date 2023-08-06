from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.session import tktauth
from wcs.adminauth.session import SessionPlugin
from wcs.adminauth.tests import FunctionalTestCase
from wcs.adminauth.tests.utils import b64encode
from zope.publisher.browser import TestRequest
import binascii


class TestSessionPlugin(FunctionalTestCase):

    def setUp(self):
        # Setup PAS plugin
        super(TestSessionPlugin, self).setUp()

        uf = self.portal.acl_users
        plugin = SessionPlugin('session_adminauth')
        uf._setObject(plugin.getId(), plugin)
        plugin = uf['session_adminauth']
        plugin.manage_activateInterfaces([
            'IAuthenticationPlugin',
            'ICredentialsResetPlugin',
            'ICredentialsUpdatePlugin',
            'IExtractionPlugin',
        ])
        self.plugin = plugin

    def test_extract_credentials_without_cookie(self):
        req = TestRequest()
        self.assertEqual({}, self.plugin.extractCredentials(req))

    def test_extract_credentials_from_cookie(self):
        cookie = b64encode('test ticket')
        req = TestRequest(**{self.plugin.cookie_name: cookie})
        creds = self.plugin.extractCredentials(req)
        self.assertEqual(b"test ticket", creds["cookie"])

    def test_extract_credentials_from_invalid_cookie(self):
        cookie = "test ticket"
        req = TestRequest(**{self.plugin.cookie_name: cookie})
        self.assertEqual({}, self.plugin.extractCredentials(req))

    def test_authenticate_credentials_of_wrong_extractor(self):
        creds = {'cookie': 'test ticket', 'extractor': 'wrong'}
        self.assertEqual(None, self.plugin.authenticateCredentials(creds))

    def test_authenticate_credentials(self):
        ticket = tktauth.createTicket(
            secret=self.plugin._getSigningSecrets()[0],
            userid=TEST_USER_ID,
        )
        creds = {'cookie': ticket, 'extractor': self.plugin.getId()}
        self.assertEqual((TEST_USER_ID, TEST_USER_NAME),
                         self.plugin.authenticateCredentials(creds))

    def test_update_credentials(self):
        req = TestRequest()
        self.plugin.updateCredentials(req, req.response, TEST_USER_NAME, '')
        ticket = binascii.a2b_base64(req.response.getCookie(
            self.plugin.cookie_name)['value'])
        ticket_data = self.plugin._validateTicket(ticket)
        self.assertEqual(ticket_data[1], TEST_USER_NAME)

    def test_initial_signing_secret(self):
        secrets = self.plugin._getSigningSecrets()
        self.assertEqual(1, len(secrets))
        self.assertEqual(64, len(secrets[0]))
        self.assertEqual(secrets, self.plugin._getSigningSecrets())

    def test_signing_secret_changes(self):
        secret = self.plugin._getSigningSecrets()[0]
        self.plugin._secret_ts -= (self.plugin._secret_max_age + 1)
        self.assertEqual(2, len(self.plugin._getSigningSecrets()))
        self.assertNotEqual(secret, self.plugin._getSigningSecrets()[0])
        self.assertEqual(secret, self.plugin._getSigningSecrets()[1])

    def test_signing_secret_max_keep(self):
        for i in range(0, self.plugin._secrets_keep):
            self.plugin._getSigningSecrets()[0]
            self.plugin._secret_ts -= (self.plugin._secret_max_age + 1)
        self.assertEqual(self.plugin._secrets_keep,
                         len(self.plugin._getSigningSecrets()))
