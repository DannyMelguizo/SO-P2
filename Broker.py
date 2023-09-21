import argparse
import socket
import threading
import random
import time

class Broker():
    def __init__(self, period):
        self.period = period
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = "localhost"
        self.server_port = 50000
        self.buffer = 1024
        self.tuple_connection = (self.server_address, self.server_port)
        self.market_port = 51000
        
        self.tcurrency = ['BRENTCMDUSD', 
                          'BTCUSD', 
                          'EURUSD', 
                          'GBPUSD', 
                          'USA30IDXUSD', 
                          'USA500IDXUSD', 
                          'USATECHIDXUSD',
                          'XAGUSD',
                          'XAUUSD',]
        
        #Se selecciona una moneda aleatoria y se llama al mercado
        currency = random.choice(self.tcurrency)
        self.handler_markets(currency)


        print(f"Broker running.\nDir IP: {self.server_address}\nPORT: {self.server_port}")

        self.server_socket.bind(self.tuple_connection)
        self.server_socket.listen()
        print("Broker is listening...")

        while True:
            client_connection , client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handler_client, args=(client_connection, client_address))
            client_thread.start()
    
    #Gestiona la conexion del cliente
    def handler_client(self, client_connection, client_address):
        print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')

        while True:
            data = client_connection.recv(self.buffer).decode()

            if data.startswith("Data:"):
                print(data)

            if data == "QUIT":
                break

        print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
        client_connection.close()

    def handler_markets(self, currency):

        self.market_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.market_socket.connect((self.server_address, self.market_port))
        
        self.market_socket.send(b'currency: '+currency.encode())
        time.sleep(0.001)
        self.market_socket.send(b'period: '+self.period.encode())
        
        


def main(args):
    if args.period != None:
        period = args.period.upper()
    else:
        period = "H1"

    do = Broker(period)

    print(f'\nstatus: {do}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--period", type=str, help="Period of time")
    args = parser.parse_args()
    main(args)