from tools import (
    calculator,
    multiply,
    get_current_time,
    string_length,
)

tool_registry = {
    "calculator": calculator,
    "multiply": multiply,
    "get_current_time": get_current_time,
    "string_length": string_length,
}

tool_schemas = {
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

    "get_current_time": {
        "name": "get_current_time",
        "description": "获取当前日期和时间，不需要任何参数。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },

    "string_length": {
        "name": "string_length",
        "description": "计算字符串的长度。",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "需要计算长度的字符串",
                },
            },
            "required": ["text"],
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

def execute_tool(tool_name, arguments):
    tool = tool_registry.get(tool_name)#获取tool_name对应的函数（字典的值）赋值给tool，tool即成为可以执行功能的函数工具。

    if tool is None:
        return f"未知工具：{tool_name}"

    try:
        return tool(**arguments)

    except Exception as e:
        return f"工具执行失败：{e}"
