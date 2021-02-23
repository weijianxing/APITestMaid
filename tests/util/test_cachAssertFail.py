#-*- coding: utf-8 -*-
# ------ wuage.com testing team ---------
# __author__ : jianxing.wei@wuage.com
import sys
import traceback

def log_assertFail():
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)  # Fixed format
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]

    # print('An error occurred on line {} in statement {}'.format(line, text))
    return 'Assert fail on line {} in statement {}'.format(line, text)

def test_assert_fail():

    try:
        assert True
        assert 7 == 7
        assert 1 == 2, "xxxxx 1 not equal 2"
        # many more statements like this
    except AssertionError:
       print(log_assertFail())

if __name__ == '__main__':
    test_assert_fail()