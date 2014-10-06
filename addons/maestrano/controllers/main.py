# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2012 OpenERP s.a. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import os
import tempfile
import getpass
import urllib
import sys

import werkzeug.urls
import werkzeug.exceptions

import inspect

import openerp
from openerp import SUPERUSER_ID
from openerp.modules.registry import RegistryManager
from openerp.addons.web.controllers.main import login_and_redirect, set_cookie_and_redirect

MAESTRANO_ROOT = os.path.abspath(inspect.getfile(inspect.currentframe()) + '/../../../../../maestrano/')

# Load context
execfile(MAESTRANO_ROOT + '/app/init/auth.py')
from onelogin.saml import AuthRequest
from onelogin.saml import Response
from MaestranoService import MaestranoService
from MnoSsoUser import MnoSsoUser

_logger = logging.getLogger(__name__)

class Maestrano(openerp.addons.web.http.Controller):
    _cp_path = '/maestrano/auth/saml'

    #_store = filestore.FileOpenIDStore(_storedir)
    
    @openerp.addons.web.http.httprequest
    def logout(self, req, **kw):
        # Get Maestrano instance and build redirect url
        maestrano = MaestranoService.getInstance()
    
        # Redirect to Maestrano logout page
        redirect = werkzeug.utils.redirect(maestrano.getSsoLogoutUrl())
        
        return redirect
    
    @openerp.addons.web.http.httprequest
    def index(self, req, **kw):
        # Get Maestrano instance and build redirect url
        maestrano = MaestranoService.getInstance()
        auth_request_url = AuthRequest.create(**(maestrano.getSettings().getSamlSettings()))
    
        # Redirect to IDP
        redirect = werkzeug.utils.redirect(auth_request_url)
        
        return redirect

    
    @openerp.addons.web.http.httprequest
    def consume(self, req, **kw):
        # Get Maestrano Service
        maestrano = MaestranoService.getInstance()
    
        # Make sure Options variable
        # is defined
        global opts
        try:
            opts
        except NameError:
            opts = {}
        
        wsgienv = req.httprequest.environ
        env = dict(
            base_location=req.httprequest.url_root.rstrip('/'),
            HTTP_HOST=wsgienv['HTTP_HOST'],
            REMOTE_ADDR=wsgienv['REMOTE_ADDR'],
        )
        opts['env'] = env
        
        # Get SAML POST data
        _logger.info(req)
        auth_data = req.params['SAMLResponse']
    
        # Build SAML response
        settings = maestrano.getSettings().getSamlSettings()
        saml_response = Response(auth_data,settings['idp_cert_fingerprint'])
    
        if saml_response.is_valid():
            # Get Maestrano User
            sso_user = MnoSsoUser(saml_response,req.session, opts)
        
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
                redirect = set_cookie_and_redirect(req,maestrano.getAfterSsoSignInPath())
        
            else:
                # Redirect to 'access denied' page
                redirect = werkzeug.utils.redirect(maestrano.getSsoUnauthorizedUrl())
            
            return redirect

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
