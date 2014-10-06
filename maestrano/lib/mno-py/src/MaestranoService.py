from MnoSsoSession import MnoSsoSession

class MaestranoService(object):
    _settings = None
    _instance = None
    _after_sso_sign_in_path = '/'
    _session = None
    
    # constructor
    #
    # This is a private constructor (use getInstance to get an instance of this class)
    def __init__(self):
        pass
    
    # Configure the service by assigning settings
    @classmethod
    def configure(cls, config_settings):
        cls._settings = config_settings
    
    # Returns an instance of this class
    # (this class uses the singleton pattern)
    @classmethod
    def getInstance(cls):
        if not((cls._instance is not None)):
            cls._instance = MaestranoService()
        return cls._instance

    # Return the maestrano settings
    def getSettings(self):
        return self._settings
    
    # Set the maestrano sso session
    def setSession(self, session):
        self._session = session
        return self._session
    
    # Return the maestrano sso session
    def getSession(self):
        return self._session

    # Return the maestrano sso session
    def getSsoSession(self):
        return MnoSsoSession(self._settings, self.getSession())

    # Check if Maestrano SSO is enabled
    def isSsoEnabled(self):
        return (self._settings and self._settings.sso_enabled)

    # Return wether intranet sso mode is enabled (no public pages)
    def isSsoIntranetEnabled(self):
        return (self.isSsoEnabled() and self._settings.sso_intranet_mode)

    # Return where the app should redirect internally to initiate
    # SSO request
    def getSsoInitUrl(self):
        return self._settings.sso_init_url

    # Return where the app should redirect after logging user
    # out
    def getSsoLogoutUrl(self):
        return self._settings.sso_access_logout_url

    # Return where the app should redirect if user does
    # not have access to it
    def getSsoUnauthorizedUrl(self):
        return self._settings.sso_access_unauthorized_url

    # Set the after sso signin path
    @classmethod
    def setAfterSsoSignInPath(cls, path):
        self._after_sso_sign_in_path = path

    # Return the after sso signin path
    def getAfterSsoSignInPath(self):
        return self._after_sso_sign_in_path