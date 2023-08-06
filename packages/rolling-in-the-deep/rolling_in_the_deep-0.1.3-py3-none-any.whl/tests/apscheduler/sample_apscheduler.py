#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 4:51 PM
# @Author  : zhengyu.0985
# @FileName: sample_apscheduler.py
# @Software: PyCharm

import asyncio
import datetime
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.executors.asyncio import AsyncIOExecutor
# from apscheduler.jobstores.redis import RedisJobStore  # 需要安装redis
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import functools
import os
import signal

# 定义jobstore  使用redis 存储job信息
# default_redis_jobstore = RedisJobStore(
#
#     db=2,
#
#     jobs_key="apschedulers.default_jobs",
#
#     run_times_key="apschedulers.default_run_times",
#
#     host="127.0.0.1",
#
#     port=6379,
#
#     password="test"
#
# )

default_memory_jobstore = MemoryJobStore()

# 定义executor 使用asyncio是的调度执行规则

first_executor = AsyncIOExecutor()

# 初始化scheduler时，可以直接指定jobstore和executor

init_scheduler_options = {

    "jobstores": {

        # first 为 jobstore的名字，在创建Job时直接直接此名字即可

        "default": default_memory_jobstore

    },

    "executors": {

        # first 为 executor 的名字，在创建Job时直接直接此名字，执行时则会使用此executor执行

        "first": first_executor

    },

    # 创建job时的默认参数

    "job_defaults": {

        'coalesce': False,  # 是否合并执行

        'max_instances': 1  # 最大实例数

    }

}

# 创建scheduler

scheduler = AsyncIOScheduler(**init_scheduler_options)

# 启动调度

scheduler.start()  # 先启动，后添加job

# 第二个存储器
# second_redis_jobstore = RedisJobStore(
#
#     db=2,
#
#     jobs_key="apschedulers.second_jobs",
#
#     run_times_key="apschedulers.second_run_times",
#
#     host="127.0.0.1",
#
#     port=6379,
#
#     password="test"
#
# )

second_sqlalchemy_jobstore = SQLAlchemyJobStore(url='sqlite:////Users/admin/jobs.sqlite')

scheduler.add_jobstore(second_sqlalchemy_jobstore, 'second')

# 定义executor 使用asyncio是的调度执行规则

second_executor = AsyncIOExecutor()

scheduler.add_executor(second_executor, "second")


# ***********               关于 APScheduler中有关Event相关使用示例               *************

# 定义函数监听事件

def job_execute(event):
    """

    监听事件处理

    :param event:

    :return:

    """
    print(type(event))
    print(

        "job执行job:\ncode => {}\njob.id => {}\njobstore=>{}".format(

            event.code,

            event.job_id,

            event.jobstore

        ))


# 给EVENT_JOB_EXECUTED[执行完成job事件]添加回调，这里就是每次Job执行完成了我们就输出一些信息

scheduler.add_listener(job_execute, EVENT_JOB_EXECUTED)


# ***********               关于 APScheduler中有关Job使用示例               *************

# 使用的是asyncio，所以job执行的函数可以是一个协程，也可以是一个普通函数，AsyncIOExecutor会根据配置的函数来进行调度，

# 如果是协程则会直接丢入到loop中，如果是普通函数则会启用线程处理

# 我们定义两个函数来看看执行的结果

def interval_func(message):
    print("现在时间： {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    print("我是普通函数")

    print(message)


async def async_func(message):
    print("现在时间： {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    print("我是协程")

    print(message)


# 将上述的两个函数按照不同的方式创造触发器来执行

# ***********               关于 APScheduler中有关Trigger使用示例               *************

# 使用Trigger有两种方式，一种是用类创建使用，另一个是使用字符串的方式

# 使用字符串指定别名， scheduler初始化时已将其定义的trigger加载，所以指定字符串可以直接使用

if scheduler.get_job("interval_func_test", "default"):
    # 存在的话，先删除

    scheduler.remove_job("interval_func_test", "default")

# 立马开始 2分钟后结束， 每10s执行一次 存储到first jobstore  second执行

scheduler.add_job(interval_func, "interval",

                  args=["我是10s执行一次，存放在jobstore default, executor default"],

                  seconds=10,

                  id="interval_func_test",

                  jobstore="default",

                  executor="default",

                  start_date=datetime.datetime.now(),

                  end_date=datetime.datetime.now() + datetime.timedelta(seconds=240))

# 先创建tigger

trigger = IntervalTrigger(seconds=5)

if scheduler.get_job("interval_func_test_2", "second"):
    # 存在的话，先删除

    scheduler.remove_job("interval_func_test_2", "second")

# 每隔5s执行一次

scheduler.add_job(async_func, trigger, args=["我是每隔5s执行一次，存放在jobstore second, executor = second"],

                  id="interval_func_test_2",

                  jobstore="second",

                  executor="second")

# 使用协程的函数执行，且使用cron的方式配置触发器

if scheduler.get_job("cron_func_test", "default"):
    # 存在的话，先删除

    scheduler.remove_job("cron_func_test", "default")

# 立马开始 每10s执行一次

scheduler.add_job(async_func, "cron",

                  args=["我是 每分钟 30s  时执行一次，存放在jobstore default, executor default"],

                  second='30',

                  id="cron_func_test",

                  jobstore="default",

                  executor="default")

# 先创建tigger

trigger = CronTrigger(second='20,40')

if scheduler.get_job("cron_func_test_2", "second"):
    # 存在的话，先删除

    scheduler.remove_job("cron_func_test_2", "second")

# 使用创建的trigger对象直接创建
scheduler.add_job(async_func, trigger, args=["我是每分钟 20s  40s时各执行一次，存放在jobstore second, executor = second"],

                  id="cron_func_test_2",

                  jobstore="second",

                  executor="second")


# 优雅退出
def loop_exit(loop_var, signal_name):
    """
    信号值      符号      行为
    2          SIGINT    进程终端，CTRL+C
    9          SIGKILL   强制终端
    15         SIGTEM    请求中断
    20         SIGTOP    停止（挂起）进程 CRTL+D
    """
    print(f"获取信号{signal_name}: exit")
    loop_var.stop()  # 停止


if __name__ == '__main__':

    print("启动: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # asyncio.get_event_loop().run_forever()

    # 以下为可以优雅退出的启动方式
    loop = asyncio.get_event_loop()
    for sign_name in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sign_name),
                                functools.partial(loop_exit, loop, sign_name))

    print(" Ctrl+C 停止运行.")
    print(f"pid {os.getpid()}: 发送 SIGINT 和 SIGTERM 信号退出循环")
    try:
        loop.run_forever()
    finally:
        loop.close()  # 关闭
