from make_test_data import get_data

def main(output_csv):
    df = get_data()
    df.to_csv(output_csv)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('出力CSVファイル名を指定して下さい。')
        print('python {} CSVファイル'.format(__file__))
        sys.exit()

    main(sys.argv[1])
