from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Store00(Model):
	eui = columns.Text(partition_key=True)
	tms = columns.DateTime(primary_key=True, clustering_order='DESC')
	typ = columns.Text(partition_key=True)
	msg = columns.Text(required=False)

class Store01(Model):
	eui = columns.Text(partition_key=True)
	tms = columns.DateTime(primary_key=True, clustering_order='DESC')
	fid = columns.Integer(required=True)
	rcid = columns.Text(partition_key=True)
	sdid = columns.Text(partition_key=True)
	typ = columns.Text(partition_key=True)
	msg = columns.Text(required=False)
