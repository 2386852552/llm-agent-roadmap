"""
仅仅定义工具本身，不包含任何业务逻辑。
"""

from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(a,b):
    return a+b

def multiply(a,b):
    return a*b

def string_length(text):
    return len(text)