import pandas as pd
import copy
import re

MONTHLY = 'testdata/KO_monthly_max.csv'
DIVIDENDS = 'testdata/KO_dividends_max.csv'
SPLITS = 'testdata/KO_splits_max.csv'
RE_DAY = re.compile(r'\d\d$')

def merged(monthly, dividends, splits):
    # Dividencs/StockSplits列の追加
    # mon_div_spli = copy.copy(monthly)
    monthly['Date_Div'] = ''
    monthly['Dividends'] = ''
    monthly['Date_Spli'] = ''
    monthly['Stock_Splits'] = ''

    # Dividendsのコピー
    for i in dividends.index:
        mon_first = RE_DAY.sub('01', i)
        monthly.loc[mon_first, 'Date_Div'] = i
        monthly.loc[mon_first, 'Dividends'] = str(dividends.loc[i]['Dividends'])

    # Stock Splitsのコピー　
    for i in splits.index:
        mon_first = RE_DAY.sub('01', i)
        monthly.loc[mon_first, 'Date_Spli'] = i
        monthly.loc[mon_first, 'Stock_Splits'] = splits.loc[i]['Stock Splits']


    return monthly

def get_data():
# 月次データ/Dividendsデータ/StockSplitsデータを作成する
    monthly = pd.read_csv(MONTHLY, index_col=0)
    dividends = pd.read_csv(DIVIDENDS, index_col=0)
    splits = pd.read_csv(SPLITS, index_col=0)

    return merged(monthly, dividends, splits)
