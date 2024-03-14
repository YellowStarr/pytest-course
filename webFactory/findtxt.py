# -*- coding: utf-8 -*-
# ---
# @File: findtxt
# @Author: QiuWenJing
# @Time: 三月 12, 2024
# @Description:
# ---
from webFactory.myDriver import MyDriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By

def write_to(name, content):
    with open(name, mode="a", encoding="utf-8") as f:
        f.write(content)
        f.close()

if __name__ == "__main__":
    url = "https://www.beqege.cc/15505/20673557.html"
    name ="第一序列"
    driver = MyDriver()
    d = driver.get_driver()

    while True:

        driver.open_Chrome(url)
        content = driver.find_Element("xpath", "//div[@id='content']")
        write_to(name, content.text)
        try:
            driver.find_Element("link", "下一章")
        except NoSuchElementException:
            break
        next = driver.find_Element("link", "下一章")
        url =driver.get_attr(next, "href")
        time.sleep(2)
        print(url)

    driver.close_Chrome()

