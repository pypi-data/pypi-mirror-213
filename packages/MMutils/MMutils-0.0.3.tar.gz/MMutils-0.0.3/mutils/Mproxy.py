# @Time : 10/30/2021 2:22 PM
# @Author : MoMingLog
# @File : Mproxy.py
# @Software: PyCharm

import random
import time
import csv
import re
from queue import Queue

from lxml import etree
from Mcaptcha import discern_ocr
from Mrequests import request_, get_headers
from Mlog import m_logger
from threading import Thread

"""
更新日志：
2021.10.30
    1. 增加工具函数parse_by_xpath、check_usable


"""


def check_usable(item, save_item=None):
    """ 检测代理是否可用

    创建时间：2021.10.30 14:30

    :param item:
    :return:
    """
    if save_item is None:
        raise ValueError('请传入对可用代理数据进行持久化存储的函数！')
    else:
        # 下方通过在百度搜索“ip”的结果来测试代理是否可用
        url = 'https://www.baidu.com/s?wd=%E6%9C%AC%E6%9C%BAip'
        headers = get_headers(ua_type='chrome')
        headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Cookie": "BIDUPSID=417DCCD8A89DCD48C058253549BAFC98; PSTM=1652451950; BAIDUID=417DCCD8A89DCD488051FFBBCE3C78FA:SL=0:NR=10:FG=1; NOJS=1; BDUSS=WhVZmxmZnY4UUZZWm5GZm5ORVJFNWRiWXlsUFViQll0akdlNnNVMEFiOVFoMVJrSVFBQUFBJCQAAAAAAAAAAAEAAADyZor21MLTsNDHs71f0rnJqwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFD6LGRQ-ixkL; BDUSS_BFESS=WhVZmxmZnY4UUZZWm5GZm5ORVJFNWRiWXlsUFViQll0akdlNnNVMEFiOVFoMVJrSVFBQUFBJCQAAAAAAAAAAAEAAADyZor21MLTsNDHs71f0rnJqwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFD6LGRQ-ixkL; ISSW=1; ISSW=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=38516_36544_38686_38860_38795_38755_38768_38486_38808_38822_38637_38764_26350_22159; BA_HECTOR=a4a42k8k2k0581a02h8l844n1i83sno1m; ZFY=5PXDGebmAhgKXNVJFPjDnyW0i39thwIeLGugKITJzwo:C; BAIDUID_BFESS=417DCCD8A89DCD488051FFBBCE3C78FA:SL=0:NR=10:FG=1; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; sug=3; sugstore=1; ORIGIN=2; bdime=0; H_PS_645EC=3addo3vWFEgz18E1b%2FteaT%2FJ62mNKIH0xav7W3YSF%2FmFkoXQMp72Ym6xWIrKPPwQeK9a",
            "Host": "www.baidu.com"

        })
        proxies = {
            'http': f'http://{item.get("ip")}:{item.get("port")}',
            'https': f'http://{item.get("ip")}:{item.get("port")}'
        }

        try:
            page_text = request_(url=url, proxies=proxies, headers=headers, timeout=10)
            if page_text:
                match_list = re.findall("本机IP", page_text)

                if match_list:
                    save_item(item)
                else:
                    m_logger.debug(page_text)
        except Exception as te:
            m_logger.exception(f"代理 {item.get('ip')}:{item.get('port')} 不可用！")


