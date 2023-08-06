import sys
from typing import Any

from loguru import logger


class MLog:

    def __init__(self, username="MoMingLog", level="DEBUG", log_path=None):
        self.logger = None
        self.username = username
        self.level = level
        if log_path is None:
            log_path = f"logs/{self.username}.log"
        self.log_path = log_path

    def get_logger(self):
        logger.remove()  # 清除默认的日志处理器
        # 添加输出到控制台的日志处理器
        logger.add(
            sys.stdout,
            level=self.level,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{level}</level> {extra[username]} | <level>{message}</level>"
        )
        # 添加输出到文件的日志处理器
        logger.add(
            self.log_path,
            level=self.level,
            # 指定日志的旋转方式，可以是时间、大小等条件
            rotation="1 week",
            encoding="utf-8",
            # 指定处理器是否使用队列进行异步处理
            enqueue=True,
            # 指定了旋转后的日志文件的保留时间
            retention="10 days",
            # 指定了旋转后的日志文件是否进行压缩
            compression="zip",
            # 消息格式化模板
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{level}</level> {extra[username]} | <level>{message}</level>"
        )
        self.logger = logger.bind(username=f"<{self.username}>")
        return self

    def set_username(self, label_name):
        self.username = label_name
        self.logger = logger.bind(username=f"<{self.username}>")
        return self

    def set_level(self, level):
        self.level = level
        self.get_logger()

    def info(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.info(__message, *args, **kwargs)

    def debug(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.debug(__message, *args, **kwargs)

    def warning(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.warning(__message, *args, **kwargs)

    def error(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.error(__message, *args, **kwargs)

    def success(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.success(__message, *args, **kwargs)

    def exception(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.exception(__message, *args, **kwargs)

    def critical(self, __message: str, *args: Any, **kwargs: Any):
        self.logger.critical(__message, *args, **kwargs)


m_logger = MLog(level="DEBUG").get_logger()

if __name__ == '__main__':
    m_logger.set_level("DEBUG")
    m_logger.debug("debug", username="测试")
    m_logger.info("info", username="test")
    m_logger.warning("warning", username="test")
