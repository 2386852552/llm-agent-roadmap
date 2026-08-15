"""
logger.py
---------
负责整个项目的日志配置。

其他模块只需要调用 get_logger()
就可以获得统一格式的 logger。
"""

import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    创建并返回一个配置好的 Logger。

    参数：
        name:
            当前模块的名称。
            通常直接传入 __name__。

    返回：
        配置完成的 logging.Logger 对象。
    """

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger