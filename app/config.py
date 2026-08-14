"""
config.py
---------
负责读取整个项目所需要的环境变量和配置

这样做的好处是：
其他模块不需要到处写 os.getenv(),
而是统一从 config 中获取配置。
"""

import os

from dotenv import load_dotenv

load_dotenv()

LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")

def validate_config() -> None:
    """
    检查必要配置是否存在。

    如果缺少配置就抛出异常，
    而不是让程序运行到很后面出现奇怪的错误。
    """
    if not LLM_MODEL_ID:
        raise ValueError("缺少环境变量：LLM_MODEL_ID")

    if not LLM_API_KEY:
        raise ValueError("缺少环境变量：LLM_API_KEY")

    if not LLM_BASE_URL:
        raise ValueError("缺少环境变量：LLM_BASE_URL")
