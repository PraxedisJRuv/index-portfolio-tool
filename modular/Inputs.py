#the attempt was genuine, but it turns out, this is gonna be much more complicated, so far, this hasn't been used. 
#It works, the extraction part, actually does work with this.
import pandas as pd
from extraction import full_dataframe_extraction
import benchmarks
print("How many actions?")
n=int(input())
print("which ones? (remeber the tickers have to end in .CO country initials)")
tickers=[]
for i in range(n):
    tickers.append(str(input()))
print("Which start date? (has to be format yyyymmdd)")
start_date=int(input())
print("Which end date? (has to be format yyyymmdd)")
end_date=int(input())
print("Which rebalancing period?")
period=str(input())

df=full_dataframe_extraction(tickers, start_date, end_date)
print(df)