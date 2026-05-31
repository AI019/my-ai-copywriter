import requests

API_KEY = "sk-or-v1-53b76fced05c4ec087eec0e3c612f6af0dbf4344bc0dd6c3b01c493f86771134e"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": "你好，请说'我成功了'"}],
        "allow_fallback": False,
        "provider": {"only": "free"}
    }
)

print("状态码:", response.status_code)
if response.status_code == 200:
    result = response.json()
    print("AI回答:", result["choices"][0]["message"]["content"])
else:
    print("错误信息:", response.text)