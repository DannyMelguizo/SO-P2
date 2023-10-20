import argparse
import socket
import threading
import time
import json

class Broker():
    def __init__(self, period):
        #server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = "localhost"
        self.server_port = 50000
        self.tuple_connection = (self.server_address, self.server_port)
        self.buffer = 1024

        #market connection
        self.market_port = 51000

        #conditions
        self.client_condition = threading.Condition()
        self.lock = threading.Lock()

        #variables
        self.clients = []
        self.active_clients = 0
        self.status = False
        self.period = period
        self.tcurrency = ["BRENTCMDUSD", "BTCUSD", "EURUSD", "GBPUSD", "USA30IDXUSD", "USA500IDXUSD", "USATECHIDXUSD", "XAGUSD", "XAUUSD",]
        self.data = {}
        self.confirm_clients = 0
        self.confirm_markets = 0

        try:
            open("archivo.txt", 'x').close()
        except:
            open("archivo.txt", 'w').close()


        print("Starting markets...")
        for c in self.tcurrency:
            h = threading.Thread(target=self.handler_markets, args=(c,))
            h.start()


        print(f"Broker running.\nDir IP: {self.server_address}\nPORT: {self.server_port}")

        self.server_socket.bind(self.tuple_connection)
        self.server_socket.listen()
        print("Broker is listening...")

        while True:
            client_connection , client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handler_client, args=(client_connection, client_address))
            self.clients.append(client_thread)
            client_thread.start()
            
    
    #Gestiona la conexion del cliente
    def handler_client(self, client_connection, client_address):
        print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
        current = 0

        try:
            while True:
                with self.client_condition:
                    self.client_condition.notify_all()
                    time.sleep(0.0001)

                time.sleep(0.0001)
                
                with open("archivo.txt", 'r') as archivo:

                    file = archivo.readlines()

                    data = file[current]

                    client_connection.send(data.encode())
                    time.sleep(0.001)

                    data = client_connection.recv(self.buffer).decode()
                    while not data.startswith("confirm"):
                        data = client_connection.recv(self.buffer).decode()

                    current += 1

            print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')

        except ConnectionResetError:
            print(f"Client {client_address[0]}:{client_address[1]} unexpectedly disconected.")
        except Exception as e:
            print(f"Error {client_address[0]}:{client_address[1]} - {str(e)}")


        

    def handler_markets(self, currency):
        market_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        market_socket.connect((self.server_address, self.market_port))
        market_socket.send(b'currency: '+currency.encode())
        time.sleep(0.0001)
        market_socket.send(b'period: '+self.period.encode())


        while True:
            #Espera a que se conecten clientes
            with self.client_condition:
                self.client_condition.wait()
            
            while True:

                market_socket.send(b'send')

                data = market_socket.recv(self.buffer).decode()
                while not data.startswith("data:"):
                    data = market_socket.recv(self.buffer).decode()
                
                #Seccion critica, se almacenan los datos en el archivo
                self.lock.acquire()
                with open("archivo.txt", 'a') as archivo:
                    dt = {currency: eval(data.split('data:')[1])}
                    dt = str(dt).replace("'", '"')

                    archivo.write(dt+'\n')
                self.lock.release()


        
        
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