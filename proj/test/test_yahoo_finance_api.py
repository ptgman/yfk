import pytest
import os
import pandas as pd
from yfk import YahooFinanceApi as YFA
from make_test_data import get_data

OUTPUT_CSV = 'output_csv'
CODE = 'KO'

@pytest.fixture()
def ko_monthly_csv():
    """Yahoo Financeサイトでダウンロードした三種類のCSVファイルを合成したもの"""
    return get_data()

@pytest.fixture()
def ko_from_api():
    """YFinance APIから取得したデータ"""
    ko = YFA(CODE)
    ko.max(OUTPUT_CSV)
    df = pd.read_csv(os.path.join(OUTPUT_CSV, CODE + '.csv'), index_col=0)

    return df


def test_open(ko_monthly_csv, ko_from_api):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Open'] == 0.263021
    assert ko_monthly_csv.loc['1962-01-01'].loc['Open'] -\
        ko_from_api.loc['1962/01/01'].loc['Open'] < 0.01


def test_dividends(ko_monthly_csv, ko_from_api):
    ko_from_api.loc['1962/03/01'].loc['Date_Div'] == '1962/03/13'
    ko_from_api.loc['1962/03/01'].loc['Dividends'] == 0.00156

    ko_from_api.loc['1962/03/01'].loc['Date_Div'] == \
            ko_monthly_csv.loc['1962-03-01'].loc['Date_Div']

    ko_from_api.loc['1962/03/01'].loc['Dividends'] == \
            ko_monthly_csv.loc['1962-03-01'].loc['Dividends']


def test_splits(ko_monthly_csv, ko_from_api):
    assert ko_from_api.loc['1965/02/01'].loc['Date_Spli'] == '1965/02/19'
    assert ko_from_api.loc['1965/02/01'].loc['Stock_Splits'] == 2

    assert ko_from_api.loc['1965/02/01'].loc['Date_Spli'] == \
            ko_monthly_csv.loc['1965-02-01'].loc['Date_Spli'].replace('-', '/')

    assert ko_from_api.loc['1965/02/01'].loc['Stock_Splits'] == \
            1 / eval(ko_monthly_csv.loc['1965-02-01'].loc['Stock_Splits'])
