#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : weijx.cpp@gmail.com
from abc import ABCMeta
import json
import re
from json import JSONDecodeError

from util import logger
from util.exceptions import ELError, FileFormatError


def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    if data == None :
        return None
    # if this is a unicode string, return its string representation
    #if isinstance(data, unicode):
    #   return data.encode('utf-8')
    # if this is a list of values, return list of byteified values

    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts and len(data) != 0:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    # if it's anything else, return it in its original form
    return data

def getArrayObjectNode(nodekey="", reg = ".*\[\d\]$"):
    """

    :param nodekey: the leaf node .eg "name",address[0]
    :param reg:
    :return:
    """
    match = False
    # if nodekey == ".":
    #     return True, 0, 0
    if re.match(reg, nodekey) is not None:
        #The leaf node type is a array object.
        match = True
        nodes = nodekey.split("[")
        index = re.findall("\d", nodes[1])[0]
        return match , nodes[0], int(index)
    else:
        return match,None,None
def getNodeValue(data,pathstr):
    """

    :param data: json  data
    :param path: The tree type of key node. eg. "a.b.c" ,  "f.g[1].h"
    :return: the node of path key value.

    """
    path = []
    if isinstance(pathstr, str):
        path = pathstr.split(".", maxsplit=20)
    else:
        path = pathstr
    if len(path) > 1:
        try:
            match, current_node, index = getArrayObjectNode(nodekey=path[0])
            if match:
            #If the path contain object array
                data =data.get(current_node)[index]
                path = path[1:]
                return getNodeValue(data, path)
            else:
                return getNodeValue(data.get(path[0]),path[1:])
        except AttributeError:
            return None
    if len(path) == 1:
        try:
            match, node, index = getArrayObjectNode(nodekey=path[0])
            if match:
                # If the path contain object array
                return data.get(node)[index]
            else:
                return data.get(path[0])
        except AttributeError:
            return None

def getNodesValues(data,pathstr,lastNode):
    """

    :param data: json  data
    :param path: The tree type of key node. eg. "a.b.c" ,  "f.g[1].h"
    :return: All the list node of path key values.

    """
    listObject = []
    listData = []

    if(type(pathstr) is list and len(pathstr) == 1 and pathstr[0]== ''):
        listObject = data
    elif(type(pathstr) is str and pathstr == ''):
        listObject = data
    else:
        listObject = getNodeValue(data,pathstr)
    for dataInfo in listObject:
        listData.append(dataInfo.get(lastNode))
    return listData


