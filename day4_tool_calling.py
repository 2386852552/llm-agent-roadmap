import os
import json
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

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

def get_current_time():
    """获取当前时间。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculator(a, b):
    """计算两个数字的和。"""
    return a + b


def multiply(a, b):
    """计算两个数字的乘积。"""
    return a * b

tool_registry = {
    "get_current_time": get_current_time,
    "calculator": calculator,
    "multiply": multiply,
}

tool_schemas = {
    "get_current_time": {
        "name": "get_current_time",
        "description": "获取当前日期和时间，不需要任何参数。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },

    "calculator": {
        "name": "calculator",
        "description": "计算两个数字的和。",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字",
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字",
                },
            },
            "required": ["a", "b"],
        },
    },

    "multiply": {
        "name": "multiply",
        "description": "计算两个数字的乘积。",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字",
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字",
                },
            },
            "required": ["a", "b"],
        },
    },
}

def build_tool_definitions():
    definitions = []

    for schema in tool_schemas.values():
        definitions.append({
            "type": "function",
            "function": schema,
        })

    return definitions


tool_definitions = build_tool_definitions()

def execute_tool(tool_name, arguments):
    tool = tool_registry.get(tool_name)

    if tool is None:
        return f"未知工具：{tool_name}"

    try:
        return tool(**arguments)

    except Exception as e:
        return f"工具执行失败：{e}"

def run_agent(user_input):

    messages = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    while True:

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