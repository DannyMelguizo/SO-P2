import socket

server_address = "localhost"
server_port = 50000
tuple_connection = (server_address, server_port)

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.connect(tuple_connection)

    data = input()

    while data:
        server_socket.send(data.encode())
        data = input()


    
main()