"""
day3_demo.py
------------
Day 3 的入口程序。

它负责把：
配置
+
LLM
+
文件工具
+
总结业务

组合起来。
"""

from pathlib import Path

from app.llm import LLMClient
from app.summarizer import summarize_text
from app.utils import read_text_file, write_text_file

def main() -> None:
    """
    程序入口。
    """

    input_file = Path("data/notes.txt")
    output_file = Path("output/day3_summary.md")

    try:
        llm = LLMClient()
        text = read_text_file(input_file)
        print("正在调用 Qwen， 请稍候...")
        summary = summarize_text(text, llm)
        write_text_file(output_file, summary)
        print(f"总结完成，结果已保存到：{output_file}")
    except FileNotFoundError:
        print(f"找不到输入文件：{input_file}")
    except Exception as e:
        print(f"程序运行失败：{e}")

if __name__ == "__main__":
    main()