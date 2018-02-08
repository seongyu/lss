from lss import config
from lss.util import logging

from cassandra.cqlengine import connection, CQLEngineException, models

from lss.exception import *
from lss.util.eval import *

logger = logging.getLogger()
if config.DTP=='D':
	logger.setLevel(logging.DEBUG)
else :
	logger.setLevel(logging.ERROR)

def keyspace_DTP(keyspace):
	eval_config_DTP()

	if keyspace not in config.CASSANDRA_KEYSPACES:
		raise UnknownCassandraKeyspace
	return keyspace # It could update if needs DTP process

# input : conn_name, host_array, [option]
def register_connection():
	logger.debug('Connecting registration start ***')
	connection.register_connection(config.CA_HOST, config.CASSANDRA_CONTACT_POINTS[config.DTP], default=True)
	logger.debug('*** Registed successfully')

# input : conn_name
def setup(keyspace):
	try :
		# if conn_name is exist
		connection.set_default_connection(config.CA_HOST)
	except Exception as err :
		logger.error('=====CQLEngineException=====',err)
		unregister_connection()
		register_connection()

		models.DEFAULT_KEYSPACE = keyspace_DTP(keyspace)

# input : conn_name
def unregister_connection():
	logger.debug('Connecting unregistration start ***')
	connection.unregister_connection(config.CA_HOST)
	logger.debug('*** Unregisted successfully')