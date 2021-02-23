#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com

import unittest
import os
import sys
from unittest import skip

from util.loadExtPy import load_ext_python_files, CloneExtMoudle


class TestLoadExt(unittest.TestCase):
    def setUp(self):
        extdir = "/ext_python"
        extfilename = "/ext_python/ext_class_test.py"
        self.userhook = CloneExtMoudle(modulefile=extfilename, class_name="ExtClass")


    def tearDown(self):
        pass
    #@skip("")
    def test_load_function(self):
        #func = globals().get("test")()
        #func = getattr( TestLoadExt,"test_return")()
        #func  = globals().__getattribute__(ExtClass,"test")()
        #print(self.__dict__)
        #print(func)
        pass
    def test_userhook(self):
        self.userhook.exec_method("test")
    def test_userhook(self):
        self.userhook.exec_method("test_fun", "luolaosh")

    def test_userhook_return(self):
        func = self.userhook.exec_method("test_fun", "luolaosh", "wuage test")
        print("function return " + func)
        assert func == "luolaosh"
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())
