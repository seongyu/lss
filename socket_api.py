from websocket_server import WebsocketServer
import json, _thread, time
PORT=9100
HOST="0.0.0.0"
server = WebsocketServer(host=HOST, port=PORT)

def new_client(client, server):
  print("New client connected and was given id %d" % client['id'])

def send_message_to_all(orr):
  server.send_message_to_all(json.dumps(orr))


def client_left(client, server):
  print("Client(%d) disconnected" % client['id'])



# def message_received(client, server, message):
#   msg = json.loads(message)
#   server.send_message(client,json.dumps({
#     'status':'OK',
#     'get count':msg['count'],
#     'sended message':msg['message']
#     }))


def run_socketServer(name):
  server.set_fn_new_client(new_client)
  server.set_fn_client_left(client_left)
  # server.set_fn_message_received(message_received)
  print('start socket server now')
  server.serve_forever()


print('ready to start...')

try :
  _thread.start_new_thread(run_socketServer, ('run socket',))
  # run_socketServer('test')
except Exception as err :
  print(err)