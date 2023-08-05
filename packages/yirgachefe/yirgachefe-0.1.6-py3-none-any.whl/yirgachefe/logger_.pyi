"""Logger interface"""
from typing import Optional


class Logger:
    def __init__(self, name=None):
        pass

    def update_logger(self,
                      log_level: int=None,
                      log_format=None,
                      log_path=None,
                      stream_out: Optional[bool]=None,
                      coloredlog: bool=False,
                      **optionals):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, exc_info=True, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass
