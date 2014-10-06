from datetime import datetime
import dateutil.parser
import json
import sys
import random

# Properly format a User received from Maestrano 
# SAML IDP
class MnoSsoBaseUser(object, ):
    # Session Object
    session = None
    
    # User UID
    uid = ''
    
    # User email
    email = ''
    
    # User name
    name = ''
    
    # User surname
    surname = ''
    
    # Maestrano specific user sso session token
    sso_session = ''
    
    # When to recheck for validity of the sso session
    sso_session_recheck = None
    
    # Is user owner of the app
    app_owner = False
    
    # An associative array containing the Maestrano 
    # organizations using this app and to which the
    # user belongs.
    # Keys are the maestrano organization uid.
    # Values are an associative array containing the
    # name of the organization as well as the role 
    # of the user within that organization.
    # ---
    # List of Organization Roles
    # - Member
    # - Power User
    # - Admin
    # - Super Admin
    # ---
    # e.g:
    # { 'org-876' => {
    #      'name' => 'SomeOrga',
    #      'role' => 'Super Admin'
    #   }
    # }
    organizations = []
    
    # User Local Id
    local_id = None
    
    
    # Construct the MnoSsoBaseUser object from a SAML response
    def __init__(self, saml_response, session=[]):
        # Populate user attributes from assertions
        self.session = session
        self.uid = saml_response.get_assertion_attribute_value('mno_uid')[0]
        self.sso_session = saml_response.get_assertion_attribute_value('mno_session')[0]
        self.sso_session_recheck = dateutil.parser.parse(saml_response.get_assertion_attribute_value('mno_session_recheck')[0])
        self.name = saml_response.get_assertion_attribute_value('name')[0]
        self.surname = saml_response.get_assertion_attribute_value('surname')[0]
        self.email = saml_response.get_assertion_attribute_value('email')[0]
        self.app_owner = (saml_response.get_assertion_attribute_value('app_owner')[0] == 'true')
        self.organizations = json.loads(saml_response.get_assertion_attribute_value('organizations')[0])

    # Try to find a local application user matching the sso one
    # using uid first, then email address.
    # If a user is found via email address then then setLocalUid
    # is called to update the local user Maestrano UID
    # ---
    # Internally use the following interface methods:
    #  - getLocalIdByUid
    #  - getLocalIdByEmail
    #  - setLocalUid
    def matchLocal(self):
        self.local_id = self.getLocalIdByUid()
        if self.local_id is None:
            self.local_id = self.getLocalIdByEmail()
            if self.local_id:
                self.setLocalUid()
        if self.local_id:
            self.syncLocalDetails()
        return self.local_id

    # Return whether the user is private (
    # local account or app owner or part of
    # organization owning this app) or public
    # (no link whatsoever with this application)
    def accessScope(self):
        if ((self.local_id or self.app_owner) or (len(self.organizations) > 0)):
            return 'private'
        return 'public'

    # Create a local user by invoking createLocalUser
    # and set uid on the newly created user
    # If createLocalUser returns null then access
    # is refused to the user
    def createLocalUserOrDenyAccess(self):
        if self.local_id is None:
            self.local_id = self.createLocalUser()
            if self.local_id:
                self.setLocalUid()
        return self.local_id
    
    
    # Set user in session. Called by signIn method.
    # This method should be overriden in MnoSsoUser to
    # reflect the app specific way of putting an authenticated
    # user in session.
    def setInSession(self):
        raise Exception('Function %s must be overriden in MnoSsoUser class!'% (sys._getframe().f_code.co_name))
    
    # Create a local user based on the sso user
    # This method must be re-implemented in MnoSsoUser
    # (raise an error otherwise)
    def createLocalUser(self):
        raise Exception('Function %s must be overriden in MnoSsoUser class!'% (sys._getframe().f_code.co_name))

    
    # Get the ID of a local user via Maestrano UID lookup
    # This method must be re-implemented in MnoSsoUser
    # (raise an error otherwise)
    def getLocalIdByUid(self):
        raise Exception('Function %s must be overriden in MnoSsoUser class!'% (sys._getframe().f_code.co_name))

    # Get the ID of a local user via email lookup
    # This method must be re-implemented in MnoSsoUser
    # (raise an error otherwise)
    def getLocalIdByEmail(self):
        raise Exception('Function %s must be overriden in MnoSsoUser class!'% (sys._getframe().f_code.co_name))

    # Set the Maestrano UID on a local user via email lookup
    # This method must be re-implemented in MnoSsoUser
    # (raise an error otherwise)
    def setLocalUid(self):
        raise Exception('Function %s must be overriden in MnoSsoUser class!'% (sys._getframe().f_code.co_name))

    # Set all 'soft' details on the user (like name, surname, email)
    # This is a convenience method that must be implemented in
    # MnoSsoUser but is not mandatory.
    def syncLocalDetails(self):
        return True

    
    # Sign the user in the application. By default,
    # set the mno_uid, mno_session and mno_session_recheck
    # in session.
    # It is expected that this method get extended with
    # application specific behavior in the MnoSsoUser class
    def signIn(self):
        if self.setInSession():
            self.session['mno_uid'] = self.uid
            self.session['mno_session'] = self.sso_session
            self.session['mno_session_recheck'] = self.sso_session_recheck.isoformat()

    # Generate a random password.
    # Convenient to set dummy passwords on users
    def generatePassword(self):
        length = 20
        characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        randomString = ''
        if 1:
            i = 0
            while (i < length):
                randomString = ('%s%s' % (randomString, characters[random.randint(0, (len(characters) - 1))]))
                i = (i + 1)
        return randomString
