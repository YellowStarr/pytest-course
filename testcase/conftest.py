# -*- coding: utf-8 -*-
# ---
# @File: conftest
# @Author: QiuWenJing
# @Time: 二月 03, 2024
# @Description: 清理中间生成数据
# ---
import pytest
from myutils.yamlutil import YamlUtil

@pytest.fixture(scope='class', autouse=True)
def cleanup():
    yield
    YamlUtil().clear_yaml_temp()