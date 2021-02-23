#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com
import os
import unittest

from util.loadConfig import load_file


class TestLoadconf(unittest.TestCase):
    def test_load(self):
        file = os.getcwd() + "/config/alter.yaml"
        print(file)
        conf = load_file(file)
        token = conf["dingToken"]
        at_mobiles = conf["atowners"]
        owner = conf["owner"]

        print("token is : " + token)
        print("at_mobiles is : " + str(at_mobiles))
        print("owner is : " + owner)
        assert owner, "魏建星"
        # print("token is : " + token)file



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())