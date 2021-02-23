#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com
from util import  loadConfig
from util.loadConfig import load_file, load_folder_files
import os
import unittest

class TestLoading(unittest.TestCase):
    def test_load(self):
        dirname = os.getcwd() + "/metacase"
        print(dirname)
        filelist = load_folder_files(dirname)
        print(filelist)
        for casefile in filelist:
            context = load_file(casefile)
            print(context)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())