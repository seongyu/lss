from logging import CRITICAL	# 50
from logging import ERROR	# 40
from logging import WARNING	# 30
from logging import INFO	# 20
from logging import DEBUG	# 10
from logging import NOTSET	#  0
from lss import config

import logging
import logging.handlers
import os.path
import time

class UTCFormatter(logging.Formatter):
	converter = time.gmtime

def getLogger():
	logger = logging.getLogger()

	if logger.handlers:
		return logger

	fileHandler = logging.handlers.RotatingFileHandler(
		os.path.join(config.LOG_DIR_PATH, config.LOG_FILENAME),
		mode = 'a',
		maxBytes = config.LOG_MAX_BYTES,
		backupCount = config.LOG_BACKUP_COUNT,
		encoding = 'utf8',
		delay = 0,
	)
	streamHandler = logging.StreamHandler()
	formatter = UTCFormatter('%(asctime)s|%(filename)-20s|%(funcName)-40s|%(lineno)5s|%(levelname)-8s|%(message)s')

	fileHandler.setFormatter(formatter)
	logger.addHandler(fileHandler)

	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)

	logger.setLevel(logging.NOTSET)

	return logger
