import socket
import json
import threading
import time
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

server_address = "localhost"
server_port = 50000
tuple_connection = (server_address, server_port)
buffer = 2048

#Data storage
dictionary = None


#Variables
fields = ["Open", "High", "Low", "Close"]
tcurrency = ['BRENTCMDUSD', 'BTCUSD', 'EURUSD', 'GBPUSD', 'USA30IDXUSD', 'USA500IDXUSD', 'USATECHIDXUSD', 'XAGUSD', 'XAUUSD',]
mc = mpf.make_marketcolors(up='g', down='r')
colors = mpf.make_mpf_style(marketcolors=mc)
pkwargs=dict(type='candle', mav=(5,13), style=colors)
thread_count = 0

main_fig, main_axes = plt.subplots(3,3)
plt.ion()

#Conditions
data_condition = threading.Condition()
lock = threading.Lock()


class trading():
    def __init__(self, currency, positionx, positiony):
        self.positionx = positionx
        self.positiony = positiony
        self.currency = currency
        self.content = {"Open" : [], "High" : [], "Low" : [], "Close" : []}
        self.date = []
        self.df = None

    def add_data(self):
        data = json.loads(dictionary[self.currency])
        self.date.append(data['Date'])

        for key in fields:
            self.content[key].append(data[key])

        self.df = pd.DataFrame(self.content, index=self.date)
        self.df = self.df.drop_duplicates()
        self.df.index.name = 'Date'
        
        self.df.index = pd.to_datetime(self.df.index)

    def plot(self):
        mpf.plot(self.df, **pkwargs, ax=main_axes[self.positionx, self.positiony])
        plt.draw()
        plt.pause(0.0001)


def main():
    global dictionary, main_fig

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.connect(tuple_connection)
    
    BRENTCMDUSD = trading("BRENTCMDUSD", 0, 0)
    BTCUSD = trading("BTCUSD", 0, 1)
    EURUSD = trading("EURUSD", 0, 2)
    GBPUSD = trading("GBPUSD", 1, 0)
    USA30IDXUSD = trading("USA30IDXUSD", 1, 1)
    USA500IDXUSD = trading("USA500IDXUSD", 1, 2)
    USATECHIDXUSD = trading("USATECHIDXUSD", 2, 0)
    XAGUSD = trading("XAGUSD", 2, 1)
    XAUUSD = trading("XAUUSD", 2, 2)

    while True:

        data = server_socket.recv(buffer).decode()
        while data == '':
            data = server_socket.recv(buffer).decode()

        dictionary = json.loads(data)

        BRENTCMDUSD.add_data()
        BTCUSD.add_data()
        EURUSD.add_data()
        GBPUSD.add_data()
        USA30IDXUSD.add_data()
        USA500IDXUSD.add_data()
        USATECHIDXUSD.add_data()
        XAGUSD.add_data()
        XAUUSD.add_data()


        BRENTCMDUSD.plot()
        BTCUSD.plot()
        EURUSD.plot()
        GBPUSD.plot()
        USA30IDXUSD.plot()
        USA500IDXUSD.plot()
        USATECHIDXUSD.plot()
        XAGUSD.plot()
        XAUUSD.plot()

        plt.tight_layout()
        plt.show()

        server_socket.send(b'confirm')


main()