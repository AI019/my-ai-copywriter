# 由 Cline 协助修改
import os

import streamlit as st
import requests
from datetime import datetime
from docx import Document
from io import BytesIO
from pathlib import Path

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_OPTIONS = {
    "DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
    "Kimi-K2.5": "Pro/moonshotai/Kimi-K2.5",
    "通义千问 Qwen2.5-72B": "Qwen/Qwen2.5-72B-Instruct",
    "通义千问 Qwen3-8B": "Qwen/Qwen3-8B",
    "智谱 GLM-4-9B": "Zhipu/GLM-4-9B-Chat",
    "百川 Baichuan4": "Baichuan/Baichuan4",
    }
REQUEST_TIMEOUT = 60
LOG_DIR = Path(__file__).parent


# 风格对应的 prompt 映射
# 页面配置
st.set_page_config(page_title="AI 文案生成器", page_icon="✍️")

# 标题
st.title("✍️ AI 文案生成器")
st.caption(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# 风格对应的 prompt 映射
def get_prompt(style, product):
    prompts = {
        "小红书种草风": f"""你是一个小红书种草博主，请为以下商品写一篇小红书风格的种草文案。

商品：{product}

要求：
1. 标题要吸引人，带emoji
2. 正文分3-4个卖点，每个卖点用emoji开头
3. 语气亲切自然，像朋友推荐
4. 结尾加上3-5个相关标签

请直接输出文案，不要有其他说明。""",

        "朋友圈分享风": f"""请为商品「{product}」写一段微信朋友圈风格的推荐文案。

要求：
1. 简短有力，不超过150字
2. 语气亲切，像朋友在分享
3. 带2-3个emoji
4. 结尾加一句号召性的话

请直接输出文案。""",

        "专业评测风": f"""请为商品「{product}」写一篇专业评测风格的文案。

要求：
1. 标题客观专业
2. 分3-4个技术/功能卖点，每个卖点有具体说明
3. 语气中立可信
4. 结尾给出总结和购买建议

请直接输出文案。""",

        "淘宝促销风": f"""请为商品「{product}」写一段淘宝详情页风格的促销文案。

要求：
1. 突出卖点和优惠
2. 使用短句、符号分隔
3. 语气热情有感染力
4. 结尾加上行动呼吁（如"点击购买"）

请直接输出文案。""",

        "微博热搜风": f"""请为商品「{product}」写一段微博热搜风格的推荐文案。

要求：
1. 开头用"#话题#"格式，像是热搜话题
2. 正文简短有力，不超过100字
3. 语气像网友热议，带2-3个emoji
4. 结尾带2-3个相关话题标签

请直接输出文案。""",

        "抖音脚本风": f"""请为商品「{product}」写一个抖音短视频脚本风格的文案。

要求：
1. 开头写出"【画面】"和"【文案】"
2. 分3-4个镜头，每个镜头15字以内
3. 最后一句是"🔥 点击购物车，同款 Get！"
4. 整体节奏快，有冲击力

请直接输出文案。""",

        "知乎干货风": f"""请为商品「{product}」写一段知乎回答风格的推荐文案。

要求：
1. 开头用"谢邀"或"作为XXX用户"
2. 正文分3-4个要点，每个要点有具体说明
3. 语气理性、专业、可信
4. 结尾总结并给出建议

请直接输出文案。""",

        "英文国际风": f"""Please write an English product description for "{product}".

Requirements:
1. Short and catchy title
2. 3-4 bullet points highlighting key features
3. Friendly, conversational tone
4. End with a call to action

Output in English only."""
    }
    return prompts.get(style, prompts["小红书种草风"])


def append_copy_log(log_filename, prod, style, model_name, body):
    try:
        log_path = LOG_DIR / log_filename
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n📝 商品: {prod}\n")
            f.write(f"🎨 风格: {style}\n")
            f.write(f"🤖 模型: {model_name}\n")
            f.write(f"📝 生成时间: {now_str}\n")
            f.write(body + "\n")
            f.write("-" * 50 + "\n")
    except OSError as e:
        st.warning(f"日志写入失败（{prod}）：{e}")


def parse_api_error(response):
    err_msg = f"❌ 生成失败，状态码：{response.status_code}"
    detail = ""
    try:
        body = response.json()
        if isinstance(body.get("error"), dict):
            detail = body["error"].get("message", "")
        if not detail:
            detail = body.get("message", "")
    except ValueError:
        detail = response.text[:300].strip()
    if detail:
        err_msg += f"\n详情：{detail}"
    if response.status_code == 403:
        err_msg += (
            "\n\n💡 Kimi 等部分模型需 SiliconFlow 账户完成实名认证，"
            "且 API Key 须来自已认证账户。请登录 https://cloud.siliconflow.cn "
            "检查「用户中心 → 实名认证」与账户余额。"
        )
    return err_msg


# 侧边栏：API Key 设置
with st.sidebar:
    st.header("⚙️ 设置")
    # 优先 secrets → 环境变量 → 手动输入
    api_key = st.secrets.get("API_KEY", "")
    if api_key:
        st.success("✅ API Key 已从 secrets 自动加载")
    elif os.environ.get("API_KEY"):
        api_key = os.environ.get("API_KEY", "")
        st.success("✅ API Key 已从环境变量自动加载")
    else:
        api_key = st.text_input("API Key", type="password", value="", help="本地测试时手动输入")
    st.markdown("---")
    st.caption("💡 提示：文案会保存在日志文件中，也可导出 Word 文档")

# 主界面
st.header("📝 生成文案")

# 商品名称输入（支持多个，用逗号分隔）
product = st.text_area(
    "商品名称（多个请用逗号分隔）",
    placeholder="例如：无线蓝牙耳机,便携咖啡杯,智能手表",
    height=80,
)

# 风格选择（8种风格）
style = st.selectbox(
    "选择文案风格", 
    options=["小红书种草风", "朋友圈分享风", "专业评测风", "淘宝促销风", "微博热搜风", "抖音脚本风", "知乎干货风", "英文国际风"],
    index=0,
    key="style_select"  # 添加唯一 key
)

# 模型选择
model_label = st.selectbox(
    "选择 AI 模型",
    options=list(MODEL_OPTIONS.keys()),
    index=0,
)
model_id = MODEL_OPTIONS[model_label]

# 生成按钮
if st.button("🚀 生成文案", type="primary"):
    if not product or not product.strip():
        st.error("请输入商品名称")
    elif not api_key.strip():
        st.error("请在侧边栏填写 API Key")
    else:
        products = [p.strip() for p in product.replace("，", ",").split(",") if p.strip()]
        if not products:
            st.error("请输入至少一个有效商品名称")
        else:
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            with st.spinner(f"{model_label} 正在为 {len(products)} 个商品创作文案..."):
                all_results = []
                ok_count = 0
                fail_count = 0
                log_filename = f"copy_log_web_{datetime.now().strftime('%Y%m%d')}.log"

                headers = {
                    "Authorization": f"Bearer {api_key.strip()}",
                    "Content-Type": "application/json",
                }

                for prod in products:
                    prompt = get_prompt(style, prod)
                    data = {
                        "model": model_id,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 800,
                    }

                    try:
                        response = requests.post(
                            API_URL,
                            headers=headers,
                            json=data,
                            timeout=REQUEST_TIMEOUT,
                        )
                    except requests.RequestException as e:
                        err_msg = f"❌ 网络请求失败：{e}"
                        all_results.append((prod, err_msg))
                        append_copy_log(log_filename, prod, style, model_label, err_msg)
                        fail_count += 1
                        continue

                    if response.status_code == 200:
                        try:
                            result = response.json()
                            ai_reply = result["choices"][0]["message"]["content"]
                        except (KeyError, IndexError, TypeError, ValueError) as e:
                            err_msg = f"❌ 响应解析失败：{e}"
                            all_results.append((prod, err_msg))
                            append_copy_log(log_filename, prod, style, model_label, err_msg)
                            fail_count += 1
                            continue

                        all_results.append((prod, ai_reply))
                        append_copy_log(log_filename, prod, style, model_label, ai_reply)
                        ok_count += 1
                    else:
                        err_msg = parse_api_error(response)
                        all_results.append((prod, err_msg))
                        append_copy_log(log_filename, prod, style, model_label, err_msg)
                        fail_count += 1

            if ok_count and not fail_count:
                st.success(f"✅ 成功生成 {ok_count} 篇文案！")
            elif ok_count and fail_count:
                st.warning(f"完成：成功 {ok_count} 篇，失败 {fail_count} 篇")
            else:
                st.error(f"全部失败（{fail_count} 篇），请检查 API Key 或网络")


            if all_results:
                doc = Document()
                doc.add_heading("AI 文案生成报告", 0)
                doc.add_paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                doc.add_paragraph(f"AI 模型：{model_label}")
                doc.add_paragraph(f"文案风格：{style}")
                doc.add_paragraph(f"商品数量：{len(all_results)} 个（成功 {ok_count}，失败 {fail_count}）")
                doc.add_paragraph("-" * 50)

                for i, (prod, content) in enumerate(all_results):
                    doc.add_heading(f"商品：{prod}", level=1)
                    doc.add_paragraph(content)
                    if i < len(all_results) - 1:
                        doc.add_page_break()

                doc_bytes = BytesIO()
                doc.save(doc_bytes)
                doc_bytes.seek(0)

                st.download_button(
                    label="📥 下载 Word 文档",
                    data=doc_bytes,
                    file_name=f"文案报告_{batch_id}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"download_{batch_id}",
                )
                st.markdown("---")

            for prod, content in all_results:
                with st.expander(f"📦 {prod}", expanded=True):
                    st.markdown(content)
            
            if ok_count > 0:
                st.balloons()
            