def parse_by_xpath(*args, is_ip_domain=False, check_usable_func=check_usable, save_item=None):
    """通过 xpath 来获取 ip 和 port

    创建时间：2021.10.30 14.22

    :param args: 实际最大参数为 5个：page_text、ip_xpath、port_xpath、ip_port_xpath、domain，程序会自动根据传进来的参数个数判断执行
    :param is_ip_domain: 如果 domain不是 None 则需要通过这个参数来判断图片状态的是 ip（True） 还是 port（False），又或者两者都有（both）
    :param check_usable_func: 检测代理是否可用的函数，默认为工具函数check_usable
    :param save_item: 保存可用代理的函数
    :return:
    """
    page_text = args[0]  # 网页源代码
    ip_xpath = None  # ip对应的 xpath，默认为 None
    port_xpath = None  # 对应的 xpath, 默认为 None
    ip_port_xpath = None  # 当 抓取的数据是 “ip:port”形式的时候使用这个参数，默认值为 None
    domain = None  # 如果存在图片形式的，则使用这个参数，默认值为None
    ip_domain = None
    port_domain = None
    args_num = len(args)
    if args_num == 3:
        ip_xpath = args[1]
        port_xpath = args[2]
    elif args_num == 2:
        ip_port_xpath = args[1]
    elif args_num == 4:
        ip_xpath = args[1]
        port_xpath = args[2]
        domain = args[3]
        if is_ip_domain == 'both':
            ip_domain = domain
            port_domain = domain
        elif is_ip_domain:
            ip_domain = domain
        elif not is_ip_domain:
            port_domain = domain

    element = etree.HTML(page_text)
    if ip_port_xpath is None:
        ip_ = element.xpath(ip_xpath)
        port_ = element.xpath(port_xpath)
        for ip, port in zip(ip_, port_):
            item = {
                # 使用三元运算，判断domain参数是否为空，如果不为空，则表示该网站使用了反爬，需要我们识别出ip或port
                # 判断 ip_domain 是否为空，如果不为空，则识别图片
                'ip': ip.strip() if ip_domain is None else discern_ocr(request_(url=domain + ip, ret_format='content')),
                # 判断port_domain是否为空，如果不为空，则识别图片
                'port': port.strip() if port_domain is None else discern_ocr(
                    request_(url=domain + port, ret_format='content'))
            }
            Thread(target=check_usable_func, args=(item, save_item)).start()
    else:
        ip_port_ = element.xpath(ip_port_xpath)
        for ip_port in ip_port_:
            ip_port_list = ip_port.split(':')
            item = {
                # 使用三元运算，判断domain参数是否为空，如果不为空，则表示该网站使用了反爬，需要我们识别出ip或port
                'ip': ip_port_list[0].strip() if ip_domain is None else discern_ocr(
                    request_(domain + ip_port_list[0], ret_format='content')),
                'port': ip_port_list[1].strip() if port_domain is None else discern_ocr(
                    request_(domain + ip_port_list[1], ret_format='content'))
            }
            Thread(target=check_usable_func, args=(item, save_item)).start()


