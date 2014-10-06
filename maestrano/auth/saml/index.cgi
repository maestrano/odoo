#!/usr/bin/python

import inspect, os, sys, traceback

try:
    MAESTRANO_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + '/../../'))

    # Load context
    execfile(MAESTRANO_ROOT + '/app/init/auth.py')
    from onelogin.saml import AuthRequest
    from MaestranoService import MaestranoService
    
    # Get Maestrano instance and build redirect url
    maestrano = MaestranoService.getInstance()
    auth_request_url = AuthRequest.create(**(maestrano.getSettings().getSamlSettings()))
    
    # Redirect to IDP
    print "Location: " + auth_request_url
    print


except Exception as inst:
    print inst
    print '<br/><br/><br/>'
    print traceback.print_exc(file=sys.stdout)
