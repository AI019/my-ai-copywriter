import requests

API_KEY = "sk-gvzojjeykwdbiutvxartsqanvauatejktmprxgczeidfcyes"  # 你的密钥

url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("🤖 AI 聊天助手已启动（输入 'quit' 或 'exit' 退出）")
print("-" * 40)

while True:
    # 获取用户输入
    user_input = input("\n🙋 你: ")
    
    # 退出条件
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("👋 再见！")
        break
    
    # 调用 AI
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 500
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]
        print(f"🤖 AI: {ai_reply}")
    else:
        print(f"❌ 错误: {response.status_code} - {response.text}")