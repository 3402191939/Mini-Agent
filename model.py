import json
import os

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def ask_model(prompt: str) -> dict:
    """Call AI model and return a validated action."""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY is not configured")
    print("\nRequesting model for action...")

    with OpenAI(
        api_key = api_key,
        base_url = "https://api.deepseek.com",
    ) as client:
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Follow the supplied instructions and task history."
                        "Return exactly one JSON object."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_format={"type": "json_object"},
            extra_body={"thinking": {"type": "disabled"}},
            max_tokens=2048,
        )

    if not response.choices:
        raise RuntimeError("The model returned no choices")

    choice = response.choices[0]
    if choice.finish_reason != "stop":
        raise RuntimeError(
            f"The model output did not complete answer successfully: {choice.finish_reason}"
        )
    
    raw = choice.message.content
    print("\nRaw model response:")
    print(repr(raw))
    if not raw or not raw.strip():
        raise RuntimeError("The model returned empty content")

    action = json.loads(raw)
    if not isinstance(action, dict):
        raise ValueError("The model output must be a JSON object")

    action_type = action.get("type")
    if action_type == "final":
        content = action.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("The final answer must include a non-empty content string.")
    elif action_type != "tool_call":
        raise ValueError("The type must be either 'tool_call' or 'final'")
 
    print("\nModel action:")
    print(json.dumps(action, ensure_ascii=False, indent=2))

    if response.usage:
        print(
            f"\nTokens: input={response.usage.prompt_tokens}, "
            f"output={response.usage.completion_tokens}"
        )  
    return action