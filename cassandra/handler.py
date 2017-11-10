from lss import config
from lss.util import logging
logger = logging.getLogger()
if config.DTP=='D':
	logger.setLevel(logging.DEBUG)
else :
	logger.setLevel(logging.ERROR)

from .connection import setup
from .lora_streaming.models import Store00

from datetime import datetime
import json

def store00(arr):
	try:
		msg = json.dumps(arr['msg'])
		tms = datetime.strptime(arr['tms'], "%Y-%m-%dT%H:%M:%S.%fZ")
	except Exception as err:
		logger.error(err)
		tms = datetime.now()
		msg = ''
	
	setup('lora_streaming_t')
	Store00.create(
		eui = arr['eui'],
		tms = tms,
		typ = arr['typ'],
		msg = msg
		)