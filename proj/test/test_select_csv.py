import pytest
import pandas as pd
from yfk import SelectCsv
from yfk import BaseDate

TEST_CSV = 'testdata2/A.csv'

def is_equal(date, df1, df2):
    '''
    ある日の株価データが同値かチェックする
    date:   日付
    df1:    株価データ1
    df2:    株価データ2
    '''
    return (df1.fillna(0).loc[date]['Open':'Stock_Splits'] ==
            df2.fillna(0).loc[date]['Open':'Stock_Splits']).all() 

@pytest.fixture(scope='session')
def test_data():
    df = pd.read_csv(TEST_CSV, index_col=0)
    return df

def test_start_end(test_data):
    start = BaseDate(2010, 1, 1)
    end = BaseDate(2010, 4, 1)
    selcsv = SelectCsv(TEST_CSV)
    selected_data = selcsv.get(start, end)
    assert is_equal('2010/01/01', test_data, selected_data)

def test_start_end_range(test_data):
    '''一定範囲内のデータの同値性をテストする'''
    start = BaseDate(2001, 1, 1)
    end = BaseDate(2001, 12, 1)
    selcsv = SelectCsv(TEST_CSV)
    selected_data = selcsv.get(start, end)

    for mon in range(1, 13):
        date = '2001/{:02}/01'.format(mon)
        assert is_equal(date, test_data, selected_data)

def test_oldest_end(test_data):
    start = None
    end = BaseDate(2010, 4, 1)
    selcsv = SelectCsv(TEST_CSV)
    selected_data = selcsv.get(start, end)
    assert is_equal('2010/01/01', test_data, selected_data)

def test_newest_end(test_data):
    start = BaseDate(2000, 5, 1)
    end = None
    selcsv = SelectCsv(TEST_CSV)
    selected_data = selcsv.get(start, end)
    assert is_equal('2009/08/01', test_data, selected_data)

