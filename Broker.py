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
        self.data_condition = threading.Condition()
        self.client_condition = threading.Condition()
        self.lock = threading.Lock()

        #variables
        self.clients = []
        self.status = False
        self.period = period
        self.tcurrency = ['BRENTCMDUSD', 'BTCUSD', 'EURUSD', 'GBPUSD', 'USA30IDXUSD', 'USA500IDXUSD', 'USATECHIDXUSD', 'XAGUSD', 'XAUUSD',]
        self.data = {}

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

        self.client_status()
        
        #Esperar a recibir datos
        with self.data_condition:
            self.data_condition.wait()

        #Envio de datos al cliente
        client_connection.send(json.dumps(self.data).encode())

        with self.data_condition:
            self.data_condition.wait()


        print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
        self.clients.remove(threading.current_thread())
        client_connection.close()

    def handler_markets(self, currency):
        market_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        market_socket.connect((self.server_address, self.market_port))
        market_socket.send(b'currency: '+currency.encode())
        time.sleep(0.0001)
        market_socket.send(b'period: '+self.period.encode())

        #Espera a que se conecten clientes
        with self.client_condition:
            self.client_condition.wait()

        market_socket.send(b'send')

        data = market_socket.recv(self.buffer).decode()
        while not data.startswith("data:"):
            data = market_socket.recv(self.buffer).decode()
        
        #Seccion critica, se almacenan los datos en la variable self.data
        self.lock.acquire()
        self.data[currency] = data.split('data:')[1]
        self.lock.release()

        #Avisa a los clientes que se van a enviar datos
        with self.data_condition:
            self.data_condition.notify_all()
            time.sleep(0.0001)

    #Determinar si hay conexiones
    #Si ya habian conexiones recibe los datos, si no, envia la señal para empezar a recibirlos
    def client_status(self):

        if self.status == True:
            None
        elif len(self.clients) > 0:
            with self.client_condition:
                self.status = True
                self.client_condition.notify_all()
                time.sleep(0.0001)
        else:
            self.status = False
        
        
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