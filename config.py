import os.path

DTP = 'D'

if DTP !='D':
	HOST = '10.140.0.8'
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
	'D': ['127.0.0.1']
}

CASSANDRA_DB_PATH = os.path.join(ROOT_PATH,'db','cassandra')
CASSANDRA_KEYSPACES = ['lora_streaming']

LOG_BACKUP_COUNT = 100
LOG_MAX_BYTES = 10 * 1000 * 1000
LOG_DIR_PATH = os.path.join(ROOT_PATH, 'log')
LOG_FILENAME = 'streaming.log'

MQ_HOST = HOST
MQ_PORT = 5672
MQ_QUEUE = 'lss'
