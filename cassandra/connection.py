from lss import config
from lss.util import logging
logger = logging.getLogger()
if config.DTP=='D':
	logger.setLevel(logging.DEBUG)
else :
	logger.setLevel(logging.ERROR)

from cassandra.cqlengine import connection
from lss.exception import *
from lss.util.eval import *

def keyspace_DTP(keyspace):
	eval_config_DTP()

	if keyspace not in config.CASSANDRA_KEYSPACES:
		raise UnknownCassandraKeyspace
	return keyspace # It could update if needs DTP process

def register_connection():
	logger.debug('Connecting registration start ***')
	connection.register_connection(config.HOST, config.CASSANDRA_CONTACT_POINTS[config.DTP])
	logger.debug('*** Registed successfully')

def setup(keyspace):
	connection.setup(config.CASSANDRA_CONTACT_POINTS[config.DTP], keyspace_DTP(keyspace))

def unregister_connection():
	logger.debug('Connecting unregistration start ***')

	connection.unregister_connection(config.HOST)
	logger.debug('*** Unregisted successfully')