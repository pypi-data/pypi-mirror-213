import sys
from loguru import logger


class MLog:
    def __init__(self, username="MoMingLog", level="DEBUG"):
        self.logger = logger
        self.username = username
        self.level = level

    def get_logger(self):
        logger.remove()  # 清除默认的日志处理器
        # 添加自定义的日志处理器
        logger.add(
            # f"{self.username}.log",
            sys.stdout,
            level=self.level,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <level>{level}</level> - {extra[username]}-<level>{message}</level>"
        )

        return logger.bind(username=f"【{self.username}】")


m_logger = MLog(level="DEBUG").get_logger()

if __name__ == '__main__':
    m_logger.debug("debug")
    m_logger.info("info")
    m_logger.warning("warning")
    m_logger.error("error")
    m_logger.critical("critical")
    m_logger.exception("exception")
