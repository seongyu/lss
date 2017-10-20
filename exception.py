# Root Exception
class StreamingException(Exception):
	pass

# Basic Exceptions
class ImproperlyConfigured(StreamingException):
	pass

# Cassandra Exceptions
class UnknownCassandraKeyspace(StreamingException):
	pass
