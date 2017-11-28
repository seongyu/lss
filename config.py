import os
import os.path

DTP = 'T'

if DTP == 'S':
	MQ_HOST = 'localhost'
	HOST = '10.140.0.8'
elif DTP == 'T':
	# MQ_HOST = '35.201.132.176' # for develop computer
	MQ_HOST = 'localhost' # for GCP server
	HOST = '10.140.0.8' #for cassandra name
	# HOST = '35.201.132.176'
else :
	HOST = 'localhost'
	MQ_HOST = 'localhost'

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

CASSANDRA_CONTACT_POINTS = {
	'S':[
		'10.140.0.2',
		'10.140.0.3',
		'10.140.0.4',
		'10.140.0.5',
		'10.140.0.6',
	],
	'T':[
		'10.140.0.2',
		'10.140.0.3',
		'10.140.0.4',
		'10.140.0.5',
		'10.140.0.6',
	],
	'D':['127.0.0.1']
}

CASSANDRA_DB_PATH = os.path.join(ROOT_PATH,'db','cassandra')

CASSANDRA_KEYSPACES = ['lora_streaming','lora_streaming_t']

LOG_BACKUP_COUNT = 100
LOG_MAX_BYTES = 10 * 1000 * 1000
LOG_DIR_PATH = os.path.join(ROOT_PATH, 'log')
try:
	os.stat(LOG_DIR_PATH)
except:
	os.mkdir(LOG_DIR_PATH)
LOG_FILENAME = 'streaming.log'

MQ_PORT = 5672
MQ_QUEUE = 'lss'
MQ_USER = 'lora'
MQ_PSWD = 'lora'