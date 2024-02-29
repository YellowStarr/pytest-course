# -*- coding: utf-8 -*-
# ---
# @File: run_case
# @Author: QiuWenJing
# @Time: 二月 03, 2024
# @Description:
# ---
import time,os
import pytest


if __name__ == "__main__":
    pytest.main()
    time.sleep(3)
    # pytest.main(['-vs', "--html=./reports/report.html" ])
    os.system("allure generate ./temps -o ./reports --clean")
