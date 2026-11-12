import json

def ask_model(prompt: str) -> dict:
    """Send prompt and return effective action, currently sending by manual"""
    print("\nCopy the following text to model:\n")
    print(prompt)

    while True:
        raw = input(
            "\nPaste the single-line JSON action from the model"
            "(enter '/quit' to quit):\n"
        )
        if raw.strip() == "/quit":
            raise KeyboardInterrupt

        try:
            action = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"JSON parsing failed: {exc}, please try again.")
            continue

        if not isinstance(action, dict):
            print("The model's action must be a JSON object, please try again.")
            continue

        action_type = action.get("type")

        if action_type == "final":
            content = action.get("content")
            if not isinstance(content, str) or not content.strip():
                print("The final answer must include a non-empty content string.")
                continue
        elif action_type != "tool_call":
            print("The type must be either 'tool_call' or 'final', please try again.")
            continue
        return action