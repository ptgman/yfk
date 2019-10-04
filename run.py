import os
import datetime
import sys
from yfk import main as yfkmain
from yfk.config import OUTPUT_DIR, YFK_CSV_MON, YFK_CSV_DAY, YFK_MEIGARA, ERROR_CODES

if __name__ == '__main__':
    day_or_mon = sys.argv[1]
    day_mon_dir = {'d':YFK_CSV_DAY, 'm':YFK_CSV_MON}[day_or_mon]   # d)日足 m)月足

    # CSVファイル出力ディレクトリの作成
    now = datetime.datetime.today()
    dirname = '{:04}{:02}{:02}_{:02}{:02}{:02}'.format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
    # output_dir = os.path.join(OUTPUT_DIR, dirname)
    output_dir = os.path.join(OUTPUT_DIR, day_mon_dir, dirname)
    os.makedirs(output_dir)

    start_time = datetime.datetime.now()

    # 日足／月足別に入力引数を取得してCSVファイルを作成する
    if day_or_mon == 'd':
        yfkmain(YFK_MEIGARA, output_dir, sys.argv[2])
    else:   # == 'm'
        max = bool(sys.argv[2])
        start = sys.argv[3]
        end = sys.argv[4]
        # yfkmain(YFK_MEIGARA, output_dir, max=True, start=None, end=None)
        yfkmain(YFK_MEIGARA, output_dir, max=True, start=None, end=None)

    end_time = datetime.datetime.now()

    print('It took {} seconds.'.format((end_time - start_time).seconds))
