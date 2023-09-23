import pandas as pd
import argparse
import mplfinance as mpf
import matplotlib.animation as animation

class RealTimeAPI():

    def __init__(self, df):
        self.data_pointer = 0
        self.data_frame = df
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        self.data_pointer += 1
        if self.data_pointer >= self.df_len:
            return None
        return self.data_frame.iloc[self.data_pointer]
    
    def initial_fetch(self):
        if self.data_pointer > 0:
            return
        return self.data_frame.iloc[0:self.data_pointer+1]
    
class japanese_candlestick():

    def animate(self, empty):
        nxt = self.rtapi.fetch_next()
        if nxt is None:
            return
        
        self.df = self.df.append(nxt)
        self.rs = self.df.resample(self.resample_period).agg(self.resample_map).dropna()
        self.ax.clear()
        mpf.plot(self.rs, ax=self.ax, **self.pkwargs)
                
    def __init__(self, content, currency):
        self.content = content
        self.currency = currency

        self.mc = mpf.make_marketcolors(up='g', down='r')
        self.colors = mpf.make_mpf_style(marketcolors=self.mc)

        self.pkwargs=dict(type='candle', mav=(5,13), style=self.colors, ylabel=f'Price ({self.currency})')

        self.rtapi = RealTimeAPI(self.content)
        self.resample_map = {'Open':'first', 'High':'max', 'Low':'min', 'Close':'last' }
        self.resample_period = '10T'

        self.df = self.rtapi.initial_fetch()
        self.rs = self.df.resample(self.resample_period).agg(self.resample_map).dropna()

        self.fig , self.axes = mpf.plot(self.rs, returnfig=True, **self.pkwargs)
        self.ax = self.axes[0]

        ani = animation.FuncAnimation(self.fig, self.animate, interval=100)
        mpf.show()
    
def file(period, format, currency):
    
    name = currency + '_' + period.upper() + '.' + format

    return name

def simtrading(file_name, format, currency, period):

    try:

        rows = ["Date", "Open", "High", "Low", "Close", "Volume"]
        nrows = 100

        content = pd.read_csv(file_name, parse_dates=True, index_col=0, names=rows, nrows=nrows)
    
    except:

        print("An error has ocurred while we tried to open the file.")

        return 1

    japanese_candlestick(content, currency)

    return 0

def main(args):
    if args.currency != None and args.period != None and args.format != None:
        currency = args.currency
        period = args.period
        format = args.format
        currency = currency.upper()
        format = format.lower()

        name = file(period, format, currency)

        do = simtrading(name, format, currency, period)

        print(f'\nstatus: {do}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--period", type=str, help="Period of time")
    parser.add_argument("-f", "--format", type=str, help="File format")
    parser.add_argument("-m", "--currency", type=str, help="Currency")
    args = parser.parse_args()
    main(args)
