import csv
import os
import re

from mmutils.log_utils.Mlog import m_logger
from mmutils.spider_utils.Mrequests import random_headers_with_ua, request_


def check_usable(item, save_item=None):
    """ 检测代理是否可用

    创建时间：2021.10.30 14:30

    :param item: 代理
    :param save_item: 可用代理的持久化存储函数
    :return:
    """
    if save_item is None:
        raise ValueError('请传入对可用代理数据进行持久化存储的函数！')
    else:
        # 下方通过在百度搜索“ip”的结果来测试代理是否可用
        url = 'https://www.baidu.com/s?wd=%E6%9C%AC%E6%9C%BAip'
        headers = random_headers_with_ua(ua_type='chrome')
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


def check_proxy(ip, port) -> bool:
    url = 'http://www.baidu.com/s?ie=UTF-8&wd=本机ip'
    headers = random_headers_with_ua()
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
                m_logger.success(f"代理：{ip}:{port}，请求成功")
                return True
            else:
                m_logger.error(f"代理：{ip}:{port}，请求失败")
                return False
        else:
            m_logger.error("请求失败")
            return False
    except Exception as te:
        m_logger.error(f"代理：{ip}:{port}，请求失败, 异常")
        return False


def get_available_proxy(
        num: int = 1,
        file_data=None,
        file_path: str = None,
        is_recheck: bool = False,
) -> list:
    """获取可用代理

    创建时间：2023.6.8

    :param file_data: 代理文件数据，如果传入该参数，则不需要传入file_path
    :param file_path: 代理文件路径，如果传入该参数，则不需要传入file_data
    :param num: 需要获取的代理数量
    :param is_recheck: 是否需要重新检查代理，则会在获取代理的时候顺便检查代理是否可用
    :return:
    """
    if file_data is None:
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), '2proxies.csv')
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
                ret_data.append({
                    "http://": f"{ip}:{port}",
                    "https://": f"{ip}:{port}"
                })
                if len(ret_data) == num:
                    break
        else:
            ret_data.append(proxy)
            if len(ret_data) == num:
                break

    return ret_data
