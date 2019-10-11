import pytest
from yfk import BaseDate

@pytest.fixture(scope='session')
def normal_date():
    return BaseDate(2010, 8, 21)

@pytest.fixture()
def leap_year_feb28():    # 閏年の2月29日
    return BaseDate(2012, 2, 28) 

@pytest.fixture()
def leap_year_feb29():    # 閏年の2月29日
    return BaseDate(2012, 2, 29) 

def test_after_year(normal_date):
    '''
    n年間のテスト
    '''
    assert str(normal_date.after_year(1)) == str(BaseDate(2011, 8, 20))
    assert str(normal_date.after_year(2)) == str(BaseDate(2012, 8, 20))
    assert str(normal_date.after_year(3)) == str(BaseDate(2013, 8, 20))

def test_before_year(normal_date):
    '''
    過去n年間のテスト
    '''
    assert str(normal_date.before_year(1)) == str(BaseDate(2009, 8, 22))
    assert str(normal_date.before_year(2)) == str(BaseDate(2008, 8, 22))
    assert str(normal_date.before_year(3)) == str(BaseDate(2007, 8, 22))

def test_after_month(normal_date):
    '''
    nヶ月間のテスト
    '''
    assert str(normal_date.after_month(1)) == str(BaseDate(2010, 9, 20))
    assert str(normal_date.after_month(2)) == str(BaseDate(2010, 10, 20))
    assert str(normal_date.after_month(3)) == str(BaseDate(2010, 11, 20))
    assert str(normal_date.after_month(5)) == str(BaseDate(2011, 1, 20))

def test_before_month(normal_date):
    '''
    過去nヶ月間のテスト
    '''
    assert str(normal_date.before_month(1)) == str(BaseDate(2010, 7, 22))
    assert str(normal_date.before_month(2)) == str(BaseDate(2010, 6, 22))
    assert str(normal_date.before_month(3)) == str(BaseDate(2010, 5, 22))

################
# 閏年のテスト #
################
def test_leap_after_year(leap_year_feb28, leap_year_feb29):
    assert str(leap_year_feb28.after_year(1)) == str(BaseDate(2013, 2, 27))
    assert str(leap_year_feb29.after_year(1)) == str(BaseDate(2013, 2, 27))

def test_leap_before_year(leap_year_feb28, leap_year_feb29):
    assert str(leap_year_feb28.before_year(1)) == str(BaseDate(2011, 3, 1))
    assert str(leap_year_feb29.before_year(1)) == str(BaseDate(2011, 3, 1))

def test_leap_after_month(leap_year_feb28, leap_year_feb29):
    assert str(leap_year_feb28.after_month(1)) == str(BaseDate(2012, 3, 27))
    assert str(leap_year_feb29.after_month(1)) == str(BaseDate(2012, 3, 28))

def test_leap_before_month(leap_year_feb28, leap_year_feb29):
    assert str(leap_year_feb28.before_month(1)) == str(BaseDate(2012, 1, 29))
    assert str(leap_year_feb29.before_month(1)) == str(BaseDate(2012, 1, 30))

####################
# 日付の大小テスト #
####################
def test_equal():
    d1 = BaseDate(2019, 10, 10)
    d2 = BaseDate(2019, 10, 10)
    assert d1 == d2

def test_less_or_equal():
    d1 = BaseDate(2019, 10, 10)
    d2 = BaseDate(2019, 10, 10)
    d3 = BaseDate(2019, 3, 10)
    assert d2 <= d1
    assert d3 <= d1

def test_less_than():
    d1 = BaseDate(2019, 10, 10)
    d3 = BaseDate(2019, 3, 10)
    assert d3 < d1

def test_greater_or_equal():
    d1 = BaseDate(2019, 10, 10)
    d2 = BaseDate(2019, 10, 10)
    d3 = BaseDate(2020, 10, 10)
    assert d2 >= d1
    assert d3 >= d1

def test_greater_than():
    d1 = BaseDate(2019, 10, 10)
    d3 = BaseDate(2020, 3, 10)
    assert d3 > d1

