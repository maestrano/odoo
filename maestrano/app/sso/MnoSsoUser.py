import os
from MnoSsoBaseUser import MnoSsoBaseUser
import openerp
from openerp import SUPERUSER_ID
from openerp.modules.registry import RegistryManager
from openerp.osv.fields import char
import inspect
import werkzeug

#
# Configure App specific behavior for 
# Maestrano SSO
#
class MnoSsoUser(MnoSsoBaseUser):
    # Database connection
    connection = None
    Users = None
    env = None
    
    #
    # Extend constructor to inialize app specific objects
    #
    # @param OneLogin_Saml_Response $saml_response
    #   A SamlResponse object from Maestrano containing details
    #   about the user being authenticated
    #
    def __init__(self, saml_response, session=[], opts=[]):
        super(MnoSsoUser,self).__init__(saml_response,session)
        
        dbname = 'openerp'
        self.connection = RegistryManager.get(dbname)
        
        # Get Users service and extend it
        self.Users = self.connection.get('res.users')
        self.Users._columns['mno_uid'] = openerp.osv.fields.char()
        self.Users._all_columns['mno_uid'] = openerp.osv.fields.column_info('mno_uid', openerp.osv.fields.char())
        
        if opts['env']:
            self.env = opts['env']
    
    
    # Set user in session. Called by signIn method.
    def setInSession(self):
        password = self.generatePassword()
        
        if self.local_id is not None:
            with self.connection.cursor() as cr:
                ret = self.Users.write(cr, SUPERUSER_ID, [self.local_id], {
                    'password': password
                })
                cr.commit()
                self.session.authenticate('openerp', self.uid, password, self.env)
        return True
        
    # Sign the user in the application. By default,
    # set the mno_uid, mno_session and mno_session_recheck
    # in session.
    # It is expected that this method get extended with
    # application specific behavior in the MnoSsoUser class
    def signIn(self):
        if self.setInSession():
            self.session.context['mno_uid'] = self.uid
            self.session.context['mno_session'] = self.sso_session
            self.session.context['mno_session_recheck'] = self.sso_session_recheck.isoformat()
    
    # Create a local user based on the sso user
    # Only if access scope is private
    def createLocalUser(self):
        if self.accessScope() == "private":
            with self.connection.cursor() as cr:
                user_hash = self.buildLocalUser()
                user_id = self.Users.create(cr, SUPERUSER_ID, user_hash)
            
                if user_id is not None:
                    # add groups
                    groups = self.getGroupIdsToAssign()
                    if groups:
                        vals = {'groups_id': [(4, g) for g in groups]}
                        ret = self.Users.write(cr, SUPERUSER_ID, [user_id], vals)

                    return user_id
            
        return None
            
    # Build a hash used for user creation
    def buildLocalUser(self):
        user = {
          'login': self.uid,
          'name': (self.name + ' ' + self.surname),
          'password': self.generatePassword(),
          'email': self.email  
        }
        
        return user
    
    # Create the role to give to the user based on context
    # If the user is the owner of the app or at least Admin
    # for each organization,
    def getGroupIdsToAssign(self):
        default_user_roles = None;
        default_admin_roles = [1,2,6]
        role_ids = default_user_roles #basic user
        
        if self.app_owner:
            role_ids = default_admin_roles
        else:
            for organization in self.organizations.itervalues():
                if (organization['role'] == 'Admin' or organization['role'] == 'Super Admin'):
                    role_ids = default_admin_roles
                else:
                    role_ids = default_user_roles
        
        return role_ids
    
    # Get the ID of a local user via Maestrano UID lookup
    def getLocalIdByUid(self):
        with self.connection.cursor() as cr:
            usr_list = self.Users.search(cr, SUPERUSER_ID, [('mno_uid','=',self.uid)],0,1)
            if len(usr_list) > 0:
                return usr_list[0]
        return None
            
    # Get the ID of a local user via email lookup
    def getLocalIdByEmail(self):
        with self.connection.cursor() as cr:
            usr_list = self.Users.search(cr, SUPERUSER_ID, [('user_email','=',self.email)],0,1)
            if len(usr_list) > 0:
                return usr_list[0].id
        return None
        
    # Set the Maestrano UID on a local user via email lookup
    def setLocalUid(self):
        if self.local_id is not None:
            with self.connection.cursor() as cr:
                ret = self.Users.write(cr, SUPERUSER_ID, [self.local_id], {
                    'mno_uid': self.uid
                })
                return ret
        return None
    
    # Set all 'soft' details on the user (like name, surname, email)
    def syncLocalDetails(self):
        if self.local_id is not None:
            with self.connection.cursor() as cr:
                ret = self.Users.write(cr, SUPERUSER_ID, [self.local_id], {
                    'name': self.name + ' ' + self.surname,
                    'user_email': self.email,
                    'login': self.uid
                })
                return ret
        return None
