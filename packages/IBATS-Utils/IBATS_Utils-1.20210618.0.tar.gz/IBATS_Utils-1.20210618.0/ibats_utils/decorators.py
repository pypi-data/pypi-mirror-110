"""
@author  : MG
@Time    : 2021/5/14 11:11
@File    : decorators.py
@contact : mmmaaaggg@163.com
@desc    : 用于封装各种工具装饰器
"""
import functools
import logging
import threading
import time

logger = logging.getLogger(__name__)


def timer(func):
    """
    为当期程序进行计时
    :param func:
    :return:
    """

    @functools.wraps(func)
    def timer_func(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            estimate = time.strftime('%H:%M:%S', time.gmtime(end - start))
            logger.info('%s 运行时间：%s 相关参数 (%s, %s)', func.__name__, estimate, args, kwargs)

    return timer_func


def thread_save(func):
    """线程安全装饰器，用于该函数执行过程线程安全"""
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        with lock:
            func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":
    pass
