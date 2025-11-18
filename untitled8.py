import streamlit as st
from openai import OpenAI
import os

# 💎 ─────────────────────────────
# 白 × 水色 かわいいシンプルデザイン
# 💎 ─────────────────────────────
st.markdown("""
<style>

html, body {
    background-color: #f7fbff; 
}

/* タイトル・見出し */
h1, h2, h3 {
    color: #3aa7e0 !important;
    font-weight: 700;
}

/* カード（白 × 水色） */
.card {
    background: #ffffff;
    border: 2px solid #cfeaff;
    border-radius: 16px;
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(180, 215, 255, 0.25);
}

/* 入力フォーム */
input, textarea {
    border-radius: 10px !important;
    border: 1.5px solid #b8e1ff !important;
    padding: 8px !important;
    background-color: white !important;
}

/* Streamlit の hidden input を非表示にする（←空白の枠の原因） */
input[type="hidden"] {
    display: none !important;
}

/* ボタン（白 × 水色） */
div.stButton > button {
    background-color: #d4efff;
    color: #1b85c9;
    border-radius: 12px;
    padding: 8px 20px;
    border: 1.5px solid #9ad7ff;
    font-size: 16px;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #bde6ff;
    border-color: #7ccaff;
}

/* 成功メッセージ */
div.stAlert.success {
    background-color: #e3f6ff;
    border-left: 5px solid #5cc0ff !important;
    color: #1479b8;
}

/* warning */
div.stAlert.warning {
    background-color: #fff8e5;
    border-left: 5px solid #ffc96b !important;
    color: #b37a00;
}

/* レシピ文を読みやすく */
p, li {
    font-size: 16px;
    line-height: 1.6;
    color: #234b5e;
}

</style>
""", unsafe_allow_html=True)

# 🔒 OpenAI APIキー
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。Secrets または環境変数に設定してください。")
else:
    client = OpenAI(api_key=api_key)

    # 🌸 タイトル
    st.title("🍳 ディナープランナー")
    st.write("食材と気分から、ぴったりのレシピを提案します！")

    # 入力欄カード
    st.markdown('<div class="card">', unsafe_allow_html=True)

    ingredients = st.text_input("食材を入力（カンマ区切りで）")
    mood = st.text_input("今日の気分（例：疲れた、寒い、元気）")

    st.markdown("</div>", unsafe_allow_html=True)

    # 🍱 ボタン
    if st.button("レシピを提案して！"):

        if not ingredients or not mood:
            st.warning("⚠️ 食材と気分の両方を入力してください。")
        else:
