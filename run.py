import os
import datetime
import sys
from yfk import main as yfkmain
from yfk.config import OUTPUT_DIR, YFK_CSV_MON, YFK_CSV_DAY, YFK_MEIGARA, ERROR_CODES

if __name__ == '__main__':
    # CSVファイル出力ディレクトリの作成
    now = datetime.datetime.today()                                                  
    dirname = '{:04}{:02}{:02}_{:02}{:02}{:02}'.format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
    output_dir = os.path.join(OUTPUT_DIR, YFK_CSV_MON, dirname)
    os.makedirs(output_dir)

    start_time = datetime.datetime.now()
    yfkmain(YFK_MEIGARA, output_dir, max=True, start=None, end=None)

    end_time = datetime.datetime.now()
    print('It took {} seconds.'.format((end_time - start_time).seconds))

