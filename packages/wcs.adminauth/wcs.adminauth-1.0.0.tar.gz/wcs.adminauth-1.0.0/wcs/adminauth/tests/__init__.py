from wcs.adminauth.testing import WCS_ADMINAUTH_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import TestCase
import transaction


class FunctionalTestCase(TestCase):

    layer = WCS_ADMINAUTH_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()
