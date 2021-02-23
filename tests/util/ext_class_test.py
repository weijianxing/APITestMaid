#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
import json
class ExtClass():
    def test(self):
        print("testing function in class.")
    def test_fun(self,name = "wuage",group = "testing"):
        print("test fun")
        print("name is : ", name)
        print("group is : ", group)
        return name
    def verifySearchOrder(self,data,startwith):
        # print("Get init data",data)
        # pass
        resp = json.loads(data)
        assert type(resp) is list, " data not type of list. : " + str(type(resp))
        print("verify start with: " + startwith)
        for item in resp:
            print("Get  item data : ", item)
            assert len(item["showWord"])>0 , " showWord can be empty. " + str(item)
            #assert fail testing.
            # assert len(item["showWord"]) > 5000, " showWord can be empty. " + str(item)