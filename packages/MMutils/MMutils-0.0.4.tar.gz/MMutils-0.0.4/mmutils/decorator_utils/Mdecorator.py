# @Time : 10/30/2021 10:49 AM
# @Author : MoMingLog
# @File : Mdecorator.py

import time
from threading import Lock

from mmutils.log_utils.Mlog import m_logger

lock = Lock()


def spend(func):
    """ 用于计算函数运行时间的装饰器

    创建时间：2021.11.01 12:41

    :param func:
    :return:
    """

    def run(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        end = time.time()
        spend_time = end - start
        m_logger.info(f"{func.__name__}花费的时间为；{spend_time}")
        return f

    return run


def tips_txt(func):
    """
    创建时间：2021.10.31 20:30

    :param func:
    :return:
    """

    def run(content: str):
        lock.acquire()
        m_logger.debug(f'正在写入数据{content}')
        f = func(content)
        m_logger.debug(f'数据写入完成'.center(50, '-'))
        lock.release()
        return f

    return run


def tips_csv(func):
    """ 用于存储数据到 csv 文件中时的提示装饰器

    创建时间：2021.10.30 10:50

    更新时间：2021.11.03 7:45

    :param func: 被装饰的函数
    :return:
    """

    @tips
    def run(item: dict):
        """ 实际运行的函数

        :param item: 要传入的参数
        :return:
        """
        # lock.acquire()
        # print(f'正在写入数据{item}')
        f = func(item)
        # print(f'数据写入完成'.center(50, '-'))
        # lock.release()
        return f

    return run


def tips(func):
    """ 用来提示的总函数

    创建时间：2021.11.03 7:45

    :param func:
    :return:
    """

    def run(*args, **kwargs):
        lock.acquire()
        print(f'正在写入数据{args[0] if len(args) == 1 else ""}{kwargs if len(kwargs) != 0 else ""}')
        f = func(*args, **kwargs)
        print('数据写入完成'.center(50, '-'))
        lock.release()
        return f

    return run

@spend
def test():
    time.sleep(1)

if __name__ == '__main__':
    test()