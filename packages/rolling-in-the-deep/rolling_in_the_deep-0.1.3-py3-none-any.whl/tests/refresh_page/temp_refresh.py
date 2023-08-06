#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 9:03 下午
# @Author  : secret
# @FileName: temp_refresh.py
# @Software: PyCharm

# !/usr/bin/env python
# -*- coding: utf-8 -*-

#多线程刷浏览量脚本
#新华社接口
import requests
import threading

exitFlag = 0

req_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'gzip',
                'Connection': 'close',
                'Referer': None
                }


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        main(self.name, self.counter)
        print("Exiting " + self.name)


def main(threadName, delay):
    try:
        # url = "http://h.xinhuaxmt.com/vh512/share/10829661?channel=weixin"
        # url = "https://h.xinhuaxmt.com/vh512/share/11101730?d=1348bec&channel=weixin"
        url = "https://h.xinhuaxmt.com/vh512/share/11220930?isview=1&homeshow=0&newstype=1001"
        print("\nAccess web page start...")
        brushNum = 2000000
        # brushNum = 2
        for i in range(brushNum):
            print(threadName)

            # req = urllib2.Request(url, None, req_header)
            # resp = urllib2.urlopen(req, None, req_timeout)
            # html = resp.read()

            get_response = requests.get(url=url, headers=req_header)
            html = get_response.text
            # print("resp=", html)
            # print("geturl打印信息：%s" % (resp.geturl()))
            print("geturl打印信息：%s" % get_response.url)
            # print("info打印信息：%s" % (resp.info()))
            print("code打印信息：%s" % get_response.status_code)

            print("Success!\t", i + 1)
    except Exception as e:
        print(e.args)
        print('出错啦！')


if __name__ == '__main__':
    for t in range(10):
        myThread(t, "Thread-"+str(t), 1).start()
