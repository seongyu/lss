from websocket_server import WebsocketServer
import json, _thread, time
PORT=9100

clients = []
server = WebsocketServer(PORT)

def new_client(client, server):
  print("New client connected and was given id %d" % client['id'])
  clients.append(client)

def send_message_cli(arr):
  for cli in clients :
    server.send_message(cli,json.dumps(arr))


def client_left(client, server):
  clients.remove(client)
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
  server.run_forever()

_thread.start_new_thread(run_socketServer, ('run socket',))