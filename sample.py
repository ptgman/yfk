# sample program
import yfinance as yf

ko = yf.Ticker('KO')
# ko_hist = ko.history(start='2015-01-20', end='2015-01-20', interval='1d', period='max', auto_adjust=False)
ko_hist = ko.history(start='2015-01-21', end='2015-01-21', interval='1d', period='max', auto_adjust=False)
# print(ko_hist)
# print(ko_hist.loc['2015-01-20'])
