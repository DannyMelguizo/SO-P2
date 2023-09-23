import socket
import threading
import pandas as pd
import json

class Mercado():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = "localhost"
        self.server_port = 51000
        self.buffer = 1024
        self.tuple_connection = (self.server_address, self.server_port)

        self.rows = ["Date", "Open", "High", "Low", "Close", "Volume"]
        self.nrows = 100
        
        print(f"Market running.\nDir IP: {self.server_address}\nPORT: {self.server_port}")

        self.server_socket.bind(self.tuple_connection)
        self.server_socket.listen()
        print("Market is listening...")

        while True:
            client_connection , client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handler_client, args=(client_connection, client_address))
            client_thread.start()
    
    def handler_client(self, client_connection, client_address):
        print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
        currency = ''
        period = ''
        current = 0
        start = 0

        while True:
            data = client_connection.recv(self.buffer).decode()

            while not data.startswith("currency:"):
                data = client_connection.recv(self.buffer).decode()
            
            currency = data.split(' ')[1]

            data = client_connection.recv(self.buffer).decode()
            while not data.startswith("period:"):
                data = client_connection.recv(self.buffer).decode()
            
            period = data.split(' ')[1]

            file = f'{currency}/{currency}_{period}.csv'

            content = pd.read_csv(file, parse_dates=True, names=self.rows, skiprows=range(0,start), nrows=self.nrows)

            print(f"I'm waiting for a signal to send data: {client_address[1]}")

            data = client_connection.recv(self.buffer).decode()
            while not data.startswith("send"):
                data = client_connection.recv(self.buffer).decode()

            data = content.iloc[current]

            data = data.to_dict()

            data = json.dumps(data)

            client_connection.send(b'data:'+data.encode())

            

            

        print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
        client_connection.close()
        


def main():

    do = Mercado()

    print(f'\nstatus: {do}')


main()