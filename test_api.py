import requests

API_KEY = "sk-or-v1-4b694f2dae5394923b81eb6810284b4ff31de7e412ffff9085a5ccdaed99c4e67"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": "你好，请做一下自我介绍"}],
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
