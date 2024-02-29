
import pytest
from myutils.myRequests import MyRequests
import allure
import os, time
from myutils.yamlutil import YamlUtil
from myutils import ddt

# 关联接口测试

class Testdemo:


    @allure.feature("关联接口测试")
    @pytest.mark.parametrize("url, header, method, param, expect, extract, feature, story",YamlUtil().read_casedata_yaml("case_data.yml"))
    def test_related_api_demo(self, url, header, method, param, expect,extract, feature, story ,cleanup):

        MyRequests().send_requests(method, url,
                                 header=header,
                                 param = param,
                                 expect = expect,
                                 extract = extract,
                                feature = feature,
                                   story = story)


