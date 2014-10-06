#-----------------------------------------------
# Define root folder
#-----------------------------------------------
global MAESTRANO_ROOT
if not(MAESTRANO_ROOT):
    MAESTRANO_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + '/../../'))

#-----------------------------------------------
# Load Libraries & Settings
#-----------------------------------------------
execfile(MAESTRANO_ROOT + '/app/init/_lib_loader.py')
execfile(MAESTRANO_ROOT + '/app/init/_config_loader.py')
