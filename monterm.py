######################
# 月足データ期間指定 #
######################
import sys, re
import argparse
from yfk import BaseDate

RE_DATE = re.compile(r'^(\d{4})(?:/|-)?(\d{2})(?:/|-)?(\d{2})')
def main(start=None, end=None):
    '''
    start:  開始年月日(YYYYMMDD) Noneのときmaxの開始日付(=最古日付)
    end:    終了年月日(YYYYMMDD) Noneのときmaxの終了日付(=最新日付)
    '''
    pass


def get_base_date(date):
    '''
    date:   YYYYMMDD
    '''
    date = str(date)
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])
    return BaseDate(year, month, day)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='月足データ期間抽出プログラム')
    group_month = parser.add_mutually_exclusive_group()
    group_year = parser.add_mutually_exclusive_group()
    group_from_to = parser.add_mutually_exclusive_group()

    parser.add_argument('base_date', type=int, help='基準年月日')

    parser.add_argument('--to', type=int, help='最古年月日から基準日まで')
    # group_from_to.add_argument('--old', action='store_true', help='最古年月日から基準日まで')
    group_month.add_argument('--am', type=int, help='基準日を含めてnヶ月間')
    group_month.add_argument('--bm', type=int, help='基準日を含めて過去nヶ月間')
    group_year.add_argument('--ay', type=int, help='基準日を含めてn年間')
    group_year.add_argument('--by', type=int, help='基準日を含めて過去n年間')

    args = parser.parse_args()
    base_date = get_base_date(args.base_date) # BaseDate型

    if args.to: # 基準日から指定年月日まで
        start = base_date
        end = get_base_date(args.to)
    elif args.am: # nヶ月間
        print(args.am)
        start = base_date
        end = base_date.after_month(args.am)
    elif args.bm: # 過去nヶ月間
        start = base_date.before_month(args.bm)
        end = base_date
    elif args.ay: # n年間
        start = base_date
        end = base_date.after_month(args.ay)
    elif args.by: # 過去n年間
        start = base_date.before_month(args.by)
        end = base_date
    else:   # オプション引数がないとき
        start = None
        end = base_date

    # DEBUG
    if True:
        print('start:' + str(start))
        print('end: ' + str(end))
