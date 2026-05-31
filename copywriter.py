import requests
from datetime import datetime

# 你的 API Key
API_KEY = "sk-gvzojjeykwdbiutvxartsqanvauatejktmprxgczeidfcyes"

url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 创建日志文件（带时间戳）
log_filename = f"/Volumes/AI_Work/Projects/copy_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def save_to_log(content):
    """保存内容到日志文件"""
    with open(log_filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def generate_copy(product_name, style):
    """根据风格生成产品文案"""
    
    # 不同风格的不同 Prompt
    prompts = {
        "1": f"""你是一个小红书种草博主，请为以下商品写一篇小红书风格的种草文案。

商品：{product_name}

要求：
1. 标题要吸引人，带emoji
2. 正文分3-4个卖点，每个卖点用emoji开头
3. 语气亲切自然，像朋友推荐
4. 结尾加上3-5个相关标签

请直接输出文案，不要有其他说明。""",

        "2": f"""请为商品「{product_name}」写一段微信朋友圈风格的推荐文案。

要求：
1. 简短有力，不超过150字
2. 语气亲切，像朋友在分享
3. 带2-3个emoji
4. 结尾加一句号召性的话

请直接输出文案。""",

        "3": f"""请为商品「{product_name}」写一篇专业评测风格的文案。

要求：
1. 标题客观专业
2. 分3-4个技术/功能卖点，每个卖点有具体说明
3. 语气中立可信
4. 结尾给出总结和购买建议

请直接输出文案。""",

        "4": f"""请为商品「{product_name}」写一段淘宝详情页风格的促销文案。

要求：
1. 突出卖点和优惠
2. 使用短句、符号分隔
3. 语气热情有感染力
4. 结尾加上行动呼吁（如“点击购买”）

请直接输出文案。"""
    }
    
    prompt = prompts.get(style, prompts["1"])
    
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"❌ 错误: {response.status_code}"

# 保存启动信息
save_to_log(f"文案生成器启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
save_to_log("=" * 50)

print("=" * 50)
print("🤖 AI 文案生成器（多风格版）")
print("=" * 50)
print(f"📁 文案将自动保存到: {log_filename}")
print("-" * 50)
print("\n📌 请选择文案风格：")
print("   1. 小红书种草风 🌟")
print("   2. 朋友圈分享风 💬")
print("   3. 专业评测风 📊")
print("   4. 淘宝促销风 🛒")
print("-" * 50)

while True:
    # 选择风格
    style = input("\n🎨 请选择风格（1/2/3/4，输入 q 退出）: ")
    
    if style.lower() == 'q':
        save_to_log(f"\n程序结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("👋 再见！")
        break
    
    if style not in ['1', '2', '3', '4']:
        print("⚠️ 请输入 1、2、3 或 4")
        continue
    
    # 输入商品名称
    product = input("📝 请输入商品名称: ")
    
    if not product.strip():
        print("⚠️ 商品名称不能为空")
        continue
    
    print("\n⏳ 正在生成文案，请稍候...\n")
    print("-" * 50)
    
    copy = generate_copy(product, style)
    print(copy)
    print("-" * 50)
    
    # 风格名称映射
    style_names = {"1": "小红书种草风", "2": "朋友圈分享风", "3": "专业评测风", "4": "淘宝促销风"}
    
    # 保存到日志
    save_to_log(f"\n📝 商品: {product}")
    save_to_log(f"🎨 风格: {style_names[style]}")
    save_to_log(f"📝 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    save_to_log(copy)
    save_to_log("-" * 30)