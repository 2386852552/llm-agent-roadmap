"""
utils.py
---------
放一些和具体业务无关的通用工具函数。
"""

from pathlib import Path

def read_text_file(file_path: Path) -> str:
    """
    读取 UTF-8 文本文件。

    如果文件不存在，Path.read_text() 
    会抛出 FileNotFoundError。
    这里不隐藏这个错误，让上层代码处理。
    """

    return file_path.read_text(encoding="utf-8")

def write_text_file(file_path: Path, content: str) -> None:
    """
    把文本内容写进指定文件。

    如果父目录不存在，会自动创建。
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        content, 
        encoding="utf-8",
        )