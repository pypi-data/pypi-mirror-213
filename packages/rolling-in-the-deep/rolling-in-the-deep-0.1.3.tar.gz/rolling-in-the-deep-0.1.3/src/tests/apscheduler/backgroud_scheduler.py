    #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 2:20 PM
# @Author  : zhengyu.0985
# @FileName: backgroud_scheduler.py
# @Software: PyCharm
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
#########################################################
# 调度器
scheduler = BackgroundScheduler()
scheduler.start()
# 执行器, 在定时任务该执行时，以进程或线程方式执行任务
# 线程方式：ThreadPoolExecutor
thread_executor = ThreadPoolExecutor(10)
scheduler.add_executor(thread_executor, 'thread_exe')

# 线程方式：ThreadPoolExecutor
process_executor = ProcessPoolExecutor(10)
scheduler.add_executor(process_executor, 'process_exe')

scheduler.shutdown()
#########################################################

# 或者
executors = {
    'thread_exe': ThreadPoolExecutor(10),
    'process_exe': ProcessPoolExecutor(10)
}
# 方式一
scheduler = BackgroundScheduler(executors=executors)
scheduler.start()  # 此处程序不会发生阻塞
# 方式二
sched = BackgroundScheduler()
sched.configure(executors=executors)
sched.start()  # 此处程序不会发生阻塞


def my_func(name: str):
    print(f'name={name}')


# 方式一
job = scheduler.add_job(my_func, 'interval', ['scheduler_2s'], seconds=2)
job.pause()
# 修改job
job.modify(max_instances=6, name='new_name')
job.resume()
# job.remove()


# 方式二
sched.add_job(my_func, 'interval', args=['sched_5s'], seconds=5, id='my_job_id')
sched.pause_job(job_id='my_job_id')
sched.resume_job(job_id='my_job_id')
# sched.remove_job(job_id='my_job_id')
# 调整任务调度周期
# sched.reschedule_job(job_id='my_job_id', trigger='cron')

# 需要主线程一直运行。否则主线程停止后，BackgroundScheduler也会停止。
try:
    while True:
        time.sleep(1)
except Exception as e:
    print(e.args)
    # 停止APScheduler运行
    scheduler.shutdown()
    sched.shutdown()

