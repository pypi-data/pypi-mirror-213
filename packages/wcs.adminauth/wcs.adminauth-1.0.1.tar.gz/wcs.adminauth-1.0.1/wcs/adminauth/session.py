from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import (
    IAuthenticationPlugin,
    ICredentialsResetPlugin,
    ICredentialsUpdatePlugin,
    IExtractionPlugin,
)
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from plone.session import tktauth
from persistent.list import PersistentList
from random import SystemRandom
from zope.interface import implementer
import binascii
import string
import time
import sys


manage_addSessionPlugin = PageTemplateFile(
    "session", globals(), __name__="manage_addSessionPlugin")


def addSessionPlugin(self, id_, title='', REQUEST=None):
    """Add a wcs.adminauth session plugin.
    """
    plugin = SessionPlugin(id_, title)
    self._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace"
            "?manage_tabs_message=wcs.adminauth+session+plugin+added." %
            self.absolute_url()
        )

@implementer(
    IAuthenticationPlugin,
    ICredentialsResetPlugin,
    ICredentialsUpdatePlugin,
    IExtractionPlugin,
)
class SessionPlugin(BasePlugin):
    """Session authentication plugin using cookie-based tickets.
    """

    meta_type = "wcs.adminauth Session Plugin"
    security = ClassSecurityInfo()

    cookie_name = "__ac"
    cookie_path = "/"
    timeout = 12*60*60  # 12h.
    _secret_max_age = 6*60*60  # 6h
    _secrets_keep = 3

    mod_auth_tkt = False
    if sys.version_info[0] == 2 and sys.version_info[1] < 6:
        mod_auth_tkt = True

    def __init__(self, id_, title=None):
        self._setId(id_)
        self.title = title
        self._secrets = PersistentList()
        self._secret_ts = 0

    # IExtractionPlugin implementation
    def extractCredentials(self, request):
        creds = {}

        if self.cookie_name not in request:
            return creds

        try:
            creds["cookie"] = binascii.a2b_base64(request.get(
                self.cookie_name))
        except binascii.Error:
            # If we have a cookie which is not properly base64 encoded it
            # can not be ours.
            return creds

        return creds

    # IAuthenticationPlugin implementation
    def authenticateCredentials(self, credentials):

        # Ignore credentials that are not from our extractor
        extractor = credentials.get('extractor')
        if extractor != self.getId():
            return None

        ticket = credentials["cookie"]
        ticket_data = self._validateTicket(ticket)
        if ticket_data is None:
            return None

        (digest, userid, tokens, user_data, timestamp) = ticket_data
        pas = self._getPAS()
        info = pas._verifyUser(pas.plugins, user_id=userid)
        if info is None:
            return None

        return (info['id'], info['login'])

    # ICredentialsUpdatePlugin implementation
    def updateCredentials(self, request, response, login, new_password):
        pas = self._getPAS()
        info = pas._verifyUser(pas.plugins, login=login)
        if info is not None:
            # Only setup a session for users in our own user folder.
            self._setupSession(info["login"], response)

    # ICredentialsResetPlugin implementation
    def resetCredentials(self, request, response):
        response = self.REQUEST["RESPONSE"]
        response.expireCookie(self.cookie_name, path=self.cookie_path)

    def _setupSession(self, userid, response, tokens=(), user_data=''):
        cookie = tktauth.createTicket(
            secret=self._getSigningSecrets()[0],
            userid=userid,
            tokens=tokens,
            user_data=user_data,
            mod_auth_tkt=self.mod_auth_tkt,
        )
        cookie = binascii.b2a_base64(cookie).rstrip()
        options = dict(path=self.cookie_path, http_only=True)
        response.setCookie(self.cookie_name, cookie, **options)

    def _validateTicket(self, ticket, now=None):
        if now is None:
            now = time.time()
        for secret in self._getSigningSecrets():
            ticket_data = tktauth.validateTicket(
                secret,
                ticket,
                timeout=self.timeout,
                now=now,
                mod_auth_tkt=self.mod_auth_tkt,
            )
            if ticket_data is not None:
                return ticket_data

    def _getSigningSecrets(self):
        # Change secrets periodically
        age = time.time() - self._secret_ts
        if not self._secrets or age > self._secret_max_age:
            random = SystemRandom()
            chars = string.ascii_letters + string.digits
            self._secrets.insert(
                0, ''.join(random.choice(chars) for i in range(64)))
            self._secret_ts = time.time()
            if len(self._secrets) > self._secrets_keep:
                self._secrets.pop()
        return self._secrets
