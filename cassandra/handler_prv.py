from lss import config
from lss.util import logging
logger = logging.getLogger()
if config.DTP=='D':
  logger.setLevel(logging.DEBUG)
else :
  logger.setLevel(logging.ERROR)

from .connection import setup
from .lora_streaming.models import Store00
# from .lora_streaming.models import Store01

from datetime import datetime
import json

def store(arr):
  try:
    msg = json.dumps(arr['msg'])
    tms = datetime.strptime(arr['tms'], "%Y-%m-%dT%H:%M:%S.%fZ")
  except Exception as err:
    logger.error('sotre00, parsing error. ',err)
    tms = datetime.now()
    msg = ''
  setup('lora_streaming_t')
  try:
    Store00.create(
      pid = arr['pid'],
      fid = arr['fid'],
      cid = arr['cid'],
      rcid = arr['rcid'],
      sdid = arr['sdid'],
      ttk = arr['ttk'],
      typ = arr['typ'],
      tms = tms,
      msg = msg
      )
  except Exception as err:
    logger.error('store01 save error. ',err)
    pass
