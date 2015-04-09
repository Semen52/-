# coding: utf8
import pandas

def load_data_from_csv(file_in='data\parsered1.csv', info=True):
    """
    Load data from csv file.
    :param file_in: input file.
    :param info: show statistical information.
    :return: DataFrame.
    """
    try:
        data = pandas.read_csv(file_in, header=0, sep=';')
        if info:
            print data.info()
            print data.describe()
        return data
    except Exception:
        print 'Error while loading file' + file_in


def save_data_to_csv(file_out='data\\anomaly.csv', data=''):
    out_file = open(file_out, "wb")
    out_file.write(str(data).encode('utf8'))
    out_file.close()
