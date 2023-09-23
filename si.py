import pandas as pd

rows = ["Date", "Open", "High", "Low", "Close", "Volume"]
nrows = 100
url = 'BTCUSD/BTCUSD_H1.csv'

actual =  0

df = pd.read_csv(url, parse_dates=True, index_col=0, names=rows, nrows=nrows)


szs = df.to_dict(orient='index')

print(next(iter(szs.items())))