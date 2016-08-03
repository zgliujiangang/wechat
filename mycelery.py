# coding: utf-8
import sys
sys.path.append('.')

import logging
import datetime
from celery import Celery

my_celery = Celery()



@my_celery.task
def async_task(func, args=[], kwargs={}):
    try:
        func(*args, **kwargs)
    except Exception as err:
        func_name = func.__name__
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        args = str(args)
        kwargs = str(kwargs)
        info = "time:%(time)s|func_name:%(func_name)s|error:%(err)s|args:%(args)s|kwargs:%(kwargs)s" % {"time": time, "func_name": func_name, "err": err, "args": args, "kwargs": kwargs}
        logging.info(info)


if __name__ == '__main__':
    my_celery.worker_main()
    
