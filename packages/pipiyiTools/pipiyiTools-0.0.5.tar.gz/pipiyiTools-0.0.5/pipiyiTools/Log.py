import logging
import colorlog


class Log:
    # 设置日志格式
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )

    def __init__(self, filename="log"):
        # 它会自动获取当前模块的名称作为 logger 的名称。
        # 这样可以在日志中标识出日志消息来自哪个模块
        self.logger = logging.getLogger(__name__)
        # 设置 logger 对象的日志级别为 DEBUG
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            # 创建日志处理器对象 用于打印台输出
            console_handle = self._create_handler(logging.StreamHandler(), logging.INFO)

            # 创建一个写入文件的处理器对象 用于日志记录
            file_handler = self._create_handler(
                logging.FileHandler(f"{filename}.log"), logging.WARNING
            )

            self.logger.addHandler(console_handle)
            self.logger.addHandler(file_handler)

    @staticmethod
    def _create_handler(handler, level):
        handler.setLevel(level)
        handler.setFormatter(Log.formatter)
        return handler

    def info(self, message, *args):
        self.logger.info(message, *args)

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def warning(self, message, *args):
        self.logger.warning(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
