# -*- encoding: utf-8 -*-

import os
import csv
import json
import numpy as np
from scipy import io as sio
from json_tricks.np import dumps


def load_from_matlab(filename):
    """Returns a dictionary from a matlab binary file.
    :param filename str: Location for the `.mat` file
    :rtype: dict
    """
    matlab_obj = sio.loadmat(filename)
    information = {}
    rate = {}
    container = {}    
    for var in matlab_obj:
        if (len(matlab_obj[var]) and str(var) != "__version__" and str(var) != "__header__"):
            tmp = np.array(matlab_obj[var][0]).tolist()
            information[var] = ','.join(str(np.array(e).tolist()[0]) for e in tmp[0][0])
            current_rate = 0
            if len(tmp[0]):
                current_rate = np.array(tmp[0][1]).tolist()[0][0]
            rate[var] = current_rate
    container[0] = information
    container[1] = rate
    return container

def to_csv(dict_obj, filename):
    """Writes to a `.csv` file what's inside `dict_obj`.
    :param dict_obj dict: Object to serialize
    :param filename str: Destination for the serialized data
    """
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerows(dict_obj.items())

if __name__ == '__main__':
    path = 'data/'
    file_list = []
    list_dir = os.walk(path)
    for root, dirs, files in list_dir:
        for current in files:
            (file_name, extension) = os.path.splitext(current)
            if(extension == ".mat"):
                obj = load_from_matlab(path+current)
                to_csv(obj[0], path + file_name + '.csv')
                to_csv(obj[1], path + file_name + '_rate.csv')
