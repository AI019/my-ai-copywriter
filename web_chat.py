import streamlit as st
import requests
from datetime import datetime

# 页面配置
st.set_page_config(page_title="AI 聊天助手", page_icon="🤖")

# 标题
st.title("🤖 AI 聊天助手")
st.caption(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
API_KEY = "sk-gvzojjeykwdbiutvxartsqanvauatejktmprxgczeidfcyes"
url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

if prompt := st.chat_input("在这里输入你的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 调用 AI
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    
    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考..."):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            else:
                error_msg = f"❌ 错误: {response.status_code}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})