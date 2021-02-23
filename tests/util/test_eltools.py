#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
import unittest


class TestJasonVerify(unittest.TestCase):

   def test_split_elkeys(self):
       testkey :str = "response:@@data.province"
       testkey2 :str = "response:$$data.province"
       testkey3: str = "response:#data.province"
       regjson = ":@@"
       userdefine = ":$$"
       strsp = ":#"
       spsjon = testkey.split(regjson,maxsplit=2)
       print(spsjon)
       spuserdefine = testkey2.split(userdefine,maxsplit=2)
       print(spuserdefine)
       sps = testkey3.split(strsp, maxsplit=2)
       print(sps)



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())