import socket
import json
import threading
import pandas as pd
import mplfinance as mpf
import argparse
import matplotlib.pyplot as plt

server_address = "localhost"
server_port = 50000
tuple_connection = (server_address, server_port)
buffer = 2048

#Data storage
dictionary = None


#Variables
fields = ["Open", "High", "Low", "Close"]
mc = mpf.make_marketcolors(up='g', down='r')
colors = mpf.make_mpf_style(marketcolors=mc)
pkwargs=dict(type='candle', mav=(5,13), style=colors)
thread_count = 0

main_fig = main_axes = 0
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
            try:
                mpf.plot(df, **pkwargs, axtitle=f"Market {currency}", ax=main_axes[positionx, positiony])
            except:
                mpf.plot(df, **pkwargs, axtitle=f"Market {currency}", ax=main_axes[positiony])
            plt.draw()
            lock.release()
            
        else:
            continue


def main(currencies):
    global dictionary, main_fig, main_axes

    amount_currencies = len(currencies)/3 + 0.4
    n_rows = round(amount_currencies)

    main_fig, main_axes = plt.subplots(n_rows,3)
    plt.ion()

    posx = 0
    posy = 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(tuple_connection)

    for c in currencies:
        c = threading.Thread(target=trading, args=(c, posx, posy))
        c.start()
        posy += 1
        if posy == 3:
            posy = 0
            posx += 1
    
    server_socket.send(str(currencies).encode())

    while True:

        data = server_socket.recv(buffer).decode()
        while data == '':
            data = server_socket.recv(buffer).decode()

        data = data.replace("'", '"')
        dictionary = json.loads(data)

        plt.pause(0.00001)
        plt.tight_layout()
        plt.show()

        with data_condition:
            data_condition.notify_all()

        server_socket.send(b'confirm')


def initialize(args):
    currencies = args.currencies

    do = main(currencies)

    print(f'\nstatus: {do}')    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--currencies", type=str.upper, choices=["BRENTCMDUSD", "BTCUSD", "EURUSD", "GBPUSD", "USA30IDXUSD", "USA500IDXUSD", "USATECHIDXUSD", "XAGUSD", "XAUUSD"], default=["BRENTCMDUSD", "BTCUSD", "EURUSD", "GBPUSD", "USA30IDXUSD", "USA500IDXUSD", "USATECHIDXUSD", "XAGUSD", "XAUUSD"], nargs= '+',help="Currencies that you want to see")
    args = parser.parse_args()
    initialize(args)