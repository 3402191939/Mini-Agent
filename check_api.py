import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.environ.get('DEEPSEEK_API_KEY'),
    base_url = "https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role": "system", 
            "content": (
                "Just output a JSON object."
                'example: {"type": "final", "content": "linked successfully"}'
            )
        },
        {
            "role": "user", 
            "content": "Please return JSON object when linked successfully."
        },
    ],
    response_format={"type": "json_object"},
    extra_body={"thinking": {"type": "disabled"}},
    max_tokens=256,
)

choice = response.choices[0]

if choice.finish_reason != "stop":
    raise RuntimeError(
        f"The model did not complete answer successfully: {choice.finish_reason}"
    )

raw = choice.message.content

if not raw or not raw.strip():
    raise RuntimeError("The model returned empty content")

action = json.loads(raw)

if not isinstance(action, dict):
    raise ValueError("The model output must be a JSON object")

print("The model return:")
print(json.dumps(action, ensure_ascii=False, indent=2))
