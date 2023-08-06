from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
import wcs.adminauth
import os


class AdminauthLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(AdminauthLayer, self).setUpZope(app, configurationContext)
        self.loadZCML(package=wcs.adminauth)
        z2.installProduct(app, 'wcs.adminauth')
        os.environ['ADMIN_AUTH_USERID'] = 'adminuser'
        os.environ['ADMIN_AUTH_CAS_SERVER_URL'] = 'https://cas.example-server.org/'


WCS_ADMINAUTH_FIXTURE = AdminauthLayer()
WCS_ADMINAUTH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(WCS_ADMINAUTH_FIXTURE,), name="wcs.adminauth:Functional")