def check_proxy(ip, port) -> bool:
    url = 'http://www.baidu.com/s?ie=UTF-8&wd=本机ip'
    headers = get_headers()
    headers['Referer'] = 'https://www.baidu.com/'
    headers[
        'Cookie'] = 'BIDUPSID=D29624969C39994D9D17480DCF65EDB1; PSTM=1630857355; BAIDUID=D29624969C39994D183522665890A809:FG=1; BD_UPN=12314753; __yjs_duid=1_679dab97d101a0326f13b9a8a808bc0a1631104777407; H_WISE_SIDS=107314_110085_127969_131861_175668_175755_176399_177370_178384_178529_178634_179349_179458_179620_181106_181136_181251_181399_181588_181676_181712_182000_182530_183239_183330_183536_183611_183626_183869_183979_184042_184200_184267_184319_184326_184793_184809_184876_184894_185252_185275_185300_185519_185653_185746_185904_186026_186113_186313_186319_186412_186446_186455_186508_186595_186625_186643_186899_187067_187121_187185_187202_187214_187289_187325_187487_187563; MSA_WH=360_640; BDSFRCVID_BFESS=zJAOJexroG0vH6JHEJNeMdhrmmKKvV3TDYLtOwXPsp3LGJLVgWj3EG0PtoaGdu_-ox8EogKKQgOTHRCF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tRk8oI0aJDvDqTrP-trf5DCShUFsaJjWB2Q-XPoO3KJOqhuGy-A53Iu7jRnPQtbiW5cpoMbgylRM8P3y0bb2DUA1y4vpKhbBt2TxoUJ2abjne-53qtnWeMLebPRiQ4b9QgbN5hQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wD5thj6PVKgTa54cbb4o2WbCQMqcN8pcN2b5oQT8ByajZBUQZBDTu0nn-aR6vOPQKDpOUWfA3XpJvQnJjt2JxaqRC5M38hp5jDh3MhP_1bhode4ROfgTy0hvcLR3cShn-LUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQh-p52f6LetJcP; BDUSS=tiNzBNaDZPbEszLUh2dUVVM2ZQSzhaMXhPNmpKMGltc3M5LWMtb2RuSGh5SkZoSVFBQUFBJCQAAAAAAAAAAAEAAADyZor21MLTsNDHs71f0rnJqwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOE7amHhO2phb2; BDUSS_BFESS=tiNzBNaDZPbEszLUh2dUVVM2ZQSzhaMXhPNmpKMGltc3M5LWMtb2RuSGh5SkZoSVFBQUFBJCQAAAAAAAAAAAEAAADyZor21MLTsNDHs71f0rnJqwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOE7amHhO2phb2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=34947_34446_34067_31253_34967_34584_34517_34917_26350_34971_34868; channel=baidusearch; BAIDUID_BFESS=C3C7190A243B9F151317E636ACA16207:FG=1; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=5; H_PS_645EC=4665hF0GZnaGNwwZKaZxseXN9MXz99QpMkdK%2BtEvV2ySA7GJ0L7mPOA2nUo; BA_HECTOR=0l0l812h252l0h810r1gnprf90q; COOKIE_SESSION=597_0_5_2_11_2_1_0_5_2_0_0_45301_0_0_0_1635557263_0_1635577320%7C9%230_0_1635577320%7C1; baikeVisitId=a6cde87f-c5dd-4412-8f2f-c203b8eebe3f'
    proxies = {
        'http': 'http://' + ip + ':' + port,
        'https': 'http://' + ip + ':' + port
    }

    try:
        page_text = request_(url=url, proxies=proxies, headers=headers, timeout=6)
        if page_text:
            match_list = re.findall("本机IP", page_text)
            if match_list:
                m_logger.debug(f"代理：{ip}:{port}，请求成功")
                return True
            else:
                m_logger.debug(f"代理：{ip}:{port}，请求失败")
                return False
        else:
            m_logger.debug("请求失败")
            return False
    except Exception as te:
        m_logger.error(f"代理：{ip}:{port}，请求失败, 异常")
        return False


import os


def get_available_proxy(
        num: int = 1,
        file_data=None,
        file_path: str = None,
        is_recheck: bool = False,
) -> list:
    """获取可用代理

    创建时间：2023.6.8

    :param file_path: 代理文件路径
    :param num: 需要获取的代理数量
    :param is_recheck: 是否需要重新检测代理
    :return:
    """
    if file_data is None:
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), 'proxies.csv')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            proxies = list(reader)
    else:
        reader = csv.reader(file_data)
        next(reader)
        proxies = list(reader)

    ret_data = []
    for proxy in proxies:
        if not proxy:
            continue
        ip = proxy[0]
        port = proxy[1]
        if is_recheck:
            if check_proxy(ip, port):
                ret_data.append(proxy)
                if len(ret_data) == num:
                    break
        else:
            ret_data.append(proxy)
            if len(ret_data) == num:
                break

    return ret_data


import concurrent.futures
import threading


