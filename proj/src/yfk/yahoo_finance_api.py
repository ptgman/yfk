#1111111112222222222333333333344444444445555555555666666666677777777778888888888
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
import sys, os
import numpy as np
import pandas as pd
import yfinance as yf
from yfk.config import OUTPUT_DIR

class YahooFinanceApi:
    def __init__(self, code):
        self._code = code

    def _get_dividends(self, hist):
        '''
        ヒストリーデータから'Dividends'が0.0でないデータを取得し、
        DividendsのSeriesとして返す
        '''
        dividends =pd.Series({i:v for i,v in hist.loc[:,'Dividends'].
            iteritems() if v != 0.0})

        return dividends

    def _get_splits(self, hist):
        '''
        ヒストリーデータから'Stock Splits'が0でないデータを取得し、
        Stock SplitsのSeriesとして返す
        '''
        splits =pd.Series({i:v for i,v in hist.loc[:,'Splits'].
            iteritems() if v != 0.0})

        return splits

    def _merge(self, hist, dividends, splits):
        '''
        1.ヒストリーからDividendsとStock Splitsの行を削除する
        2.ヒストリーにDividends/Stock Splits情報表示カラムを付け足す
        3.dividendsとsplitsを追加カラムに移す
        '''
        hist = hist.query('Dividends == 0.0 and Splits == 0.0').loc[:,'Open':'Volume']
        hist['Date_Div'] = ''
        hist['Dividends'] = ''
        hist['Date_Spli'] = ''
        hist['Stock_Splits'] = ''

        # Dividendsの移動
        for i, v in dividends.iteritems(): # i)日付 v)Dividend
            now_date = i.split('/')
            first_date = now_date[0] + '/' + now_date[1].rjust(2, '0') + '/01'
            hist.loc[first_date, 'Date_Div'] = i
            hist.loc[first_date, 'Dividends'] = str(v)

        # Stock Splitsの移動
        for i, v in splits.iteritems():
            now_date = i.split('/')
            first_date = now_date[0] + '/' + now_date[1].rjust(2, '0') + '/01'
            hist.loc[first_date, 'Date_Spli'] = i
            hist.loc[first_date, 'Stock_Splits'] = str(v)

        hist.index.name = 'Date'

        return hist

    def max(self, output_dir):
        '''
        output_dir: CSVファイル出力ディレクトリ(YYYYMMDD_hhmmss)の絶対パス
        '''
        ticker = yf.Ticker(self._code)
        hist = ticker.history(period='max', interval='1mo', auto_adjust=False)
        hist.index = [d.strftime("%Y/%m/%d") for d in hist.index]
        hist = hist.rename(columns={'Stock Splits':'Splits'})
        dividends = self._get_dividends(hist)
        splits = self._get_splits(hist)

        hist = self._merge(hist, dividends, splits)

        output_file = os.path.join(output_dir,
                '{code}.csv'.format(code=self._code))
        hist.to_csv(output_file)

        # dividends.to_csv('dividends.csv')
        # splits.to_csv('splits.csv')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('引数の数が違います。')
        print('最低1個の銘柄コードを指定して下さい。')
        print('python {} コード1[,コード2,コード3...]'.format(__file__))
        sys.exit()

    for i in range(1, len(sys.argv)):
        yfa = YahooFinanceApi(sys.argv[i])
        yfa.max('20190918_123456')

