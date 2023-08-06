# @Time : 10/30/2021 2:22 PM
# @Author : MoMingLog
# @File : Mproxy.py
# @Software: PyCharm


import random
import time
import concurrent.futures
import threading
from queue import Queue

from lxml import etree
from mmutils.ocr_utils.Mcaptcha import ocr_captcha
from mmutils.proxy_utils import *
from mmutils.spider_utils.Mrequests import request_, random_headers_with_ua
from mmutils.log_utils.Mlog import m_logger


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
            headers = random_headers_with_ua()
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
            # Thread(target=check_usable_func, args=(item, __save_item)).start()
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
                    'ip': ip.strip() if ip_domain is None else ocr_captcha(
                        request_(url=domain + ip, ret_format='content')),
                    # 判断port_domain是否为空，如果不为空，则识别图片
                    'port': port.strip() if port_domain is None else ocr_captcha(
                        request_(url=domain + port, ret_format='content'))
                }
                threading.Thread(target=run, args=(item,)).start()

        else:
            ip_port_ = element.xpath(ip_port_xpath)
            for ip_port in ip_port_:
                ip_port_list = ip_port.split(':')
                item = {
                    # 使用三元运算，判断domain参数是否为空，如果不为空，则表示该网站使用了反爬，需要我们识别出ip或port
                    'ip': ip_port_list[0].strip() if ip_domain is None else ocr_captcha(
                        request_(domain + ip_port_list[0], ret_format='content')),
                    'port': ip_port_list[1].strip() if port_domain is None else ocr_captcha(
                        request_(domain + ip_port_list[1], ret_format='content'))
                }
                threading.Thread(target=run, args=(item,)).start()

    def _spider(self, func):
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


class Proxy(SpiderProxy):
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

    def __save_item(self):
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

    def spider_free_proxy(self, is_deduplication=False):
        """
        生成并持久化代理
        :param is_deduplication: 是否去重, 默认不去重
        :return:
        """
        # 开始爬取代理
        self._spider(self.__save_item)
        # 判断是否去重
        if is_deduplication:
            self.deduplication()

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
        if self.proxies == []:
            self.__dr = csv.reader(self.__file_read_object)
            next(self.__dr)
            self.proxies = list(self.__dr)

        proxy = random.choice(self.proxies)

        return {
            "http://": f"{proxy[0]}:{proxy[1]}",
            "https://": f"{proxy[0]}:{proxy[1]}"
        }

    def filter_proxy(self, in_path=None, out_path=FILTER_FILE_PATH):
        """
        过滤代理
        :param in_path:  输入csv文件的路径
        :param out_path: 输出csv文件的路径
        :return:
        """
        if in_path is None:
            proxies = list(self.__dr)
        else:
            with open(in_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)
                proxies = list(reader)

        if proxies == []:
            m_logger.warning("您的代理文件内容为空")
            return

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
            with open(out_path, 'w', encoding='utf-8-sig', newline="") as f:
                writer = csv.DictWriter(f, fieldnames=['ip', 'port'])
                writer.writeheader()
                writer.writerows(temp_proxies)

        # 将可用代理写入文件
        save()

        # if len(temp_proxies) < 20:
        #     self.generate()

    def filter_proxy_by_local(self, num: int = 1):
        """
        从本地文件中过滤代理

        效率相对于filter_proxy()低

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
                    "http://": f"{proxy[0]}:{proxy[1]}",
                    "https://": f"{proxy[0]}:{proxy[1]}"
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
    proxy = Proxy()
    proxy.filter_proxy()
