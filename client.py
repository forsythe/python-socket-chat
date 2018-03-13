from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
	PORT = 33002
else:
	PORT = int(PORT)

if not HOST:
	HOST = 'localhost'

BUFSIZ = 1024
SERVER_ADDR = (HOST, PORT)

def receive():
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode()
			print(msg)
		except OSError:
			break

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(SERVER_ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

while True:
	msg = input()
	client_socket.send(msg.encode())

	if msg == ".QUIT":
		client_socket.close()
		break

print("See you again soon!")