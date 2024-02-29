# -*- coding: utf-8 -*-
# ---
# @File: eastmoney_test
# @Author: QiuWenJing
# @Time: 二月 28, 2024
# @Description:
# ---
import pytest
from webFactory.eastFactory import EastFactory
import allure

# from myutils import ddt

class Test_EastMoney:

    @pytest.fixture(scope="class")
    def get_driver(self):
        url = "https://www.eastmoney.com/"
        web = EastFactory()
        web.open_Chrome(url)
        yield web
        web.close_Chrome()

    @allure.feature("网页搜索框测试")
    def test_web_search(self, get_driver):
        web = get_driver
        input = web.search_warehouse()
        web.action(input["search_input"], 'input', "000001")
        btn = input["search_btn"]
        web.action(btn, 'click')
        web.switch_handler()
        web.get_current_handler()
        el2 = web.find_Element('class', 'quote_title_name')
        assert web.get_attr(el2,'text') == '平安银行'

    @allure.feature("顶部导航栏")
    def test_web_nav(self, get_driver):
        web = get_driver
        web.switch_handler(0)
        links = web.nav_warehouse()
        links_text = []
        for i in range(len(links)):
            links_text.append(web.get_attr(links[i],'text'))
        assert "净值" in links_text



