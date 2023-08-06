#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 5:53 下午
# @Author  : zhengyu.0985
# @FileName: data_analysis.py
# @Software: PyCharm

import time

from src.rolling_king.jason.webdriver.webdriver_common import WebDriverCommon
from src.rolling_king.jason.python.tools.zy_stamp_tool import TimeStampExchange
# httpSender = HttpSender("https://h.xinhuaxmt.com")
# httpSender.send_get_request_by_suburi("/905/n/newsapi/h5/news-detail/detail", {'docid': 10829661, 'share': 1})
# print(httpSender.get_response.text)

WebDriverCommon.init_driver(executable_path='./chromedriver')
WebDriverCommon.navigate("https://h.xinhuaxmt.com/vh512/share/11101730?d=1348bec&channel=weixin")
count = 0
while True:
    count += 1
    if count % 10 == 0:
        print("第" + str(count) + "次，时间：" + TimeStampExchange.stamp2datetime())
    WebDriverCommon.refresh()



