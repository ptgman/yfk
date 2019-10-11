import os

# Windows side directories
# yfk_csv         株価CSVファイル出力フォルダ
# yfk_meigara     銘柄コードファイル(us-meigara.csv)を置くフォルダ
# yfk_bat         バッチファイルを置くフォルダ

YFK_CSV = 'yfk_csv'
YFK_CSV_MON = 'monthly'
YFK_CSV_DAY = 'daily'
YFK_CSV_MONTERM = 'monterm'

# OUTPUT_DIR = os.path.join(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))), CSVROOT)
YAHOO_FINANCE = os.path.join(os.environ['HOME'], 'hostpg')
OUTPUT_DIR = os.path.join(YAHOO_FINANCE, YFK_CSV)

# CSVFILE = 'us-meigara.csv'
YFK_MEIGARA = os.path.join(YAHOO_FINANCE, 'yfk_meigara', 'us-meigara.csv')
YFK_BAT = 'yfk_bat'
ERROR_CODES = 'error.csv'

API_SLEEP = 1   # APIアクセスのウエイト(秒)
