# import json as jn

import requests
from faker import Faker

"""
更新日志：
2021.10.29
    1. request_函数增加参数：verify=True、warning=True、allow_redirects=True

2021.10.28
    1. 增加函数：get_headers、requests_

"""


def get_headers(ua_type=None):
    """ 获取随机UA的headers字典

    创建时间：2021.10.28

    更新时间：2022.03.05

    更新日志
    2022.03.05：
        增加获取特定ua类型

    :return: 返回headers
    """
    ua = None
    if ua_type is None:
        ua = Faker().user_agent()
    elif ua_type == "chrome":
        ua = Faker().chrome()

    headers = {
        'User-Agent': ua
    }
    return headers


def get_ua(ua_type=None):
    """
    获取随机UA

    创建时间：2022.03.07

    :param ua_type: UA类型
    :return:
    """
    ua = None
    if ua_type is None:
        ua = Faker().user_agent()
    elif ua_type == "chrome":
        ua = Faker().chrome()

    return ua


def request_(url, proxies=None, verify=True, warning=True, allow_redirects=True, headers=None, ua_type=None,
             params=None, data=None,
             json=None,
             timeout=15,
             encoding='utf-8',
             ret_format='text'):
    """ 发送请求

    创建时间：2021.10.28

    更新时间：2022.03.15

    更新日志：
    2022.03.05:
        增加ua_type参数
    2022.03.15
        去掉字符串转json, 直接使用requests库自带的json参数(我就是个憨憨)

    :param url: 要请求的链接地址
    :param proxies: 设置代理，默认为 None
    :param verify: 是否验证 SSL证书
    :param warning: 是否忽略证书警告
    :param allow_redirects: 地址重定向，默认为 True
    :param headers: 携带的请求头，默认只有一个随机 UA的 headers
    :param ua_type: 要获取的ua类型
    :param params: 发送 get请求时所需要携带的参数
    :param data: 携带的请求参数，默认为 None
    :param json: 携带的 json类型的请求参数， 默认为 None
    :param timeout: 请求的超时时间，默认为 5
    :param encoding: 返回的编码类型， 默认为 utf-8
    :param ret_format: 返回的数据类型：包括 text, json, content, headers, res，默认text
    :return:
    """
    if not warning:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    if headers is None:
        headers = get_headers(ua_type)
    # 判断是否是post请求
    if data is not None:
        # 如果data不为空表示发送的是表单数据
        res = requests.post(url=url, proxies=proxies, verify=verify, allow_redirects=allow_redirects, headers=headers,
                            data=data)
    # 如果条件一不满足，则判断条件二是否满足，同样是post请求
    elif json is not None:
        # 如果json不为空，表示发送的是json字符串数据
        # json = jn.dumps(json)  # dumps传入的参数是字典对象，loads传入的参数是字符串
        res = requests.post(url=url, proxies=proxies, verify=verify, allow_redirects=allow_redirects, headers=headers,
                            json=json)
    # 如果以上条件都不满足，则表示发送的是get请求
    else:
        res = requests.get(url=url, proxies=proxies, verify=verify, allow_redirects=allow_redirects, headers=headers,
                           params=params, timeout=timeout)
    # 设置返回的数据编码类型
    res.encoding = encoding
    # 判断要返回什么类型的数据
    if ret_format == "json":
        # 返回json字符串
        return res.json()
    elif ret_format == 'content':
        # 返回二进制数据
        return res.content
    elif ret_format == 'headers':
        # 返回响应头
        return res.headers
    elif ret_format == 'res':
        # 返回响应对象
        return res
    # 默认返回text
    return res.text
