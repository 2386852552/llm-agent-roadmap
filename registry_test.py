def add(a,b):
    return a+b

def multiply(a,b):
    return a*b

tool_registry = {
    "add": add,
    "multiply": multiply,
}

print(tool_registry["add"](2,3))
print(tool_registry["multiply"](4,5))

tool_name = "add"

tool = tool_registry[tool_name]

result = tool(100, 200)

print(result)
