import datetime
from dateutil.relativedelta import relativedelta

class BaseDate:
    '''
    基準となる日付クラス
    '''
    def __init__(self, year, month, day):
        '''
        year    : 年
        month   : 月
        day     : 日
        '''
        self._date = datetime.datetime(year, month, day)

    def after_year(self, n):
        '''
        n年間(=n年後の前日)の日付を求める
        基準年月日が2010年8月21日の時、2011年8月20日になる
        n: n年間
        '''
        the_date = self._date + relativedelta(years=n) - datetime.timedelta(1)

        return BaseDate(the_date.year, the_date.month, the_date.day)

    def before_year(self, n):
        '''
        過去n年間(=n年前の翌日)の日付を求める
        基準年月日が2010年8月21日の時、2009年8月22日になる
        n: n年間
        '''
        the_date = self._date - relativedelta(years=n) + datetime.timedelta(1)

        return BaseDate(the_date.year, the_date.month, the_date.day)

    def after_month(self, n):
        '''
        nヶ月間(=nヶ月後の前日)の日付を求める
        基準年月日が2010年8月21日の時、2010年9月20日になる
        n: nヶ月間
        '''
        the_date = self._date + relativedelta(months=n) - datetime.timedelta(1)

        return BaseDate(the_date.year, the_date.month, the_date.day)

    def before_month(self, n):
        '''
        過去nヶ月間(=nヶ月前の翌日)の日付を求める
        基準年月日が2010年8月21日の時、2009年8月22日になる
        n: 過去nヶ月間
        '''
        the_date = self._date - relativedelta(months=n) + datetime.timedelta(1)

        return BaseDate(the_date.year, the_date.month, the_date.day)

    def __str__(self):
        return '{year:04d}/{month:02d}/{day:02d}'.format(
                year=self._date.year, month=self._date.month, day=self._date.day)
