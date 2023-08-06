#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/23 9:24 PM
# @Author  : zhengyu.0985
# @FileName: pyhive_test.py
# @Software: PyCharm

from pyhive import hive

conn = hive.Connection(
    host="",
    port=0,
    auth="CUSTOM",
    database="",
    username="zhengyu.0985",
    password=""
)

cursor = conn.cursor()
hive_sql = "select * from code_insights.dwd_code_coverage where date = '20220622'"
cursor.execute(hive_sql)
for tuple_result in cursor.fetchall():
    print(tuple_result)
cursor.close()
conn.close()