class JsonVerifyUtils(metaclass=ABCMeta):
    def __init__(self,jsondata):

        try:
            self.data = json_loads_byteified(jsondata)
        except JSONDecodeError as e:
            logger.log_error("JsonVerifyUtils init json data fail." + str(e))

    def verifyNodeContain(self,path: str,value):
        """
        verify user define data node contain expect value.
        :param path:
        :param value:
        :return:
        """
        actureValue = getNodeValue(self.data, path)
        assert str(actureValue).__contains__(value), "assert verifyNodeContain fail. " + str(self.data) + " did not contain  " \
                + value + " with path:  " + path
    def verifyNodeEq(self,path: str,value):
       """
       verify user define data node equal expect value.
       :param path:
       :param value:
       :return:
       """
       actureValue = getNodeValue(self.data, path)
       assert str(actureValue) == value, "assert jsonNodeEq fail. " + str(self.data) + " did not equal  " + value + " with path:  " + path

    def verifyStartwith(self,path: str, value):
        actureValue = getNodeValue(self.data, path)
        if type(actureValue) is list:
            for val in actureValue:
                if type(val) is not str:
                    raise ELError("verifyStartwith define path " + path + " not right. ")
                assert str(val).startswith(value[0]), "assert verifyStartwith fail. " + val + " did not equal  " + value[0]
        elif type(actureValue) is str:
            assert str(actureValue).startswith(value[0]), "assert verifyStartwith fail. " + actureValue + " did not equal  " + value[0]
        else:
            raise ELError("verifyStartwith define path " + path + " not right. ")
    def startwith(self,path: str, value):
        self.verifyStartwith(path=path,value=value)

    def verifyStartwiths(self,path: str, value):
        paths = path.split(".")
        print("verifyStartwiths : " + str(paths))
        actureValue = getNodesValues(self.data, paths[:-1],paths[-1])
        if type(actureValue) is list:
            for val in actureValue:
                if type(val) is not str:
                    raise ELError("verifyStartwith define path " + path + " not right. ")
                assert str(val).startswith(value[0]), "assert verifyStartwith fail. " + val + " did not equal  " + value[0]
        elif type(actureValue) is str:
            assert str(actureValue).startswith(value[0]), "assert verifyStartwith fail. " + actureValue + " did not equal  " + value[0]
        else:
            raise ELError("verifyStartwith define path " + path + " not right. ")
    def startwiths(self,path: str, value):
        print("startwiths path: "  + path)
        print("startwiths value: " + str(value))
        self.verifyStartwiths(path,value)

    def spliteEL(self, el: str, reg="="):
        """

        :param el: the json el at yaml node value, format: method param1 param2 ... paramN
        :param reg:
        :return:
        """
        methodInfos = el.split(reg)
        if methodInfos == None or len(methodInfos) == 0:
            raise FileFormatError("JsonVerifyUtils el value analyse fail.")

        elif len(methodInfos) == 1:
            name = "verifyNodeEq"
            value = methodInfos[0]
            methodInfos[0] = name
            methodInfos[1] = value
        else:
            pass
        if methodInfos[0] == "=" or methodInfos[0] == "==" or  methodInfos[0] == "eq":
            methodInfos[0] = "verifyNodeEq"
        return methodInfos
    def executeVerify(self,nodePath, el):
        """

        :param elMethod: the template json EL method
        :param args: method argements
        :return:
        """
        if(type(el) is not str):
            raise ELError(" execute verfiy input el type not string.")
        methodInfos = self.spliteEL(el)
        if hasattr(JsonVerifyUtils, methodInfos[0]):
            method = getattr(self, methodInfos[0])
            #The first paramter is path and the secand is expect value for json common verify method
            return method(nodePath,methodInfos[1:])
        else:
            raise ELError("user defined hook method : " + methodInfos[0] + " not found.")
if __name__ == '__main__':
    import json

    my_json_string = """{
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
    json2 = """
    [{"area":"","showWord":"<em>不锈</em>钢六角棒","suggestWord":"不锈钢六角棒","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢板","suggestWord":"不锈钢板","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢冷轧无缝管","suggestWord":"不锈钢冷轧无缝管","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢异型管","suggestWord":"不锈钢异型管","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢热轧无缝管","suggestWord":"不锈钢热轧无缝管","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢螺丝线","suggestWord":"不锈钢螺丝线","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢工业流体管","suggestWord":"不锈钢工业流体管","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢锻打件","suggestWord":"不锈钢锻打件","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢玫瑰金板","suggestWord":"不锈钢玫瑰金板","wordType":0,"xianhuoWordType":0},{"area":"","showWord":"<em>不锈</em>钢发条料","suggestWord":"不锈钢发条料","wordType":0,"xianhuoWordType":0}]
    """
    # input_dict = {"a": {"b": {"c": 1}}}  # 1
    # path = "a.b.c".split(".")
    # print(path[1:])
    # reg = ".*\[\d\]$"
    # print()
    jdict = json_loads_byteified(json2)
    path = ".suggestWord".split(".", maxsplit=20)
    # value = getNodeValue(jdict, path)
    # path = [".","suggestWord"]
    print(path)
    print(path[:1])
    print(path[-1])
    value = getNodesValues(jdict, path[:-1] , path[-1])
    # print(jdict)
    # print(jdict[0].get("suggestWord"))
    # print(path)
    test = ["111","222","333","3336"]
    print(test[:-1])
    print(value)