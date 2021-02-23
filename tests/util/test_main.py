#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com
import unittest

from core.main import Main


class TestMain(unittest.TestCase):

    def setUp(self):
        #
        pass
        self.main = Main("/tests/util/metacase/")
        # self.main = Main("metacase/")
        self.main.load_metaCases()

    def test_main(self):
       self.main.execute_metacases()
       # self.main.send_failMsg("")
       self.main.genarate_testReport()

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())