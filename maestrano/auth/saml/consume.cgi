#!/usr/bin/python

import inspect, os, sys, traceback, cgi
import werkzeug

print "Context-Type: text/html\n\n"

try:
    MAESTRANO_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + '/../../'))

    # Load context
    execfile(MAESTRANO_ROOT + '/app/init/auth.py')
    from onelogin.saml import Response
    from MaestranoService import MaestranoService
    from MnoSsoUser import MnoSsoUser
    
    # Get Maestrano Service
    maestrano = MaestranoService.getInstance()
    
    # Make sure Options variable
    # is defined
    global opts
    try:
        opts
    except NameError:
        opts = {}
    
    # Get SAML POST data
    auth_data = cgi.FieldStorage().getvalue('SAMLResponse')
    
    #print os.environ.__dict__
    basereq = werkzeug.wrappers.Request(os.environ.__dict__)
    
    # Build SAML response
    settings = maestrano.getSettings().getSamlSettings()
    saml_response = Response(auth_data,settings['idp_cert_fingerprint'])
    
    if saml_response.is_valid():
        # Get Maestrano User
        sso_user = MnoSsoUser(saml_response,{}, opts)
        
        # Try to match the user with a local one
        sso_user.matchLocal()
        
        # If user was not matched then attempt
        # to create a new local user
        if sso_user.local_id is None:
            sso_user.createLocalUserOrDenyAccess()
            
        # If user is matched then sign it in
        # Refuse access otherwise
        if sso_user.local_id is not None:
            sso_user.signIn()
            
            # Redirect to application
            print "Location: " + maestrano.getAfterSsoSignInPath()
            print
        
        else:
            # Redirect to 'access denied' page
            print "Location: " + maestrano.getSsoUnauthorizedUrl()
            print


except Exception as inst:
    print inst
    print '<br/><br/><br/>'
    print traceback.print_exc(file=sys.stdout)