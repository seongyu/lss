import os
import os.path

DTP = 'S'

if DTP == 'S':
	HOST = '10.140.0.8'
elif DTP == 'T':
	HOST = '35.201.132.176'
else :
	HOST = 'localhost'

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
	'D':[
		'10.140.0.2',
		'10.140.0.3',
		'10.140.0.4',
		'10.140.0.5',
		'10.140.0.6',
	]
}

CASSANDRA_DB_PATH = os.path.join(ROOT_PATH,'db','cassandra')
CASSANDRA_KEYSPACES = {
	'S' : ['lora_streaming'],
	'T' : ['lora_streaming_t'],
	'D' : ['lora_streaming_t']
}

LOG_BACKUP_COUNT = 100
LOG_MAX_BYTES = 10 * 1000 * 1000
LOG_DIR_PATH = os.path.join(ROOT_PATH, 'log')
try:
	os.stat(LOG_DIR_PATH)
except:
	os.mkdir(LOG_DIR_PATH)
LOG_FILENAME = 'streaming.log'

MQ_HOST = HOST
MQ_PORT = 5672
MQ_QUEUE = 'lss'
MQ_USER = 'lora'
MQ_PSWD = 'lora'