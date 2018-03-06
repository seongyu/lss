from datetime import date, timedelta

def get_date(term):
  if term == 'day' :
    dts = (date.today()+ timedelta(days=-1)).strftime('%Y-%m-%d')
  elif term == 'week' :
    dts = (date.today()+ timedelta(weeks=-1)).strftime('%Y-%m-%d')
  elif term == 'month':
    dts = (date.today()+ timedelta(days=-31)).strftime('%Y-%m-%d')
  return dts

def get_arr(r):
  arr = []

  while r.has_more_pages :
    arr.extend(r.current_rows)
    r.fetch_next_page()

  if len(r.current_rows) > 0 :
    arr.extend(r.current_rows)

  return arr

def take_graph_items(rows):
  rt_val = []
  ran = 20

  if len(rows) > ran :
    arr_length = int(len(rows)/20)
  else :
    ran = len(rows)
    arr_length = 1

  for i in range(ran) :
    item = rows[(i*arr_length)].asDict()
    item['tms'] = item['tms'].strftime('%Y-%m-%d %H:%M:%S')
    rt_val.append(item)

  return rt_val

def take_graph_items_v2(rows):
  rt_val = []
  ran = 20

  if len(rows) > ran :
    arr_length = int(len(rows)/20)
  else :
    ran = len(rows)
    arr_length = 1

  for i in range(ran) :
    item = rows[(i*arr_length)]
    item['tms'] = item['tms'].strftime('%Y-%m-%d %H:%M:%S')
    rt_val.append(item)

  return rt_val