#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
import os
import unittest

from core.MetaCases import MetaCases
from util.loadConfig import load_folder_files


class MetaCaseTestCase(unittest.TestCase):
    def setUp(self):
        print("load metacase.")
        dirname = os.getcwd() + "/metacase"
        self.filelist = load_folder_files(dirname)
        print(self.filelist)


    def tearDown(self):
        pass
    def test_metacaseDataLoaded(self):
        for casefile in self.filelist:
            print("xxx loading : " + casefile)
            self.metacase = MetaCases(casefile)
            print(self.metacase)
    def test_data(self):
        for casefile in self.filelist:
            print("loading : " + casefile)
            if str(casefile).endswith("searchSuggestion.yaml"):
                metacase = MetaCases(casefile)
                assert metacase.request.type == "https", "assert metacase.request.type"
                assert metacase.request.method == "get", "assert metacase.request.method"
                assert metacase.request.headers["cookie"] == "sessionid: testing",  'assert metacase.request.headers["cookie"]'
                assert metacase.request.url == 's.wuage.com/suggest/suggestwordext', "assert metacase.request.url"
                assert metacase.request.params["word"] == "$autoInject", ' assert metacase.request.params["word"]'
                assert metacase.request.params["type"] == 2, 'assert metacase.request.params["type"]'
                #assert metacase.request.baseVerification == ""
            elif str(casefile).endswith("mainsearch.yaml"):
                #metacase = MetaCases(casefile)
                pass
            else:
                assert False, "load file error."


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())