from lss import config
from lss.exception import *

def eval_setting_DTP():
	if config.DTP not in ('D', 'S'):
		raise ImproperlyConfigured
