import os
import re


def folder(path):
    """ 创建文件夹

    创建时间：2021.10.28

    :param path: 文件夹路径
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


def replace_invalid_filename_char(filename, replaced_char='_'):
    """ 去除非法文件名

    创建时间：2021.10.28

    :param filename: 原始的文件名
    :param replaced_char: 替换非法字符的字符
    :return:  返回过滤后的文件名
    """
    return re.sub('[<>/\\\\|:"*?]', replaced_char, filename)
