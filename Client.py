import socket
import json
import pandas as pd

server_address = "localhost"
server_port = 50000
tuple_connection = (server_address, server_port)
buffer = 1024

#Donde se almacenan los datos recibidos
dictionary = None

#Dataframes
df_brentcmdusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_btcusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_eurusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_gbpusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_usa30idxusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_usa500idxusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_usatechidxusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_xagusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}
df_xauusd = {"Date": [], "Open" : [], "High" : [], "Low" : [], "Close" : [], "Volume" : []}


fields = ["Date", "Open", "High", "Low", "Close", "Volume"]

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.connect(tuple_connection)

    while True:
        data = server_socket.recv(buffer).decode()
        while data == '':
            data = server_socket.recv(buffer).decode()

        dictionary = data.replace('\\', '')
        print(dictionary)

        print(json.loads(dictionary))
        
        # for key in fields:
        #     df_xagusd[key] = df_xagusd[key] + json.loads(dictionary['XAUUSD'])[key]



main()