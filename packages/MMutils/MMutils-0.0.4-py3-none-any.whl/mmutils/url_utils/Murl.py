import re
from mmutils.file_utils.Mfile import replace_invalid_filename_char


def get_filename(url, with_ext=True):
    """ 从链接中截取文件名，包括后缀（扩展名）

    :param url: 链接
    :param with_ext: 是否包含后缀（扩展名）
    :return: 返回截取的文件名，包括后缀（扩展名）
    """
    filename = replace_invalid_filename_char(re.search('.*/(.*)', url).group(1))
    if with_ext:
        return filename
    else:
        # 判断是否包含后缀（扩展名）
        if filename.find('.') == -1:
            # 如果不包含后缀（扩展名），则返回filename
            return filename
        else:
            # 如果包含后缀（扩展名），则返回截取后的文件名
            return filename[0: filename.rfind('.')]