class SpiderProxy:
    def __init__(self):
        self.proxies = []
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    def __proxy_89ip(self, max_num=6):
        """ 爬取 https://www.89ip.cn/index_1.html

            :param max_num: 爬取的最大页数， 默认为 6
            :return:
            """
        for i in range(1, max_num + 1):
            url = f'https://www.89ip.cn/index_{i}.htmls'
            page_text = request_(url=url)
            ip_xpath = '//div[@class="fly-panel"]//tbody/tr/td[1]/text()'
            port_xpath = '//div[@class="fly-panel"]//tbody/tr/td[2]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath
            )

    def __proxy_nima(self, max_num=6):
        """ 爬取 http://www.nimadaili.com/

        【 Tips】更新间隔长

        1. 国内普通代理：http://www.nimadaili.com/putong/
        2. 国内高匿代理：http://www.nimadaili.com/gaoni/ 【爬取对象】
        3. 国内 HTTP：http://www.nimadaili.com/http/
        4. 国内 HTTPS：http://www.nimadaili.com/https/

        :param max_num: 爬取的最大页数，默认为 6
        :return:
        """
        for i in range(1, max_num + 1):
            url = f'http://www.nimadaili.com/gaoni/{i}/'
            page_text = request_(url=url)
            ip_port_xpath = '//table[@class="fl-table"]/tbody/tr/td[1]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_port_xpath
            )

    def __proxy_kaixin(self, max_num=6):
        """ 爬取 http://www.kxdaili.com/dailiip.html

        :param max_num:  爬取的最大页数，默认为 6
        :return:
        """
        for i in range(1, max_num + 1):
            url = f'http://www.kxdaili.com/dailiip/1/{i}.htmls'
            page_text = request_(url=url)
            ip_xpath = '//table[@class="active"]//tbody/tr/td[1]/text()'
            port_xpath = '//table[@class="active"]//tbody/tr/td[2]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath
            )

    def __proxy_mipu(self, max_num=6):
        """ 爬取 https://proxy.mimvp.com/freeopen

        【 Tips】这个网站的端口为图片形式，所以需要特殊处理

        :param max_num: 爬取的最大页数，默认为 6
        :return:
        """
        for i in range(1, max_num + 1):
            url = f'https://proxy.mimvp.com/freeopen?proxy=in_hp&sort=&page={i}'
            page_text = request_(url=url)
            ip_xpath = '//table[@class="mimvp-tbl free-proxylist-tbl"]//tbody/tr/td[2]/text()'
            port_xpath = '//table[@class="mimvp-tbl free-proxylist-tbl"]//tbody/tr/td[3]/img/@src'
            domain = 'https://proxy.mimvp.com'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath,
                domain
            )

    def __proxy_zdaye(self, max_num=6):
        """ 爬取 https://www.zdaye.com/Free/

        【 Tips】 这个网站有反爬措施，如果不加 Referer的话，貌似再多次访问后会封禁 ip，封禁时间未测试

        :param max_num: 爬取的最大页数，默认为 6
        :return:
        """
        for i in range(1, max_num + 1):
            url = f'https://www.zdaye.com/free/{i}/'
            headers = get_headers()
            headers['Referer'] = 'https://www.zdaye.com/'
            # headers['Cookie'] = '__51vcke__1vh212XjimTsXGR8=6d56db57-69de-5f66-9239-7805d8214b1c; __51vuft__1vh212XjimTsXGR8=1635559887738; __root_domain_v=.zdaye.com; _qddaz=QD.999935559888059; ASPSESSIONIDCERASART=NFJJMNECNEKNMEIHCNKIGONA; ASPSESSIONIDCETBSDSR=MDCIPHHCMNNCHOCKKCDFHKMJ; __51uvsct__1vh212XjimTsXGR8=2; _qdda=3-1.3eaw95; _qddab=3-rw3ohm.kvdiuyjp; lastSE=baidu; acw_tc=2f624a7216355816418236717e35c17e3ff2562d2380cae09a05e73f25d7a3; __vtins__1vh212XjimTsXGR8={"sid": "e5c5030e-0037-59b4-97f8-2e7aa2d1df65", "vd": 7, "stt": 1943970, "dr": 393602, "expires": 1635583479751, "ct": 1635581679751}; Hm_lvt_80f407a85cf0bc32ab5f9cc91c15f88b=1635559888,1635559918,1635581272,1635581680; Hm_lpvt_80f407a85cf0bc32ab5f9cc91c15f88b=1635581680'
            page_text = request_(url=url, encoding='gb2312')
            ip_xpath = '//table[@id="ipc"]//tbody/tr/td[1]/text()'
            port_xpath = '//table[@id="ipc"]//tbody/tr/td[2]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath
            )

    def __proxy_kdl(self, max_num=6):
        """ 爬取 https://www.kuaidaili.com/free/inha/

        :param max_num: 爬取的最大页数，默认为 6
        :return:
        """

        for i in range(1, max_num + 1):
            url = f'https://www.kuaidaili.com/free/inha/{i}/'
            page_text = request_(url=url)
            ip_xpath = '//div[@id="list"]//tbody/tr/td[1]/text()'
            port_xpath = '//div[@id="list"]//tbody/tr/td[2]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath
            )

    def __proxy_ydl(self, max_num=6):
        """ 爬取 http://www.ip3366.net/free/?stype=1

        :param max_num: 爬取的最大页数，默认为 6
        :return:
        """
        for i in range(1, max_num + 1):
            url = f'http://www.ip3366.net/free/?stype=1&page={i}'
            page_text = request_(url)
            ip_xpath = '//div[@id="list"]//tbody/tr/td[1]/text()'
            port_xpath = '//div[@id="list"]//tbody/tr/td[2]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath
            )

    def __proxy_xhuan(self, max_num=6):
        """ 爬取 https://ip.ihuan.me/

        【 Tips】 该网站的页码链接做了反爬措施，但我们可以通过点击下一页的方法来实现页码的跳转，所以我们需要获取下一页的链接

        :param max_num: 爬取的最大页数，默认为 6
        :return:
        """

        def get_next_page_url(page_text):
            """ 用来获取下一页的链接

            :param page_text: 页面源代码
            :return:
            """
            element = etree.HTML(page_text)
            next_page = element.xpath('//a[@aria-label="Next"]/@href')
            if next_page is not None:
                next_url = 'https://ip.ihuan.me/' + next_page[0]
                return next_url
            else:
                return None

        url = 'https://ip.ihuan.me/'  # 通过主页链接获取下一页的链接
        page_text = request_(url)
        next_page_url = get_next_page_url(page_text=page_text)
        while next_page_url is not None:
            ip_xpath = '//div[@class="table-responsive"]//tbody/tr/td[1]/a/text()'
            port_xpath = '//div[@class="table-responsive"]//tbody/tr/td[2]/text()'
            self.__parse_by_xpath(
                page_text,
                ip_xpath,
                port_xpath
            )
            page_text = request_(next_page_url)
            next_page_url = get_next_page_url(page_text=page_text)

    def __parse_by_xpath(self, *args, is_ip_domain=False):
        """通过 xpath 来获取 ip 和 port

        创建时间：2021.10.30 14.22

        :param args: 实际最大参数为 5个：page_text、ip_xpath、port_xpath、ip_port_xpath、domain，程序会自动根据传进来的参数个数判断执行
        :param is_ip_domain: 如果 domain不是 None 则需要通过这个参数来判断图片状态的是 ip（True） 还是 port（False），又或者两者都有（both）
        :return:
        """
        page_text = args[0]  # 网页源代码
        ip_xpath = None  # ip对应的 xpath，默认为 None
        port_xpath = None  # 对应的 xpath, 默认为 None
        ip_port_xpath = None  # 当 抓取的数据是 “ip:port”形式的时候使用这个参数，默认值为 None
        domain = None  # 如果存在图片形式的，则使用这个参数，默认值为None
        ip_domain = None
        port_domain = None
        args_num = len(args)
        if args_num == 3:
            ip_xpath = args[1]
            port_xpath = args[2]
        elif args_num == 2:
            ip_port_xpath = args[1]
        elif args_num == 4:
            ip_xpath = args[1]
            port_xpath = args[2]
            domain = args[3]
            if is_ip_domain == 'both':
                ip_domain = domain
                port_domain = domain
            elif is_ip_domain:
                ip_domain = domain
            elif not is_ip_domain:
                port_domain = domain

        def run(item):
            # Thread(target=check_usable_func, args=(item, save_item)).start()
            if check_proxy(item['ip'], item['port']):
                self.proxies.append(item)

        element = etree.HTML(page_text)
        if ip_port_xpath is None:
            ip_ = element.xpath(ip_xpath)
            port_ = element.xpath(port_xpath)
            for ip, port in zip(ip_, port_):
                item = {
                    # 使用三元运算，判断domain参数是否为空，如果不为空，则表示该网站使用了反爬，需要我们识别出ip或port
                    # 判断 ip_domain 是否为空，如果不为空，则识别图片
                    'ip': ip.strip() if ip_domain is None else discern_ocr(
                        request_(url=domain + ip, ret_format='content')),
                    # 判断port_domain是否为空，如果不为空，则识别图片
                    'port': port.strip() if port_domain is None else discern_ocr(
                        request_(url=domain + port, ret_format='content'))
                }
                Thread(target=run, args=(item,)).start()

        else:
            ip_port_ = element.xpath(ip_port_xpath)
            for ip_port in ip_port_:
                ip_port_list = ip_port.split(':')
                item = {
                    # 使用三元运算，判断domain参数是否为空，如果不为空，则表示该网站使用了反爬，需要我们识别出ip或port
                    'ip': ip_port_list[0].strip() if ip_domain is None else discern_ocr(
                        request_(domain + ip_port_list[0], ret_format='content')),
                    'port': ip_port_list[1].strip() if port_domain is None else discern_ocr(
                        request_(domain + ip_port_list[1], ret_format='content'))
                }
                Thread(target=run, args=(item,)).start()

    def spider(self, func):
        # 将所有解析免费代理的功能函数封装到一个列表中
        proxy_func_list = [
            self.__proxy_89ip,
            self.__proxy_nima,
            self.__proxy_kaixin,
            self.__proxy_mipu,
            self.__proxy_zdaye,
            self.__proxy_kdl,
            self.__proxy_ydl,
            self.__proxy_xhuan
        ]

        # 遍历列表，将每个功能函数提交给线程池
        future_list = [self._executor.submit(func) for func in proxy_func_list]

        # 运行传进来的功能函数
        func()

        # 等待所有线程执行完毕
        concurrent.futures.wait(future_list)


