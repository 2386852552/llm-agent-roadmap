from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL_ID"),
    messages=[
        {"role": "system", "content": "你是一个友好、专业的智能助手。"},
        {"role": "user", "content": "请用一句话介绍什么是大模型。"}
    ]
)

print(response.choices[0].message.content)