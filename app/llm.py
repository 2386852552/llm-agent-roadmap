"""
llm.py
---------
专门负责和大语言模型进行通信。

其他模块不需要知道 OpenAI SDK
到底怎么创建 client、 怎么发送请求。

他们只需要调用 LLMCLient。generate() 即可。
"""

from openai import OpenAI

from app.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL_ID,
    validate_config,
)

class LLMClient:
    """
    LLM 客户端。

    这个类负责：
    1.创建 OpenAI 兼容客户端
    2.调用模型
    3.返回模型生成文本
    """

    def __init__(self) -> None:
        """
        初始化LLM客户端。
        """

        validate_config()

        self.client = OpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
        )

        self.model = LLM_MODEL_ID
    def generate(self, prompt: str) -> str:
        """
        向模型发送一个 Prompt，并返回文本结果。

        参数：
            prompt: 给模型的提示词

        返回：
            模型生成的字符串
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""


