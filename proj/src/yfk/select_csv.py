import pandas as pd

class SelectCsv:
    def __init__(self, csv_file):
        self._csv_file = csv_file

    def get(self, start, end):
        '''
        start:  開始BaseData or None
        end:    終了BaseData or None
        '''
        original_df = pd.read_csv(self._csv_file, index_col=0)
        if start:
            start_df = original_df.loc[original_df.index >= str(start)]
        else:
            start_df = original_df.loc[:]

        if end:
            # print('type(end) = ', type(end))
            # print('str(end) = ', str(end))
            # print(type(start_df.index))
            end_df = start_df.loc[start_df.index <= str(end)]
        else:
            end_df = start_df

        return end_df


if __name__ == '__main__':
    import os
    from ymd_util import BaseDate

    selcsv = SelectCsv(os.path.join(os.environ['HOME'],
        'hostpg/yfk_csv/monthly/20191010_234652/A.csv'))
    start = BaseDate(2010, 10, 1)
    end = BaseDate(2011, 4, 1)
    data = selcsv.get(start, end)

    print(data)
