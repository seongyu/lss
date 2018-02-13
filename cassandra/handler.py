from lss import config
from lss.util import logging
logger = logging.getLogger()
if config.DTP=='D':
	logger.setLevel(logging.DEBUG)
else :
	logger.setLevel(logging.ERROR)

from .connection import setup
# from .lora_streaming.models import Store00
from .lora_streaming.models import Store01

from datetime import datetime
import json

def store(arr):
	try:
		msg = json.dumps(arr['msg'])
		tms = datetime.strptime(arr['tms'], "%Y-%m-%dT%H:%M:%S.%fZ")
		ogtg = arr['pid'].split('-')[0] # it will be gw_id or bk_id or hr_id
	except Exception as err:
		logger.error('store : parsing error. ',err)
		tms = datetime.now()
		msg = ''
		ogtg = ''
		
	setup('lora_streaming_t')
	try:
		Store01.create(
			pid = arr['pid'],
			fid = arr['fid'],
			cid = arr['cid'],
			rcid = arr['rcid'],
			ogtg = ogtg,
			sdid = arr['sdid'],
			ttk = arr['ttk'],
			typ = arr['typ'],
			tms = tms,
			msg = msg
			)
	except Exception as err:
		logger.error('store : db push error. ',err)
		pass
