import requests
from datetime import datetime

API_KEY = "sk-gvzojjeykwdbiutvxartsqanvauatejktmprxgczeidfcyes"  # 你的正确密钥

url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 日志文件直接保存到 Projects 文件夹
log_filename = f"/Volumes/AI_Work/Projects/chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def save_to_log(content):
    with open(log_filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")

save_to_log(f"聊天开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
save_to_log("=" * 50)

print("🤖 AI 聊天助手已启动（输入 'quit' 或 'exit' 退出）")
print(f"📁 聊天记录将保存到: {log_filename}")
print("-" * 40)

while True:
    user_input = input("\n🙋 你: ")
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        save_to_log(f"\n聊天结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("👋 再见！")
        break
    
    save_to_log(f"\n🙋 你: {user_input}")
    
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
        save_to_log(f"🤖 AI: {ai_reply}")
    else:
        error_msg = f"❌ 错误: {response.status_code} - {response.text}"
        print(error_msg)
        save_to_log(error_msg)