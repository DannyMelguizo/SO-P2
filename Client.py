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


def trading(currency, positionx, positiony):
    global dictionary, main_axes, main_fig

    content = {"Open" : [], "High" : [], "Low" : [], "Close" : []}
    date = []
    df = None

    while True:

        with data_condition:
            data_condition.wait()

        if currency in dictionary:

            data = dictionary[currency]

            date.append(data['Date'])

            for key in fields:
                content[key].append(data[key])

            df = pd.DataFrame(content, index=date)
            df.index.name = 'Date'
            
            df.index = pd.to_datetime(df.index)

            lock.acquire()
            mpf.plot(df, **pkwargs, axtitle=f"Market {currency}", ax=main_axes[positionx, positiony])
            plt.draw()
            lock.release()
            
        else:
            continue


def main():
    global dictionary, main_fig

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(tuple_connection)
    


    BRENTCMDUSD = threading.Thread(target=trading, args=("BRENTCMDUSD", 0, 0))  #trading("BRENTCMDUSD", 0, 0)
    BTCUSD = threading.Thread(target=trading, args=("BTCUSD", 0, 1))  #trading("BTCUSD", 0, 1)
    EURUSD = threading.Thread(target=trading, args=("EURUSD", 0, 2))  #trading("EURUSD", 0, 2)
    GBPUSD = threading.Thread(target=trading, args=("GBPUSD", 1, 0))  #trading("GBPUSD", 1, 0)
    USA30IDXUSD = threading.Thread(target=trading, args=("USA30IDXUSD", 1, 1))  #trading("USA30IDXUSD", 1, 1)
    USA500IDXUSD = threading.Thread(target=trading, args=("USA500IDXUSD", 1, 2))  #trading("USA500IDXUSD", 1, 2)
    USATECHIDXUSD = threading.Thread(target=trading, args=("USATECHIDXUSD", 2, 0))  #trading("USATECHIDXUSD", 2, 0)
    XAGUSD = threading.Thread(target=trading, args=("XAGUSD", 2, 1))  #trading("XAGUSD", 2, 1)
    XAUUSD = threading.Thread(target=trading, args=("XAUUSD", 2, 2))  #trading("XAUUSD", 2, 2)

    BRENTCMDUSD.daemon = True
    BTCUSD.daemon = True
    EURUSD.daemon = True
    GBPUSD.daemon = True
    USA30IDXUSD.daemon = True
    USA500IDXUSD.daemon = True
    USATECHIDXUSD.daemon = True
    XAGUSD.daemon = True
    XAUUSD.daemon = True

    BRENTCMDUSD.start()
    BTCUSD.start()
    EURUSD.start()
    GBPUSD.start()
    USA30IDXUSD.start()
    USA500IDXUSD.start()
    USATECHIDXUSD.start()
    XAGUSD.start()
    XAUUSD.start()

    while True:

        data = server_socket.recv(buffer).decode()
        while data == '':
            data = server_socket.recv(buffer).decode()

        dictionary = json.loads(data)

        plt.pause(0.0001)
        plt.tight_layout()
        plt.show()

        with data_condition:
            data_condition.notify_all()
            time.sleep(0.001)

        server_socket.send(b'confirm')


main()