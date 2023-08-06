from faker import Faker

faker = Faker()


def random_ua(ua_type=None) -> str:
    """
    获取随机UA

    创建时间：2022.03.07

    :param ua_type: UA类型
    :return:
    """
    ua = None
    if ua_type is None:
        ua = faker.user_agent()
    elif ua_type == "chrome":
        ua = faker.chrome()

    return ua


def add_random_ua_to_headers(headers, ua_type=None) -> dict:
    """
    在headers中添加随机UA

    :param headers: headers字典
    :param ua_type: UA类型
    :return: 返回headers
    """
    if headers is None:
        headers = {}
    headers['User-Agent'] = random_ua(ua_type=ua_type)
    return headers


def random_headers_with_ua(ua_type=None) -> dict:
    """
    获取随机headers, 包含随机UA
    :param ua_type:
    :return:
    """
    headers = {
        'User-Agent': random_ua(ua_type=ua_type)
    }
    return headers
