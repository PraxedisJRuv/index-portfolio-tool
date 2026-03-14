#This test was discarded since yhfinance API seems to have many bugs and glitches
#It wouldn't allow me to request data more than twice per week, which won't work for what I intend to
import yfinance as yf
import pandas as pd
import numpy as np

#First module
tickers = ["AAPL", "MSFT", "NVDA", "AMZN"]
#EW for testing
weights = np.array([0.25, 0.25, 0.25, 0.25])
data = yf.download(tickers, period="1d", interval="1m")["Close"]

base_value = 100
normalized = data / data.iloc[0]
#EW
index_series = (normalized * weights).sum(axis=1) * base_value


#Second module
import time
from datetime import datetime
STOP_TIME = "12:50"   # time to stop (24h format)

while True:

    now = datetime.now().strftime("%H:%M")

    if now >= STOP_TIME:
        print("Stopping index calculation.")
        break

    data = yf.download(tickers, period="1d", interval="1m")["Close"]
    normalized = data / data.iloc[0]
    index_series = (normalized * weights).sum(axis=1) * 100

    print(index_series.tail(1))

    time.sleep(60)
    import matplotlib.pyplot as plt

index_series.plot(title="My Custom Index")
plt.show()