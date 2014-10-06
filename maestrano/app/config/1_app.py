# Get full host (protocal + server host)
#protocol = ('https://' if (('HTTPS' in os.environ['SERVER_PROTOCOL'])) else 'http://')
protocol = "http://"
environment = 'dev'

if environment == 'dev':
    host = "localhost:8069"
else:
    host = os.environ['HOSTNAME'].replace("mcube-", "")

if environment == 'uat':
    host = host + '.app.uat.maestrano.io'
elif environment == 'production':
    host = host + '.mcube.co'
    
full_host = protocol + host

# Name of your application
mno_settings.app_name = 'my-app'

# Enable Maestrano SSO for this app
mno_settings.sso_enabled = True

# SSO initialization URL
mno_settings.sso_init_url = full_host + '/maestrano/auth/saml/index'

# SSO processing url
mno_settings.sso_return_url = full_host + '/maestrano/auth/saml/consume'
