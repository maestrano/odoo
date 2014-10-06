import pytz
import urllib2
import json
from datetime import datetime,timedelta
import dateutil.parser

# Helper class used to check the validity
# of a Maestrano session
class MnoSsoSession(object, ):
    # Maestrano Settings object
    settings = None
    
    # Session object
    session = None
    
    # User UID
    uid = ''
    
    # Maestrano SSO token
    token = ''
    
    # When to recheck for validity of the sso session
    recheck = None
    
    
    # Construct the MnoSsoSession object
    def __init__(self, mno_settings, session):
        self.settings = mno_settings
        self.session = session
        self.uid = None
        self.token = None
        self.recheck = None
        
        if 'mno_uid' in session: self.uid = session['mno_uid']
        if 'mno_session' in session: self.token = session['mno_session']
        if 'mno_session_recheck' in session: self.recheck = dateutil.parser.parse(session['mno_session_recheck'])

    # Check whether we need to remotely check the
    # session or not
    def remoteCheckRequired(self):
        if (self.uid is not None and self.token is not None and isinstance(self.recheck, datetime)):
            if ((self.recheck - datetime.now(pytz.utc)) > timedelta(seconds = 0)):
                return False
        return True
    
    # Return the full url from which session check
    # should be performed
    def sessionCheckUrl(self):
        url = ('%s/%s?session=%s' % (self.settings.sso_session_check_url, self.uid, self.token))
        return url

    # Fetch url and return content. Wrapper function.
    def fetchUrl(self, url):
        return urllib2.urlopen(url).read()

    # Perform remote session check on Maestrano
    def performRemoteCheck(self):
        json_response = self.fetchUrl(self.sessionCheckUrl())
        if json_response:
            response = json.loads(json_response)
            if (response['valid'] and response['recheck']):
                self.recheck = dateutil.parser.parse(response['recheck'])
                return True
        return False

    # Perform check to see if session is valid
    # Check is only performed if current time is after
    # the recheck timestamp
    # If a remote check is performed then the mno_session_recheck
    # timestamp is updated in session.
    def isValid(self):
        if self.remoteCheckRequired():
            if self.performRemoteCheck():
                self.session['mno_session_recheck'] = self.recheck.isoformat()
                return True
            else:
                return False
        else:
            return True