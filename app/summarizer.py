"""
summarizer.py
---------
负责”总结文本“这一具体业务逻辑。

它不关心：
- API Key 从哪里来
- 文件怎么保存
- OpenAI Client 怎么创建

这些事情分别由其他模块负责。
"""

from app.llm import LLMClient

def build_summary_prompt(text: str) -> str:
    """
    根据输入文本构造总结 Prompt。
    """

    return f"""
    你是一个专业的学习助手。

    请分析下面的学习笔记，并输出：

    1.简介摘要
    2.5 个关键词
    3.3 个适合复习的问题

    请使用 Markdown 格式输出。

    学习笔记：
    {text}
    """.strip()

def summarize_text(text: str, llm_client: LLMClient) -> str:
    """
    调用 LLM 对文本进行总结。
    """

    prompt = build_summary_prompt(text)
    return llm_client.generate(prompt)
