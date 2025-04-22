import parser
import logging
from websocket_server import WebsocketServer

# Called for every client connecting (after handshake)
def new_client(client, server):
	server.deny_new_connections()
	print("New client connected and was given id %d" % client['id'])
	server.send_message(client, "Hello! How can I assist you?")

# Called for every client disconnecting
def client_left(client, server):
	server.allow_new_connections()
	print("Client(%d) disconnected" % client['id'])

# Called when a client sends a message
def message_received(client, server, message):
	response = parser.handle(message)
	if response is not None:
		server.send_message(client, response)
	if len(message) > 200:
		message = message[:200]+'..'
	print("Client(%d) said: %s" % (client['id'], message))

server = WebsocketServer(host='', port=9001, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
parser.handle("LED n")
server.run_forever()
