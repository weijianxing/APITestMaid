#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com

import urllib
from io import StringIO
from time import sleep
from urllib.request import urlopen
from urllib.parse import quote
import gzip
from util import logger
import urllib.error


def reRequest(delays=(2, 4, 6), exception=Exception):
    """
    rerequest the url when raise exception.
    :delays the time shoud be wait when fail
    :defail raise exception type

    """

    def decorator(function):
        """docstring for decorator"""

        def warp(*args, **kwargs):
            cnt = 0
            for delay in delays + (None,):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    if delay is None:
                        raise e
                    else:
                        cnt += 1
                        logger.log_warning("Exection found on connect retry %d: --retry after %ds" % (cnt, delay))
                    sleep(delay)

        return warp

    return decorator


def getUrlWithParamters(url, params: dict):

    url = url + '?'
    parmstr: str = ""
    firstParam: bool = True
    for (key, value) in params.items():
        if not firstParam:
            parmstr = parmstr + "&"
        parmstr += quote(key) + "=" + quote(str(value))
        firstParam = False
    return url + parmstr

#@reRequest()
def request(url, headers, postData=None, method = "GET"):
    """

    :param url:
    :param headers:
    :param cookies:
    :param postData:
    :return:
    """
    if headers is None:
        headers = {}
    try:
        if method == 'GET':
            if postData is not None:
                url = getUrlWithParamters(url, postData)
                logger.log_info("Get request URL is :  " + url)
            request = urllib.request.Request(url, None, headers)
        elif method == 'POST':
            params = urllib.parse.urlencode(postData)
            params = params.encode('utf-8')
            request = urllib.request.Request(url, data=params, headers=headers)
        else:

            raise urllib.error.URLError("method not defined.")


        resp = urllib.request.urlopen(request)
        if resp.info().get('Content-Encoding') == 'gzip':
            #buf = BytesIO(resp.read())
            f = gzip.decompress(mode = 'rb',fileobj=StringIO(resp.read()))
            r = str(f, 'utf-8')
        else:
            #decode with utf-8 solve response content contain chinese.
            r = str(resp.read(), 'utf-8')
            if r.startswith("jsonpCallback"):
                r = jsonp_2_json(r)
        return r, 200
    except Exception as e:
        logger.log_error("http tools request fail: " + str(e))
        # if the http status code 404 401 .. 500 , 501.. raise urllib.error.HTTPError
        return None, 450

def jsonp_2_json(jsonpdata: str = ""):
    prefixlen = "jsonpCallback(".__len__()
    return jsonpdata.strip()[prefixlen : -1]