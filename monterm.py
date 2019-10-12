######################
# 月足データ期間指定 #
######################
import sys, os, re, glob, datetime
import argparse
import pandas as pd
from argparse import RawTextHelpFormatter
from yfk import BaseDate
from yfk import SelectCsv
from yfk import YFK_CSV_MON, YFK_CSV_MONTERM, OUTPUT_DIR

RE_DATE = re.compile(r'^(\d{4})(?:/|-)?(\d{2})$')


def main(start=None, end=None):
    '''
    start:  開始年月日(BaseDate) Noneのときmaxの開始日付(=最古日付)
    end:    終了年月日(BaseDate) Noneのときmaxの終了日付(=最新日付)
    '''

    select_dir = max(glob.glob(os.path.join(OUTPUT_DIR, YFK_CSV_MON, '*')))
    output_dir = os.path.join(OUTPUT_DIR, YFK_CSV_MONTERM)
    os.makedirs(output_dir, exist_ok=True)

    for csv in glob.glob(os.path.join(select_dir, '*.csv')):
        monthly_term = SelectCsv(os.path.join(output_dir, csv)).get(start, end)
        # print(monthly_term)
        output_csv = 'term_' + os.path.basename(csv)
        monthly_term.to_csv(os.path.join(output_dir, output_csv))


def get_base_date(date):
    '''
    date:   (YYYY, MM)
            YYYY:年
            MM:  月
    '''

    year = int(date[0])
    month = int(date[1])
    day = int(1)
    return BaseDate(year, month, day)


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
            description='''月足データ期間抽出プログラム

[使用例]
2018年7月3日-2019年10月7日までを取得するとき
python monterm.py 2018/07/03 --to 2019/10/07

2017年5月5日から3ヶ月間を取得するとき
python monterm.py 2017/05/05 --am 3

2005年8月10日から過去7年間を取得するとき
python monterm.py 2005/08/10 --by 7

[備考]
日付フォーマットは、YYYYMMDD YYYY/MM/DD YYYY-MM-DDが使用できる

基準日とオプション指定は逆でも良い
以下は、どれでも良い
yfk/monterm.sh 2017/05/05 --am 3
yfk/monterm.sh 2017/05/05 --am=3
yfk/monterm.sh --am 3 2017/05/05
yfk/monterm.sh --am=3 2017/05/05

--am/--bm/--ay/--am/--old/--toはいずれか一つしか指定できない

base_date(基準日)の指定は必須
base_dateだけを指定した場合は、最古日付から基準日までのデータを抽出する
''')
    parser.add_argument('base_date', help='基準年月日')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--to', help='基準日から指定日付(TO)まで')
    group.add_argument('--old', action='store_true', help='最古年月から基準日まで')
    group.add_argument('--am', type=int, help='基準日を含めてAMヶ月間')
    group.add_argument('--bm', type=int, help='基準日を含めて過去BMヶ月間')
    group.add_argument('--ay', type=int, help='基準日を含めてAY年間')
    group.add_argument('--by', type=int, help='基準日を含めて過去BY年間')

    args = parser.parse_args()

    # sys.exit()
    m = RE_DATE.search(args.base_date)
    if not m:
        print('基準日の日付指定が間違っています')
        print('YYYYMDD YYYY/MM/DD YYYY-MM-DD')
        sys.exit()


    base_date = get_base_date(m.groups()) # BaseDate型を得る

    if args.to: # 基準日から指定年月日まで
        m = RE_DATE.search(args.to)
        if not m:
            print('終了日の日付指定が間違っています')
            print('YYYYMDD YYYY/MM/DD YYYY-MM-DD')
            sys.exit()

        start = base_date
        end = get_base_date(m.groups())
        if start > end:
            print('終了日が基準日より過去の日付になっています')
            sys.exit()
    elif args.old: # 最古年月から基準日まで
        start = None
        end = base_date
    elif args.am: # nヶ月間
        start = base_date
        end = base_date.after_month(args.am)
    elif args.bm: # 過去nヶ月間
        start = base_date.before_month(args.bm)
        end = base_date
    elif args.ay: # n年間
        start = base_date
        end = base_date.after_year(args.ay)
    elif args.by: # 過去n年間
        start = base_date.before_year(args.by)
        end = base_date
    else:   # オプション引数がないとき(基準日から最新年月まで)
        start = base_date
        end = None

    # DEBUG
    if False:
        print('start:' + str(start))
        print('end: ' + str(end))

    main(start, end)

    end_time = datetime.datetime.now()
    print('It took {} seconds.'.format((end_time - start_time).seconds))
