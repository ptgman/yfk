# 日足データ取得プログラム
import sys, os, datetime
import csv
from yfk import YahooFinanceApi as YFA
from yfk import YFK_MEIGARA, OUTPUT_DIR, YFK_CSV_DAY

def main(date, output_dir):
    '''
    date:   日足データの年月日
    output_dir: CSVファイル出力ディレクトリ
    '''
    date_slash = '{:04}/{:02}/{:02}'.format(
            int(date[:4]), int(date[4:6]), int(date[6:]))
    csv_file = os.path.join(output_dir, date + '.csv')
    error_log = os.path.join(output_dir, 'error_code.log')

    with open(csv_file, 'wt') as wf:
        wf.write('Ticker,Open,High,Low,Close,Adj.Close,Volume,Dividends Date,Dividends,Splits Date,Splits\n')

        with open(YFK_MEIGARA) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                code = row[0]
                yfa = YFA(code, period=None, start=date, end=date, interval='1d')
                try:
                    daily = yfa.a_day()
                    if daily.Dividends == 0.0:
                        div_date = ''
                        dividends = ''
                    else:
                        div_date = date_slash
                        dividends = '{:f}'.format(daily.Dividends)

                    if daily['Stock Splits'] == 0.0:
                        sp_date = ''
                        splits = ''
                    else:
                        sp_date = div_date
                        splits = '{:f}'.format(daily['Stock Splits'])

                    line = '{Ticker},{Open:f},{High:f},{Low:f},{Close:f},{Adj:f},{Volume:f},{Div_date},{Dividends},{Sp_date},{Splits}'.format(
                        Ticker=code,
                        Open=daily.Open, High=daily.High,
                        Low=daily.Low, Close=daily.Close,
                        Adj=daily['Adj Close'], Volume=daily.Volume,
                        Div_date=div_date, Dividends=dividends,
                        Sp_date=sp_date, Splits=splits)

                    wf.write(line)
                    wf.write('\n')
                except:
                    with open(error_log, 'at') as ef:
                        ef.write(code)
                        ef.write('\n')



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('引数の指定が間違っています')
        print('python {} 日付'.format(__file__))
        for i in sys.argv:
            print(i)

        sys.exit()

    date = sys.argv[1]

    # CSVファイル書き込みディレクトリを作る
    now_time = datetime.datetime.now()
    daily_dir = '{:04}{:02}{:02}_{:02}{:02}{:02}'.format(
            now_time.year, now_time.month, now_time.day,
            now_time.hour, now_time.minute, now_time.second)
    output_dir = os.path.join(OUTPUT_DIR, YFK_CSV_DAY, daily_dir)
    os.makedirs(output_dir)

    main(date, output_dir)
