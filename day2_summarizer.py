from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

input_path = Path("data/notes.txt")

text = input_path.read_text(encoding="utf-8")

print("AI正在分析文件...\\n")

prompt = f"""
请对下面内容进行学习型总结。

要求：

1.用3个要点总结
2.提取关键词
3.生成三个复习问题

内容：

{text}
"""

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL_ID"),
    messages=[
        {
            "role":"system",
            "content":"你是一个擅长学习总结的AI助手。"
        },
        {
            "role":"user",
            "content":prompt
        }
    ]
)

result = response.choices[0].message.content

print(result)

output_path = Path("output/notes_summary.md")

output_path.write_text(result, encoding="utf-8")

print(f"总结已保存到 {output_path}")
