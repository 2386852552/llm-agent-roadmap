"""
day3_demo.py
------------
Day 3 的入口程序。
"""

from pathlib import Path
import textwrap
from app.llm import LLMClient
from app.logger import get_logger
from app.summarizer import summarize_text
from app.utils import read_text_file, write_text_file


# 创建当前模块对应的 logger。
logger = get_logger(__name__)


def main() -> None:
    """
    程序入口。
    """

    input_file = Path("data/notes.txt")
    output_file = Path("output/day3_summary.md")

    logger.info("程序开始运行")

    try:
        logger.info("正在创建 LLM 客户端")
        llm = LLMClient()

        logger.info(f"正在读取文件：{input_file}")
        text = read_text_file(input_file)

        logger.info("正在调用 Qwen")
        print("正在调用 Qwen，请稍候...")

        result = summarize_text(text, llm)

        logger.info("Qwen 返回成功")

        questions = "\n".join(
            f"- {question}"
            for question in result.questions
        )

        markdown = f"""# {result.title}

        ## 摘要

        {result.summary}

        ## 关键词

        {", ".join(result.keywords)}

        ## 复习问题

        {questions}
        """
        write_text_file(output_file, markdown)

        logger.info(f"结果已保存：{output_file}")
        print(f"总结完成，结果已保存到：{output_file}")

    except FileNotFoundError:
        logger.error(f"找不到输入文件：{input_file}")
        print(f"找不到输入文件：{input_file}")

    except Exception:
        # logger.exception() 会自动记录：
        # 1. 错误信息
        # 2. 完整 traceback
        logger.exception("程序运行过程中发生未预期异常")

        print("程序运行失败，请查看 logs/app.log")


if __name__ == "__main__":
    main()