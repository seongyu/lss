import config
from util import global_fn as fn
from cassandra.cqlengine import connection
from datetime import date, timedelta, datetime

import pyspark 

sparkconf = pyspark.SparkConf().setAll([
  ('spark.executor.cores','1'),
  ('spark.executor.memory','2g'),
  ('spark.cores.max', '1'),
  ('spark.driver.memory','2g')])

# spark = SparkSession.builder.appName('queryfy').config(conf=sparkconf).getOrCreate()
spark = pyspark.SparkContext(conf=sparkconf)

WPORT = 8101
WHOST = '0.0.0.0'

CONN_NM = 'analizer'
KEYSPACE = 'lora_streaming_t'

# config.DTP = 'D' # for DEVELOP

Query = {
  'get_term_stats' : 'select * from store01 where fid=12 and typ=\'stat\' and sdid=%s and tms >= %s allow filtering',
  'get_fromto_stats' : 'select * from store01 where fid=12 and typ=\'stat\' and sdid=%s and tms >= %s and tms <= %s allow filtering',
  'get_stats' : 'select * from store01 where fid=12 and typ=\'stat\' and tms >= %s allow filtering',
  'get_flow_map' : 'select * from store01 where ogtg = %s and tms >= %s allow filtering'
}

def db_set(keyspace):
  try:
    connection.set_default_connection(CONN_NM)
  except Exception as err:
    print('db set exception occured...')
    connection.unregister_connection(CONN_NM)
    connection.register_connection(CONN_NM, config.CASSANDRA_CONTACT_POINTS[config.DTP], default=True)
    connection.session.set_keyspace(keyspace)
    print('...fix db connection. return to process')

def get_flow_map(term, eui):
  db_set(KEYSPACE)
  
  rt_val = []
  dt = fn.get_date(term)
  r = connection.session.execute(Query['get_flow_map'],[eui,dt])
  arr = fn.get_arr(r)

  if len(arr) <= 0 :
    return rt_val
  
  rdd = spark.parallelize(arr)
  rows = rdd.groupBy(lambda x: (x['fid'],x['rcid'],x['sdid'])).map(lambda x: (x[0], len(x[1]))).collect()

  for row in rows :
    item = {
      'fid': row[0][0],
      'rcid': row[0][1],
      'sdid': row[0][2],
      'count': row[1]
    }
    rt_val.append(item)

  rdd.unpersist()
  return rt_val

def get_stats():
  db_set(KEYSPACE)

  rt_val = []
  dt = fn.get_date('week')
  r = connection.session.execute(Query['get_stats'],[dt])
  arr = fn.get_arr(r)

  if len(arr) <= 0 :
    return rt_val

  rdd = spark.parallelize(arr)
  rows = rdd.sortBy(lambda x: x['tms'], False).groupBy(lambda x : x['ogtg']).collect()

  for row in rows :
    item = row[1].data[0]
    item['tms'] = item['tms'].strftime('%Y-%m-%d %H:%M:%S')
    rt_val.append(item)
  rdd.unpersist()
  return rt_val

def get_gf_dt_term(term, eui):
  db_set(KEYSPACE)

  rt_val = []
  dt = fn.get_date(term)
  r = connection.session.execute(Query['get_term_stats'],[eui, dt])
  arr = fn.get_arr(r)

  if len(arr) <= 0 :
    return rt_val

  rdd = spark.parallelize(arr)
  rt_val = fn.take_graph_items_v2(rdd.sortBy(lambda x : x['tms'], False).collect())

  rdd.unpersist()
  return rt_val

def get_gf_dt_from_to(f, t, eui):
  db_set(KEYSPACE)

  rt_val = []
  f = f + ' 00:00:00'
  t = t + ' 23:59:59'
  from_dt = datetime.strptime(f,'%Y-%m-%d %H:%M:%S')
  to_dt = datetime.strptime(t,'%Y-%m-%d %H:%M:%S')

  r = connection.session.execute(Query['get_fromto_stats'],[eui, from_dt, to_dt])
  arr = fn.get_arr(r)

  if len(arr) <= 0 :
    return rt_val

  rdd = spark.parallelize(arr)
  rt_val = fn.take_graph_items_v2(rdd.sortBy(lambda x : x['tms'], False).collect())
  
  rdd.unpersist()
  return rt_val

# for HTTP API
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(app, origins="*")

class GET_STAT(Resource):
  def get(self):
    rows = get_stats()
    return rows

class GET_LIST_STAT(Resource):
  def get(self, term, eui):
    rows = get_gf_dt_term(term, eui)
    return rows

class GET_FROM_TO_STAT(Resource):
  def get(self, f, t, eui):
    rows = get_gf_dt_from_to(f, t, eui)
    return rows

class GET_FLOW_MAP(Resource):
  def get(self, term, eui):
    rows = get_flow_map(term, eui)
    return rows


api.add_resource(GET_FLOW_MAP, '/map/<term>/<eui>')

api.add_resource(GET_FROM_TO_STAT, '/stat/term/<f>/<t>/<eui>')
api.add_resource(GET_LIST_STAT, '/stat/<term>/<eui>')
api.add_resource(GET_STAT, '/stat')

if __name__ == '__main__':

  app.run(host=WHOST,port=WPORT)