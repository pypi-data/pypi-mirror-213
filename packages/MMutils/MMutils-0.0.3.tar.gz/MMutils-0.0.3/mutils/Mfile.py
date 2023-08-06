import os

"""
更新日志：
2021.10.28
    1. 增加函数：folder

"""


def folder(path):
    """ 创建文件夹

    创建时间：2021.10.28

    :param path:
    :return: 返回原的路径最后不包含 / 符号
    """
    # 判断文件夹是否存在
    if not os.path.exists(path):
        # 如果文件夹不存在，则创建文件夹
        os.makedirs(path)  # makedirs创建多级目录
    if path[-1] == '/':
        # 去掉最后面的 / 符号
        return path[0: -1]
    return path
