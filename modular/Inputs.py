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