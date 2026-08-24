import os
import json

from dataclasses import dataclass, field
from typing import Any

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

@dataclass
class AgentState:

    messages: list[dict[str, Any]] = field(default_factory=list)
    iteration: int = 0
    finished: bool = False
    final_answer: str | None = None
def print_state(state: AgentState):
    print("\n[Agent State]")
    for index, message in enumerate(state.messages):
        role = message.get("role")
        print(f"  [{index}] role={role}")
        if role == "user":
            print(
                f"  content={message.get('content')}"
            )
        elif role == "assistant":
            content = message.get("content")
            if content:
                print(
                    f"  content={content}"
                )
            tool_calls = message.get("tool_calls")
            if tool_calls:
                for tool_call in tool_calls:
                    function = tool_call.get(
                        "function", {}
                    )
                    print(
                        f"  tool_call="
                        f"{function.get('name')}"
                    )
                    print(
                        f"  arguments="
                        f"{function.get('arguments')}"
                    )
        elif role == "tool":
            print(
                f"  tool_call_id="
                f"{message.get('tool_call_id')}"
            )
            print(
                f"  content="
                f"{message.get('content')}"
            )
def llm_step(state: AgentState):
    response = client.chat.completions.create(
        model = MODEL,
        messages = state.messages,
        tools = tool_definitions,
    )
    message = response.choices[0].message
    return message
def tool_step(state: AgentState,assistant_message,):
    assistant_message_dict = assistant_message.model_dump(
        exclude_none=True
    )
    state.messages.append(assistant_message_dict)
    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(
            tool_call.function.arguments
        )
        print(f"\n[Tool Call]")
        print(f"Name: {tool_name}")
        print(f"Arguments: {arguments}")
        result = execute_tool(
            tool_name,
            arguments,
        )
        print("\n[Tool Result]")
        print(result)
        state.messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )
def run_agent(user_input: str, max_iterations: int = 5,):
    state = AgentState(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ]
    )
    while state.iteration < max_iterations:
        state.iteration += 1
        print("\n" + "="*60)
        print(
            f"Iteration {state.iteration}"
        )
        print("="*60)
        print_state(state)
        assistant_message = llm_step(state)
        if not assistant_message.tool_calls:
            state.finished = True
            state.final_answer = (
                assistant_message.content
            )
            print("\n[Final Answer]")
            print(state.final_answer)
            return state
        tool_step(state,assistant_message,)
    raise RuntimeError(
        f"Agent 达到最大迭代次数"
        f"{max_iterations}, 停止执行。"
    )
def main():
    print("="*60)
    print("输入quit退出")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {
            "quit",
            "exit",
        }:
            print("谢谢使用")
            break
        if not user_input:
            continue
        try:
            state = run_agent(user_input)
            print(
                f"\nAgent: "
                f"{state.final_answer}"
            )
        except Exception as e:
            print(
                f"\n发生错误: {e}"
            )
if __name__ == "__main__":
    main()
