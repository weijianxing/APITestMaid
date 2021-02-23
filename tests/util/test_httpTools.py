#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
import unittest
from util import HttpTools
class TestHttpTools(unittest.TestCase):

    def test_getRequestUrl(self):
        url = "https://s.wuage.com/suggest/searchword"
        params = {"word": "ztong", "type": 1}
        geturl = HttpTools.getUrlWithParamters(url, params)
        assert geturl == "https://s.wuage.com/suggest/searchword?word=ztong&type=1"

    #@unittest.skip("test")
    def test_request(self):
        url = "https://s.wuage.com/suggest/searchword"
        #?word=ztong&type=1
        params = {"word":"ztong", "type":1}
        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "method": "GET"

        }
        data = HttpTools.request(url,postData=params,headers=header)
        print(data)

    def test_jsonp2json(self):
        jsonpdata = 'jsonpCallback(["紫铜带","紫铜线","紫铜排","紫铜棒","紫铜板","紫铜管","紫铜","天津众通联金属材料有限公司","永年县中通电力金具制造有限公司","山西中通高技术有限责任公司"])'
        expect = '["紫铜带","紫铜线","紫铜排","紫铜棒","紫铜板","紫铜管","紫铜","天津众通联金属材料有限公司","永年县中通电力金具制造有限公司","山西中通高技术有限责任公司"]'
        # prefixlen = "jsonpCallback(".__len__()
        # substr = jsonpdata.strip()[prefixlen: -1]
        # print(substr)
        acture = HttpTools.jsonp_2_json(jsonpdata)
        print(acture)
        assert expect == acture
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())