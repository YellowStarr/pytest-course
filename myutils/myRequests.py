# -*- coding: utf-8 -*-
# ---
# @File: myRequests
# @Author: QiuWenJing
# @Time: 二月 02, 2024
# @Description: requests的二次封装
# ---
from myutils.yamlutil import YamlUtil
from myutils.myAssertion import MyAssertion
from myutils.myLog import MyLog
import requests
import json
import pytest
import jsonpath

class MyRequests:
    def __init__(self):
        pass

    def send_requests(self, method, url, **kwargs):
        MyLog.info("执行测试用例：{feature},{story}".format(feature=kwargs["feature"],story=kwargs["story"]))
        param = kwargs["param"]
        header = kwargs["header"]
        expect = kwargs["expect"]
        extract = kwargs["extract"]
        feature = kwargs["feature"]
        story = kwargs["story"]
        if param:
            param = YamlUtil().check_args(param)
        MyLog.info("发送请求，url：{url}, method: {method}, param: {param}".format(url=url, method=method,param=param))
        res = requests.request(method, url, json=param, headers=header)
        target = res.json()
        MyLog.info("接口响应内容: "+ json.dumps(target, ensure_ascii=False))
        # 提取中间变量
        if extract:
            param_ext = dict()
            if isinstance(extract, dict):
                for k,v in extract.items():
                    param_ext[k] = jsonpath.jsonpath(target, v)[0]
                MyLog.info("========提取到响应体内容 {f}, {v} =========".format(f=k, v=param_ext[k]))
            elif isinstance(extract, list):
                for i in range(len(extract)):
                    for k,v in extract[i].items():
                        param_ext[k] = jsonpath.jsonpath(target, v)[0]
                    MyLog.info("========提取到响应体内容 {f}, {v} =========".format(f=k, v=param_ext[k]))
            YamlUtil().write_temp_yaml(param_ext)

        # 验证点
        with pytest.raises(AssertionError):
            assert self._assert(target, expect)
        # assert self._assert(target, expect)
        MyLog.info("============={f},{s}执行结束==========".format(f=feature, s=story))


    def _assert(self, res, expect):
        """
        断点，第一个参数是实际值，第二个参数是期望值
        :param res:
        :param expect:
        :return:
        """
        for k,v in expect.items():
            # assert str(target[k]) == str(v)
            MyLog.info("解析验证点关键词：" + k)
            if hasattr(MyAssertion, k):
                print("assertion:",k)
                assertion = getattr(MyAssertion(), k)
                result = assertion(res, v)
                MyLog.info("测试用例执行结果: " + str(result))
                return result
                # MyLog.info("测试用例执行结果: " + result)
