import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(connection, address):
    print("[NEW CONNECTION] {} connected.".format(address))

    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print("[{}] {}".format(address, msg))
            connection.send("Message received".encode(FORMAT))

    connection.close()


def start():
    server.listen()
    print("[LISTENING] Server is listening on {}".format(SERVER))
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print("[ACTIVE CONNECTIONS] {}".format(threading.activeCount() - 1))


print("[STARTING] server is starting...")
start()
