from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

clients = {}
addresses = {}

HOST = ''
PORT = 33002
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
	# Sets up handling for incoming clients.
	while True:
		client, client_address = SERVER.accept()
		print("{} connecting...".format(client_address))
		client.send("Enter username: ".encode())
		addresses[client] = client_address
		
		#func in new thread
		Thread(target=handle_client, args=(client,)).start() 

def handle_client(client):  # Takes client socket as argument.
	# Handles a single client connection.
	name = client.recv(BUFSIZ).decode()
	
	client.send("Welcome {}! Type .QUIT (or CTRL-C) to quit".format(name).encode())
	incoming_msg = "{} connected as {}.".format(client.getpeername(),name)
	print(incoming_msg)
	broadcast(incoming_msg)
	clients[client] = name
	print([v for k, v in clients.items()])

	while True:
		msg = client.recv(BUFSIZ).decode()
		if msg.strip() != ".QUIT" and msg.strip() != '':
			broadcast(msg, prefix=name+": ")
		elif not msg:
			#client.send(".QUIT".encode())
			client.close()
			del clients[client]
			dc_msg = "{} disconnected.".format(name)
			print(dc_msg)
			broadcast(dc_msg)
			break

def broadcast(msg, prefix=""):  # prefix is for name identification.
	# Broadcasts a message to all the clients.
	for sock, name in clients.items():
		completeMsg = prefix+msg
		sock.send(completeMsg.encode())	
		
		
if __name__ == "__main__":
	SERVER.listen(5)  # Listens for 5 connections at max.
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()  # Starts the infinite loop.
	ACCEPT_THREAD.join()
	SERVER.close()