import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from registry import execute_tool
from registry import build_tool_definitions

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL_ID")

if not API_KEY:
    raise ValueError("没有找到 LLM_API_KEY，请检查 .env 文件。")

if not BASE_URL:
    raise ValueError("没有找到 LLM_BASE_URL，请检查 .env 文件。")

if not MODEL:
    raise ValueError("没有找到 LLM_MODEL_ID，请检查 .env 文件。")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

tool_definitions = build_tool_definitions()

def run_agent(user_input,max_iterations=5):
    messages = [
        {
            "role": "user",
            "content": user_input,
        }
    ]
    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration+1}")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool_definitions,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(f"\n[Tool Call] {tool_name}")
            print(f"[Arguments] {arguments}")

            result = execute_tool(
                tool_name,
                arguments,
            )

            print(f"[Tool Result] {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })
        raise RuntimeError("Agent 达到最大迭代次数，停止执行。")

def main():

    print("=" * 60)
    print("Day 4 - Tool Calling Agent")
    print(f"当前模型：{MODEL}")
    print("输入 quit 或 exit 退出")
    print("=" * 60)

    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Bye!")
            break

        if not user_input:
            continue

        try:
            answer = run_agent(user_input)

            print(f"\nAgent: {answer}")

        except Exception as e:
            print(f"\n发生错误：{e}")

if __name__ == "__main__":
    main()