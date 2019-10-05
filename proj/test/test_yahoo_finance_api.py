import pytest
import os
import pandas as pd
from yfk import YahooFinanceApi as YFA
from make_test_data import get_data

OUTPUT_CSV = '__output_csv'
CODE = 'KO'
DELTA = 10e-6

BAD_START = '2017-01-01'
BAD_END = '2017-12-31'
BAD_END_FIRST = '2017-12-01'

START = '2018-01-01'
END = '2018-12-31'
END_FIRST = '2018-12-01'    # ENDの月始め
START_SLA = START.replace('-', '/')
END_SLA = END.replace('-', '/')
START8 = START.replace('-', '')
END8 = END.replace('-', '')


@pytest.fixture()
def ko_monthly_csv(scope='session'):
    """Yahoo Financeサイトでダウンロードした三種類のCSVファイルを合成したもの"""
    return get_data()

@pytest.fixture(scope='session')
def ko_from_api_monthly(tmpdir_factory):
    """YFinance APIから取得したデータ"""
    output_dir = tmpdir_factory.mktemp('output_csv')
    ko = YFA(CODE)
    ko.monthly(output_dir)
    df = pd.read_csv(os.path.join(output_dir, CODE + '.csv'), index_col=0, dtype=str).fillna('')

    return df

@pytest.fixture(scope='session')
def ko_from_api_monthly_ymd(tmpdir_factory):
    """YFinance APIから取得したデータ(開始／終了日付指定)"""
    output_dir = tmpdir_factory.mktemp('output_csv')
    ko = YFA('KO', start=START8, end=END8)
    ko.monthly(output_dir)
    df = pd.read_csv(os.path.join(output_dir, CODE + '.csv'), index_col=0, dtype=str).fillna('')

    return df

################################
# データフレームの同値チェック #
################################
def is_same_value(df1, df2):
    '''
    df1:    Yahoo Financeサイトから取得(YYYY-MM-DD)
    df2:    APIで取得(YYYY/MM/DD)
    '''
    for i in df1.index:
        ii = i.replace('-', '/')
        row1 = df1.loc[i]
        row2 = df2.loc[ii]
        if abs(float(row1['Open']) - float(row2['Open'])) > DELTA:
            return False
        if abs(float(row1['High']) - float(row2['High'])) > DELTA:
            return False
        if abs(float(row1['Low']) - float(row2['Low'])) > DELTA:
            return False
        if abs(float(row1['Close']) - float(row2['Close'])) > DELTA:
            return False
        if abs(float(row1['Adj Close']) - float(row2['Adj Close'])) > DELTA:
            return False
        if abs(float(row1['Volume']) - float(row2['Volume'])) > DELTA:
            return False
        if row1['Date_Div'] != row2['Date_Div'].replace('/', '-'):
            return False
        dv1 = row1['Dividends']
        dv2 = row2['Dividends']
        if dv1 == '' and dv2 == '':
            continue

        if abs(float(dv1) - float(dv2)) > DELTA:
            return False

        if row1['Date_Spli'] != row2['Date_Spli'].replace('/', '-'):
            return False

        ss1 = row1['Stock_Splits']
        ss2 = row2['Stock_Splits']
        if ss1 == '' and ss2 == '':
            continue

        if abs(1 / eval(ss1) - float(ss2)) > DELTA:
            return False


    return True

#############################################
# monthlyメソッドのテスト(ノンパラメータ化) #
#############################################
def test_open(ko_monthly_csv, ko_from_api_monthly):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Open'] - 0.263021 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Open'] -\
        float(ko_from_api_monthly.loc['1962/01/01'].loc['Open']) < DELTA


def test_high(ko_monthly_csv, ko_from_api_monthly):
    assert ko_monthly_csv.loc['1962-01-01'].loc['High'] - 0.270182 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['High'] -\
        float(ko_from_api_monthly.loc['1962/01/01'].loc['High']) < DELTA


def test_low(ko_monthly_csv, ko_from_api_monthly):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Low'] - 0.233073 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Low'] -\
        float(ko_from_api_monthly.loc['1962/01/01'].loc['Low']) < DELTA


def test_close(ko_monthly_csv, ko_from_api_monthly):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Close'] - 0.242839 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Close'] -\
        float(ko_from_api_monthly.loc['1962/01/01'].loc['Close']) < DELTA


def test_adj_close(ko_monthly_csv, ko_from_api_monthly):
    assert ko_monthly_csv.loc['1962-01-01'].loc['Adj Close'] - 0.050381 < DELTA
    assert ko_monthly_csv.loc['1962-01-01'].loc['Adj Close'] -\
        float(ko_from_api_monthly.loc['1962/01/01'].loc['Adj Close']) < DELTA


def test_volume(ko_monthly_csv, ko_from_api_monthly):
    assert float(ko_monthly_csv.loc['1962-01-01'].loc['Volume']) == 29414400
    assert ko_monthly_csv.loc['1962-01-01'].loc['Volume'] ==\
        float(ko_from_api_monthly.loc['1962/01/01'].loc['Volume'])


def test_dividends(ko_monthly_csv, ko_from_api_monthly):
    assert ko_from_api_monthly.loc['1962/03/01'].loc['Date_Div'] == '1962/03/13'
    assert float(ko_from_api_monthly.loc['1962/03/01'].loc['Dividends']) - 0.00156 < DELTA

    assert ko_from_api_monthly.loc['1962/03/01'].loc['Date_Div'] == \
            ko_monthly_csv.loc['1962-03-01'].loc['Date_Div'].replace('-', '/')

    assert float(ko_from_api_monthly.loc['1962/03/01'].loc['Dividends']) == \
            float(ko_monthly_csv.loc['1962-03-01'].loc['Dividends'])


def test_splits(ko_monthly_csv, ko_from_api_monthly):
    assert ko_from_api_monthly.loc['1965/02/01'].loc['Date_Spli'] == '1965/02/19'
    assert float(ko_from_api_monthly.loc['1965/02/01'].loc['Stock_Splits']) - 2 < DELTA

    assert ko_from_api_monthly.loc['1965/02/01'].loc['Date_Spli'] == \
            ko_monthly_csv.loc['1965-02-01'].loc['Date_Spli'].replace('-', '/')

    assert float(ko_from_api_monthly.loc['1965/02/01'].loc['Stock_Splits']) - \
            1 / eval(ko_monthly_csv.loc['1965-02-01'].loc['Stock_Splits']) \
            < DELTA

################################
# yfinanceパラメータ化のテスト #
################################
def test_monthly(ko_monthly_csv, ko_from_api_monthly_ymd):
    '''start(YYYYMMDD) - end(YYYYMMDD)'''
    assert ko_monthly_csv.loc[START].loc['Open'] - \
            float(ko_from_api_monthly_ymd.loc[START_SLA].loc['Open']) < DELTA

    assert is_same_value(ko_monthly_csv.loc[START:END_FIRST], ko_from_api_monthly_ymd)

def test_daily():
    ''''特定日付で全件日足データを取得するテスト'''
    pass
