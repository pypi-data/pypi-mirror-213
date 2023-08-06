import re

def split_(ori_str, start_str, end_str):
    """ 截取字符串

    创建时间：2021.10.28

    :param ori_str: 需要截取的原始字符串
    :param start_str:  开始的字符串，通过这个来获取开始截取的索引
    :param end_str: 结束的字符串， 通过这个来获取结束截取的索引
    :return:  返回截取后的字符串
    """
    start_index = ori_str.find(start_str) + len(start_str)  # 获取截取的开始索引
    end_index = ori_str.find(end_str)  # 获取截取的结束索引
    split_str = ori_str[start_index: end_index]  # 开始截取字符串
    return split_str


def filter_(ori_str, rep_str=None, to_str=None, mode=None, ):
    """ 过滤 / 替换 函数的综合

    创建时间：2021.10.29 20:53

    :param ori_str: 原始内容
    :param rep_str: 需要替换的字符，默认为 None
    :param to_str: 替换成的字符， 默认为 None
    :param mode: 替换模式，目前有 csv、filename，默认为None
    :return: 返回替换后的内容
    """
    if mode == 'csv':
        return filter_csv(ori_str)
    elif mode == 'filename':
        return filter_filename(ori_str)
    else:
        return filter_str(ori_str, rep_str, to_str)


def filter_str(ori_str, rep_str, to_str):
    """ 单次 /多次         过滤 / 替换 字符串

    创建时间：2021.10.29 20:50

    更新时间：2021.11.18 9:55

    :param ori_str: 原始内容
    :param rep_str: 要替换的字符（串），用 | 符号隔开，可以多次替换
    :param to_str: 替换成的字符（串），如果用 | 符号隔开，表示对应 rep_str修改
    :return: 返回替换后的内容
    """
    if rep_str is None or to_str is None:
        raise ValueError('请给rep_str和to_str赋值')
    is_split = False if rep_str.find('|') == -1 else True
    if is_split:
        rep_str_list = rep_str.split('|')
        for rep_str_index in range(len(rep_str_list)):
            is_split = False if to_str.find('|') == -1 else True
            if is_split:
                to_str_list = to_str.split('|')
                try:
                    ori_str = ori_str.replace(rep_str_list[rep_str_index], to_str_list[rep_str_index])
                except IndexError:
                    # 如果出现下标越界异常，那么默认采取替换字符串的最后一个为替换规则
                    ori_str = ori_str.replace(rep_str_list[rep_str_index], to_str_list[-1])
            else:
                ori_str = ori_str.replace(rep_str_list[rep_str_index], to_str)
        return ori_str
    else:
        return ori_str.replace(rep_str, to_str)


def filter_csv(ori_str, rep_str=',', to_str='，'):
    """ 过滤追加到 csv文件中的字符串内容中的指定字符（串）为指定字符（串）

    创建时间：2021.10.29 20:45

    :param ori_str: 原始内容
    :param rep_str: 需要替换的字符（串）， 默认为 ,（英文）
    :param to_str: 替换成的字符（串），默认为 ，（中文）
    :return: 返回替换后的内容
    """
    return ori_str.replace(rep_str, to_str)


def filter_filename(filename):
    """ 去除非法文件名

    创建时间：2021.10.28

    :param filename: 原始的文件名
    :return:  返回过滤后的文件名
    """
    return re.sub('[<>/\\\\|:"*?]', "_", filename)



