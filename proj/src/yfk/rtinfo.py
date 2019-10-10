# Yahoo Financeからリアルタイムデータを取得する

import yfinance as yf

def main(code):
    ticker = yf.Ticker(code)
    for k, v in ticker.info.items():
        print("{:<40}:{}".format(k, v))


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('銘柄コードを入力して下さい')
        print('python {} コード'.format(__file__))
        sys.exit()

    main(sys.argv[1])
