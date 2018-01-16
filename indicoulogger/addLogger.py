from MaKaC.authentication import AuthenticatorMgr
from MaKaC.user import LoginInfo
from flask import request
from flask import session

from userlogger import UserLogger
from indico.core.config import Config
import MaKaC.webinterface.urlHandlers as urlHandlers
from MaKaC.webinterface.rh.login import RHSignInBase, RHSignOut
from indico.util.i18n import _
from MaKaC.common.timezoneUtils import nowutc

# Init User Logger
logger = UserLogger().logger

def _makeLoginProcess(self):
    # Check for automatic login
    authManager = AuthenticatorMgr()
    userinfo = str(self._login) + ' ' + str(request.remote_addr)
    if (authManager.isSSOLoginActive() and len(authManager.getList()) == 1 and
            not Config.getInstance().getDisplayLoginPage()):
        self._redirect(urlHandlers.UHSignInSSO.getURL(authId=authManager.getDefaultAuthenticator().getId()))
        return
    if request.method != 'POST':
        return self._signInPage.display(returnURL=self._returnURL)
    else:
        li = LoginInfo(self._login, self._password)
        av = authManager.getAvatar(li)
        if not av:
            logger.info(userinfo + ' Login FAILED: Wrong credentials')
            return self._signInPageFailed.display(returnURL=self._returnURL)
        elif not av.isActivated():
            if av.isDisabled():
                logger.info(userinfo + ' Login FAILED: Account is DISABLED.')
                self._redirect(self._disabledAccountURL(av))
            else:
                logger.info(userinfo + ' Login FAILED: Account is NOT ACTIVTED.')
                self._redirect(self._unactivatedAccountURL(av))
            return _("Your account is not active\nPlease activate it and try again")
        else:
            logger.info(userinfo + ' Login OK: Logged in as ' + av.getFullName())
            av._loginDate = nowutc()
            self._setSessionVars(av)
        self._addExtraParamsToURL()
        self._redirect(self._url)

def _process(self):

    user = self._getUser()
    if user:
        userinfo = user.getFullName() + ' ' + str(request.remote_addr)
        logger.info('Logged out: ' + userinfo)
        self._returnURL = AuthenticatorMgr().getLogoutCallbackURL(self) or self._returnURL
        self._setUser(None)

    session.clear()
    self._redirect(self._returnURL)



RHSignInBase._makeLoginProcess = _makeLoginProcess
RHSignOut._process = _process


def do_addLogger():
    logger.info("User Logger Started")