import os


def mk_filename_pair(basepath, header_type='csv'):
    p, e = os.path.splitext(basepath)
    return p + '_header.' + header_type, p + '_data.csv'
