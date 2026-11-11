import json

from tools import list_files, read_file, search_code

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "search_code": search_code,
}

def execute_tool(request: dict) -> dict:
    """
    Execute a tool request and return either the successful 
    result or an error message.
    """
    if not isinstance(request, dict):
        return {"ok": False, "error": "tool request must be a dictionary."}

    name = request.get("name")
    arguments = request.get("arguments", {})

    if not isinstance(name, str) or name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {name}"}

    if not isinstance(arguments, dict):
        return {"ok": False, "error": "arguments must be a dictionary."}

    if not all(isinstance(key, str) for key in arguments):
        return {"ok": False, "error": "Parameter names must be strings."}

    tool = TOOLS[name]

    try:
        result = tool(**arguments)
        return {"ok": True, "data": result}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}:{exc}",}

if __name__ == "__main__":
    request_json = input("please enter tool request JSON：\n")
    try:
        request = json.loads(request_json)
    except json.JSONDecodeError as exc:
        print(f"JSON format error: {exc}")
    else:
        result = execute_tool(request)
        print(json.dumps(result, ensure_ascii=False, indent=2))