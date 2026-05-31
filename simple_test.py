import requests

API_KEY = "sk-or-v1-4b694f2dae5394923b81eb6810284b4ff31de7e412ffff9085a5ccdaed99c4e67"

print("Key 前10位:", API_KEY[:10])
print("Key 后10位:", API_KEY[-10:])
print("Key 长度:", len(API_KEY))

response = requests.post(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

print("状态码:", response.status_code)
print("返回内容:", response.text)