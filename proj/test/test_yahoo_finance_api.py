import pytest
import os
import pandas as pd
from yfk import YahooFinanceApi as YFA
from make_test_data import get_data

OUTPUT_CSV = 'output_csv'
CODE = 'KO'
DELTA = 10e-6

@pytest.fixture()
def ko_monthly_csv(scope='session'):
    """Yahoo Financeサイトでダウンロードした三種類のCSVファイルを合成したもの"""
    return get_data()

@pytest.fixture(scope='session')
def ko_from_api():
    """YFinance APIから取得したデータ"""
    ko = YFA(CODE)
    ko.max(OUTPUT_CSV)
    df = pd.read_csv(os.path.join(OUTPUT_CSV, CODE + '.csv'), index_col=0)

    return df


def test_open(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Open'] - 0.263021 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Open'] -\
        ko_from_api.loc['1962/01/01'].loc['Open'] < DELTA


def test_high(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['High'] - 0.270182 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['High'] -\
        ko_from_api.loc['1962/01/01'].loc['High'] < DELTA


def test_low(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Low'] - 0.233073 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Low'] -\
        ko_from_api.loc['1962/01/01'].loc['Low'] < DELTA


def test_close(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Close'] - 0.242839 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Close'] -\
        ko_from_api.loc['1962/01/01'].loc['Close'] < DELTA


def test_adj_close(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Adj Close'] - 0.050381 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Adj Close'] -\
        ko_from_api.loc['1962/01/01'].loc['Adj Close'] < DELTA


def test_volume(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Volume'] == 29414400
    assert ko_monthly_csv.loc['1962-01-01'].loc['Volume'] ==\
        ko_from_api.loc['1962/01/01'].loc['Volume']


def test_dividends(ko_monthly_csv, ko_from_api):
    assert ko_from_api.loc['1962/03/01'].loc['Date_Div'] == '1962/03/13'
    assert ko_from_api.loc['1962/03/01'].loc['Dividends'] - 0.00156 < DELTA

    assert ko_from_api.loc['1962/03/01'].loc['Date_Div'] == \
            ko_monthly_csv.loc['1962-03-01'].loc['Date_Div'].replace('-', '/')

    assert ko_from_api.loc['1962/03/01'].loc['Dividends'] == \
            float(ko_monthly_csv.loc['1962-03-01'].loc['Dividends'])


def test_splits(ko_monthly_csv, ko_from_api):
    assert ko_from_api.loc['1965/02/01'].loc['Date_Spli'] == '1965/02/19'
    assert ko_from_api.loc['1965/02/01'].loc['Stock_Splits'] - 2 < DELTA

    assert ko_from_api.loc['1965/02/01'].loc['Date_Spli'] == \
            ko_monthly_csv.loc['1965-02-01'].loc['Date_Spli'].replace('-', '/')

    assert ko_from_api.loc['1965/02/01'].loc['Stock_Splits'] - \
            1 / eval(ko_monthly_csv.loc['1965-02-01'].loc['Stock_Splits']) \
            < DELTA
