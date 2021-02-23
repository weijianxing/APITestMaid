#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com

import unittest
import re
from json import JSONDecodeError

from ext.jsonVerifyUtils import json_loads_byteified, getNodeValue, JsonVerifyUtils


class TestJasonVerify(unittest.TestCase):

    @unittest.skip("reason for skipping")
    def test_json_tools(self):
        path = "a.b.c".split(".")
        reg = ".*\[\d\]$"
        regindex = "\d"
        print(re.findall(regindex, "[2]")[:1])
        print(re.search(reg, "s[2]"))
        if re.match(reg, "s[2]") is None:
            assert False, "match fail."



    def test_getNodeValue(self):
        
        test_jsonstr="""
        {
               "article": [
        
                  {
                     "id":"01",
                     "language": "JSON",
                     "edition": "first",
                     "author": "Derrick Mwiti"
                  },

                  {
                     "id":"02",
                     "language": "Python",
                     "edition": "second",
                     "author": "Derrick Mwiti"
                  }
               ],

               "blog":[
               {
                   "name": "Datacamp",
                   "URL":"datacamp.com"
               }
               ]
            }
            
            """

        jdict = json_loads_byteified(test_jsonstr)
        path = "blog[0].name"
        path2 = "article"

        value = getNodeValue(jdict, path2)
        for v in value:
            print(v.get("id"))

        print("return value is : ", value)
        # assert value == "Datacamp"

    @unittest.skip("reason for skipping")
    def test_JsonUtils_nodeContain_fail(self):

            test_jsonstr = """
            {
            "caseName": "testcase1",
            "blog":[
            {"name": "test", "url": "www.wuage.com"},
            {"name": "test2", "url": "www.help.wuage.com"}
            ]
            }
            """
            with self.assertRaises(AssertionError) as context:
                verify = JsonVerifyUtils(test_jsonstr)
                verify.verifyNodeContain("blog[0].name","tesxxx")
                self.assertTrue('This is broken' in context.msg)


    @unittest.skip("reason for skipping")
    def test_JsonUtils_nodeContain(self):

        test_jsonstr = """
        {
        "caseName": "testcase1",
        "blog":[
        {"name": "test", "url": "www.wuage.com"},
        {"name": "test2", "url": "www.help.wuage.com"}
        ]
        }
        """
        verify = JsonVerifyUtils(test_jsonstr)
        verify.verifyNodeContain("blog[0].name","tes")

    @unittest.skip("reason for skipping")
    def test_JsonUtils_nodeEq(self):

            test_jsonstr = """
            {
            "caseName": "testcase1",
            "blog":[
            {"name": "test", "url": "www.wuage.com"
            ,"address" : {"home": "chaoyang" , "company": "haidian" }
            },
            {"name": "test2", "url": "www.help.wuage.com"
            ,"address" : {"home": "chaoyangw" , "company": "haidianxxx" }}
            ]
            }
            """
            verify = JsonVerifyUtils(test_jsonstr)
            verify.verifyNodeEq("blog[0].name","test")
            verify.verifyNodeEq("caseName","testcase1")
            verify.verifyNodeEq("blog[1].address.home","chaoyangw")

    @unittest.skip("reason for skipping")
    def test_JsonUtils_nodeEq_fail(self):

                test_jsonstr = """
                {
                "caseName": "testcase1",
                "blog":[
                {"name": "test", "url": "www.wuage.com"},
                {"name": "test2", "url": "www.help.wuage.com"}
                ]
                }
                """
                with self.assertRaises(AssertionError) as context:
                    verify = JsonVerifyUtils(test_jsonstr)
                    verify.verifyNodeEq("blog[0].name","testxxx")
                    info = context.msg
                    print(info)
                    self.assertTrue('This is broken' in context.msg)
    @unittest.skip("reason for skipping")
    def test_JsonUtils_nodeEq_fail2(self):

                    test_jsonstr = """
                    {
                    "caseName": "testcase1",
                    "blog":[
                    {"name": "test", "url": "www.wuage.com"},
                    {"name": "test2", "url": "www.help.wuage.com"}
                    ]
                    }
                    """
                    with self.assertRaises(AssertionError) as context:
                        verify = JsonVerifyUtils(test_jsonstr)
                        verify.verifyNodeEq("blog[0].wname","testxxx")
                        info = context.msg
                        print(info)
                        self.assertTrue('This is broken' in context.msg)
    @unittest.skip("reason for skipping")
    def test_JsonUtils_nodeEq_fail3(self):

                    test_jsonstr = """
                    {
                    "caseName": "testcase1",
                    "blog":[
                    {"name": "test", "url": "www.wuage.com"},
                    {"name": "test2", "url": "www.help.wuage.com"}
                    ]
                    }
                    """
                    with self.assertRaises(AssertionError) as context:
                        verify = JsonVerifyUtils(test_jsonstr)
                        verify.verifyNodeEq("blog","testxxx")
                        info = context.msg
                        print(info)
                        self.assertTrue('This is broken' in context.msg)
    @unittest.skip("reason for skipping")
    def test_JsonVerify_init_fail(self):

                        test_jsonstr = """
                        {
                        "caseName": "testcase1",
                        "blog":[
                        {"name": "test", "url": "www.wuage.com"},
                        {"name": "test2", "url": "www.help.wuage.com"}
                        ]
                        
                        """
                        with self.assertRaises(JSONDecodeError) as context:
                            verify = JsonVerifyUtils(test_jsonstr)
                            self.assertTrue('This is broken' in context.msg)



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(unittest.main())
