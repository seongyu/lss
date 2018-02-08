from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Store00(Model):
	pid = columns.Text(partition_key=True)
	tms = columns.DateTime(primary_key=True, clustering_order='DESC')
	cid = columns.Text(required=True)
	fid = columns.Integer(required=True)
	rcid = columns.Text(required=True)
	sdid = columns.Text(required=True)
	typ = columns.Text(required=True)
	msg = columns.Text(required=False)	
	ttk = columns.Text(required=True)

class Store01(Model):
	pid = columns.Text(partition_key=True)
	tms = columns.DateTime(primary_key=True, clustering_order='DESC')
	cid = columns.Text(required=True)
	fid = columns.Integer(required=True)
	ogtg = columns.Text(required=True)
	rcid = columns.Text(required=True)
	sdid = columns.Text(required=True)
	typ = columns.Text(required=True)
	msg = columns.Text(required=False)	
	ttk = columns.Text(required=True)

