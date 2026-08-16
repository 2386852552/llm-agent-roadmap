from tools import calculator, multiply, get_current_time, string_length

tools_registry = {
    "calculator": calculator,
    "multiply": multiply,
    "get_current_time": get_current_time,
    "string_length": string_length,
}

def execute_tool(tool_name, arguments):
    tool = tools_registry.get(tool_name)

    if tool is None:
        return f"工具 {tool_name} 不存在"

    return tool(**arguments)

print(execute_tool("calculator", {"a": 10, "b": 20}))
print(execute_tool("multiply", {"a": 6, "b": 7}))
print(execute_tool("get_current_time", {}))
print(execute_tool("unknown", {}))
print(execute_tool("string_length", {"text": "hello"}))