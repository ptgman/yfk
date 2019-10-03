#############
# ver 0.0.2 #
#############
import sys, os
import csv
from yfk import YahooFinanceApi
from yfk.config import OUTPUT_DIR, YFK_CSV, ERROR_CODES


def main(csvfile, output_dir, max=True, start=None, end=None):
    '''
    csvfile:    銘柄コードのCSVファイル
    output_dir: 取得データ出力ディレクトリ
    '''
    is_first_error = True

    with open(csvfile, 'rt') as f:
        cin = csv.reader(f)
        next(cin)

        for row in cin:
            yfa = YahooFinanceApi(row[0])
            try:
                yfa.max(output_dir)
            except:
                print('銘柄:{}のデータが作成出来ませんでした。'.format(row[0]))
                with open(os.path.join(output_dir, ERROR_CODES), 'at') as f:
                    if is_first_error:
                        f.write('銘柄コード(Ticker Symbol),銘柄名(Company Name),市場(Market)\n')
                        is_first_error = False

                    f.write(','.join(row) + '\n')


if __name__ == '__main__':

    # CSVファイル出力ディレクトリの作成
    now = datetime.datetime.today()
    dirname = '{:04}{:02}{:02}_{:02}{:02}{:02}'.format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
    output_dir = os.path.join(OUTPUT_DIR, dirname)
    os.makedirs(output_dir)

    start_time = datetime.datetime.now()
    main(YFK_CSV, output_dir, max=True, start=None, end=None)
    end_time = datetime.datetime.now()

    print('It took {} seconds.'.format((end_time - start_time).seconds))
