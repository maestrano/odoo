#-----------------------------------------------
# Require dependencies
#-----------------------------------------------
#define('PHP_SAML_XMLSECLIBS_DIR', ('%s/lib/php-saml/ext/xmlseclibs/' % (MAESTRANO_ROOT,)))
# require(('%sxmlseclibs.php' % (PHP_SAML_XMLSECLIBS_DIR,)), False)
global MAESTRANO_ROOT
PY_SAML_DIR = MAESTRANO_ROOT + '/lib/python-saml/'
sys.path.append(PY_SAML_DIR)

#define('PHP_SAML_DIR', ('%s/lib/php-saml/src/OneLogin/Saml/' % (MAESTRANO_ROOT,)))
# require(('%sAuthRequest.php' % (PHP_SAML_DIR,)), False)
# require(('%sResponse.php' % (PHP_SAML_DIR,)), False)
# require(('%sSettings.php' % (PHP_SAML_DIR,)), False)
# require(('%sXmlSec.php' % (PHP_SAML_DIR,)), False)

#-----------------------------------------------
# Require Maestrano library
#-----------------------------------------------
MNO_PY_DIR = MAESTRANO_ROOT + '/lib/mno-py/src/'
sys.path.append(MNO_PY_DIR)
sys.path.append(MNO_PY_DIR + '/sso')
import MnoSettings
import MaestranoService
import MnoSsoBaseUser
import MnoSsoSession
# define('MNO_PY_DIR', ('%s/lib/mno-php/src/' % (MAESTRANO_ROOT,)))
# require(('%sMnoSettings.php' % (MNO_PHP_DIR,)), False)
# require(('%sMaestranoService.php' % (MNO_PHP_DIR,)), False)
# require(('%ssso/MnoSsoBaseUser.php' % (MNO_PHP_DIR,)), False)
# require(('%ssso/MnoSsoSession.php' % (MNO_PHP_DIR,)), False)

#-----------------------------------------------
# Require Maestrano app files
#-----------------------------------------------
MNO_APP_DIR = MAESTRANO_ROOT + '/app'
sys.path.append(MNO_APP_DIR + '/sso')
import MnoSsoUser
