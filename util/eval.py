from lss import config
from lss.exception import *

def eval_config_DTP():
	if config.DTP not in ('D','T','S'):
		raise ImproperlyConfigured
