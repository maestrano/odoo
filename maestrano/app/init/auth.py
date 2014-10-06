#-----------------------------------------------
# Define root folder and load base
#-----------------------------------------------
global MAESTRANO_ROOT
if not(MAESTRANO_ROOT):
    MAESTRANO_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + '/../../'))

execfile(MAESTRANO_ROOT + '/app/init/base.py')

#-----------------------------------------------
# Require your app specific files here
#-----------------------------------------------
APP_DIR = os.path.abspath(MAESTRANO_ROOT + '/../')
sys.path.append(APP_DIR)
import openerp
#define('MY_APP_DIR', realpath(MAESTRANO_ROOT . '/../'));
#require MY_APP_DIR . '/include/some_class_file.php';
#require MY_APP_DIR . '/config/some_database_config_file.php';


#-----------------------------------------------
# Perform your custom preparation code
#-----------------------------------------------
# If you define the $opts variable then it will
# automatically be passed to the MnoSsoUser object
# for construction
# e.g:
# $opts = array();
# if (!empty($db_name) and !empty($db_user)) {
#     $conn = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8", $db_user, $db_pass);
#     $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
#     
#     $opts['db_connection'] = $conn;
# }