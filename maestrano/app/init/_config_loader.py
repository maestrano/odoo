from MnoSettings import MnoSettings
from MaestranoService import MaestranoService

global MAESTRANO_ROOT

# Initialize mno_settings variable
mno_settings = MnoSettings()

# Require Config files
execfile(MAESTRANO_ROOT + '/app/config/1_app.py')
execfile(MAESTRANO_ROOT + '/app/config/2_maestrano.py')

# Configure Maestrano Service
MaestranoService.configure(mno_settings)
