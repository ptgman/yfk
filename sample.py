# sample program
import yfinance as yf

ko = yf.Ticker('KO')
ko_hist = ko.history(period='max', interval='1mo', start='2019-01-01', end='2019-09-30')

print(ko_hist.loc['2019-03-01'])
