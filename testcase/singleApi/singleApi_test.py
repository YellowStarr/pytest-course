# -*- coding: utf-8 -*-
# ---
# @File: singleApi_test
# @Author: QiuWenJing
# @Time: 二月 03, 2024
# @Description: 单接口数据驱动
# ---
import pytest
from myutils.myRequests import MyRequests
import allure

from myutils import ddt

class Test_Single:
    @allure.feature("单接口数据驱动")
    @pytest.mark.parametrize("url, header, method, param, expect, extract, feature, story",ddt.read_testcase("json_get_test.yml"))
    def test_single_api_demo(self, url, header, method, param, expect,extract, feature, story ,cleanup):

        MyRequests().send_requests(method, url,
                                   header=header,
                                   param = param,
                                   expect = expect,
                                   extract = extract,
                                   feature = feature,
                                   story = story)