class GenerateProxy(SpiderProxy):
    CSV_FILE_NAME = 'proxies.csv'
    FILTER_CSV_FILE_NAME = 'proxies_filter.csv'
    FILE_PATH = os.path.join(os.path.dirname(__file__), CSV_FILE_NAME)
    FILTER_FILE_PATH = os.path.join(os.path.dirname(__file__), FILTER_CSV_FILE_NAME)

    def __init__(self):
        super().__init__()
        self.__lock = threading.Lock()
        self.__semaphore = threading.BoundedSemaphore(10)
        self.__file_append_object = open(
            self.FILE_PATH,
            'a+',
            newline="",
            encoding='utf-8-sig'
        )
        self.__file_read_object = open(
            self.FILE_PATH,
            'r',
            encoding='utf-8-sig'
        )

        self.__dw_append = csv.DictWriter(
            self.__file_append_object,
            fieldnames=['ip', 'port']
        )
        self.__dr = csv.reader(self.__file_read_object)
        self.__init()

    def __init(self):
        # 读取标题
        header_title = next(self.__dr, None)
        # 如果表头不存在，则写入表头
        if header_title != ['ip', 'port']:
            self.__dw_append.writeheader()

    def save_item(self):
        """
        保存代理
        :return:
        """

        def save():
            while True:
                if len(self.proxies) >= 10:
                    m_logger.info("正在保存代理")
                    self.__lock.acquire()
                    self.__dw_append.writerows(self.proxies)
                    self.__file_append_object.flush()
                    self.proxies = []
                    self.__lock.release()

                time.sleep(1)

        threading.Thread(target=save, daemon=True).start()

    def generate(self):
        """
        生成并持久化代理
        :return:
        """
        # 开始爬取代理
        self.spider(self.save_item)

    @classmethod
    def get_random_proxy_by_local(cls):
        """
        随机获取一个代理
        :return:
        """
        with open(cls.FILTER_FILE_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)
            proxies = list(reader)

        proxy = random.choice(proxies)

        return {
            "http://": f"{proxy[0]}:{proxy[1]}",
            "https://": f"{proxy[0]}:{proxy[1]}"
        }

    def get_random_proxy_by_filter(self):
        """
        随机获取一个代理
        :return:
        """
        proxies = random.choice(self.proxies)
        return {
            "http": f"http://{proxies[0]}:{proxies[1]}",
            "https": f"http://{proxies[0]}:{proxies[1]}"
        }
        pass

    def check_filter_proxy(self):
        pass

    def filter_proxy(self, path=None):
        """
        过滤代理
        :return:
        """
        if path is None:
            proxies = list(self.__dr)
        else:
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)
                proxies = list(reader)

        # 用于存储可用代理
        temp_proxies = []

        # 定义过滤代理的功能函数
        def __filter(proxy):
            """
            过滤代理
            :param proxy:  代理
            :return:
            """
            # 判断代理是否可用
            if check_proxy(proxy[0], proxy[1]):
                # 如果可用，将代理添加到列表中
                temp_proxies.append({
                    "ip": proxy[0],
                    "port": proxy[1]
                })

        # 将所有代理提交给线程池
        futures = [self._executor.submit(__filter, proxy) for proxy in proxies]

        # 等待所有线程执行完毕
        concurrent.futures.wait(futures)

        def save():
            self.proxies = temp_proxies
            with open(self.FILTER_FILE_PATH, 'w', encoding='utf-8-sig', newline="") as f:
                writer = csv.DictWriter(f, fieldnames=['ip', 'port'])
                writer.writeheader()
                writer.writerows(temp_proxies)

        # 写入表头

        # 将可用代理写入文件
        save()

        # if len(temp_proxies) < 20:
        #     self.generate()

    def filter_proxy_by_local(self, num: int = 1):
        """
        从本地文件中过滤代理

        速度有限制

        :param num: 需要获取的代理数量
        :return:
        """
        with open(self.FILE_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)
            proxies = list(reader)

        proxy_queue = Queue()

        max_workers = num

        if num >= 5:
            max_workers = 5

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        is_run = True

        def append_item(proxy):
            nonlocal proxy_queue

            if is_run and check_proxy(proxy[0], proxy[1]):
                return proxy

        future_list = [executor.submit(append_item, proxy) for proxy in proxies]

        for future in future_list:
            proxy = future.result()
            if proxy:
                proxy_queue.put({
                    "http": "http://" + proxy[0] + ":" + proxy[1],
                    "https": "http://" + proxy[0] + ":" + proxy[1]
                })
                m_logger.info(f"可用代理为：{proxy}, 当前可用代理数量为：{proxy_queue.qsize()}，需要的代理数量为：{num}")
                if proxy_queue.qsize() == num:
                    is_run = False
                    break

        # 将所有线程关闭
        executor.shutdown(wait=False, cancel_futures=True)

        if proxy_queue.qsize() < num:
            m_logger.info("可用代理不足")
            return proxy_queue
        return proxy_queue

    def filter_proxy_by_parse(self):
        pass

    # 去重
    def deduplication(self):
        """
        去重
        :return:
        """
        # 读取文件内容
        with open(self.FILE_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)
            proxies = list(set(map(tuple, list(reader))))
        # 写入文件
        with open(self.FILE_PATH, 'w', newline="", encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['ip', 'port'])
            writer.writerows(proxies)


if __name__ == '__main__':
    generate = GenerateProxy()
    # generate.generate()
    # usable_list = generate.filter_proxy_by_local(6)
    # pprint.pprint(usable_list.qsize())
    generate.filter_proxy(GenerateProxy.FILTER_FILE_PATH)
    generate.deduplication()
