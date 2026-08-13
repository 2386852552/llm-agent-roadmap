from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

messages = [
    {
        "role":"system",
        "content":"你是一个耐心、简洁的AI老师。"
    }
]

print("===Day1 多轮聊天机器人 ===")
print("输入quit退出\\n")

while True:
    user_input = input("你：")

    if user_input.lower() == "quit":
        print("谢谢使用！")
        break

    messages.append({
        "role":"user",
        "content":user_input
    })

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL_ID"),
        messages=messages
    )

    assistant_reply = response.choices[0].message.content

    print(f"AI: {assistant_reply}\\n")

    messages.append({
        "role":"assistant",
        "content":assistant_reply
    })

    print(f"[当前历史消息数：{len(messages)}]\\n")


