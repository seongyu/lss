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

if __name__ == '__main__':
  arr = get_flow_map('week','3139393930303033')
  print(arr)
