#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author : Zhou Jian
@email  : summychou@163.com
'''

import glob
import os
import zipfile

try:
    from tqdm import tqdm
except ImportError, e:
    print '>> tqdm Module is not found, please install it first'

def run():

    textfiles = glob.glob('anjuke_new_house/*txt')
    if len(textfiles) != 0:
        print ">> compress files under anjuke_new_house"
        f = zipfile.ZipFile('anjuke_new_house/anjuke_new_house.zip', 'w', zipfile.ZIP_DEFLATED)
        for textfile in tqdm(textfiles):
            f.write(textfile)
            os.remove(textfile)
        f.close()

    textfiles = glob.glob('anjuke_second_house/*txt')
    if len(textfiles) != 0:
        print ">> compress files under anjuke_second_house"
        f = zipfile.ZipFile('anjuke_second_house/anjuke_second_house.zip', 'w', zipfile.ZIP_DEFLATED)
        for textfile in tqdm(textfiles):
            f.write(textfile)
            os.remove(textfile)
        f.close()

    textfiles = glob.glob('anjuke_renting_house/*txt')
    if len(textfiles) != 0:
        print ">> compress files under anjuke_renting_house"
        f = zipfile.ZipFile('anjuke_renting_house/anjuke_renting_house.zip', 'w', zipfile.ZIP_DEFLATED)
        for textfile in tqdm(textfiles):
            f.write(textfile)
            os.remove(textfile)
        f.close()

if __name__ == '__main__':
    run()
