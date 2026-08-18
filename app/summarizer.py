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
import json
from app.llm import LLMClient
from app.models import SummaryResult
from pydantic import ValidationError

def build_summary_prompt(text: str) -> str:
    """
    根据输入文本构造总结 Prompt。
    """

    return f"""
你是一个专业的学习助手。

请分析下面的学习笔记。

你必须严格返回 JSON，
不要返回 Markdown，
不要添加 JSON 之外的文字。

JSON 格式必须是：

{{
    "title": "总结标题",
    "summary": "内容摘要",
    "keywords": ["关键词1", "关键词2", "关键词3"],
    "questions": ["复习问题1", "复习问题2", "复习问题3"]
}}

字段要求：

- title: 字符串
- summary: 字符串
- keywords: 字符串列表
- questions: 字符串列表

学习笔记：

{text}
""".strip()

def parse_summary_result(raw_text: str) -> SummaryResult:
    """
    解析 LLM 返回的 JSON 字符串为 SummaryResult。
    """

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValidationError("模型返回内容不是合法 JSON") from e

    try:
        return SummaryResult.model_validate(data)
    except ValidationError as e:
        raise ValidationError("模型返回内容格式错误") from e




def summarize_text(text: str, llm_client: LLMClient) -> SummaryResult:
    """
    调用 LLM 对文本进行总结。
    """

    prompt = build_summary_prompt(text)
    raw_text = llm_client.generate(prompt)
    return parse_summary_result(raw_text)
