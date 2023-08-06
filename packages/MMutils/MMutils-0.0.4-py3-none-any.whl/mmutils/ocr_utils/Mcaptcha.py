# @Time : 10/30/2021 1:32 PM
# @Author : MoMingLog
# @File : Mcaptcha.py
# @Software: PyCharm

import ddddocr  # 带带弟弟


def ocr_captcha(img_data):
    """ 识别验证码

    创建时间：2021.10.30 13:32

    :param img_data:
    :return:
    """
    ocr = ddddocr.DdddOcr()
    result = ocr.classification(img_data)
    return result
