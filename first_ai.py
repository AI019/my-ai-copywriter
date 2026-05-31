import requests

# 请确保这里是你的完整 API Key
API_KEY = "sk-or-v1-4b694f2dae5394923b81eb6810284b4ff31de7e412fff9085a5ccdaed99c4e67s"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": "你好，请做一下自我介绍"}],
        # 注意！这里是 allow_fallback，没有 's'！
        "allow_fallback": False,
        "provider": {"only": "free"}
    }
)

# 这行代码可以帮助我们调试，看看API到底返回了什么
print("API Status Code:", response.status_code)
print("API Response:", response.text)

# 如果请求成功（状态码200），再尝试解析
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print("请求失败，请检查上面的错误信息。")