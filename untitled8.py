st.markdown("""
<style>
/* 全体の背景色 */
body {
    background-color: #fff7fc;
}

/* ボックスのデザイン */
div.stButton > button {
    background-color: #ffb7d5;
    color: white;
    border-radius: 12px;
    padding: 8px 20px;
    border: none;
    font-size: 16px;
}
div.stButton > button:hover {
    background-color: #ff99c8;
}

/* 入力欄デザイン */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #ffc6d9 !important;
}

/* タイトル文字を可愛く */
h1 {
    color: #ff66a3 !important;
}
</style>
""", unsafe_allow_html=True)

import streamlit as st
from openai import OpenAI
import os
import requests
from bs4 import BeautifulSoup  # ← 追加（画像を探すため）

# 🔒 OpenAIのAPIキーを安全に読み込み
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。Secretsまたは環境変数に追加してください。")
else:
    client = OpenAI(api_key=api_key)

    # 🌸 タイトルと説明
    st.title("🍳ディナープランナー")
    st.write("食材と気分を入力すると、レシピ・栄養情報・を提案します！")

    # 🥕 入力欄
    ingredients = st.text_input("食材を入力（カンマ区切りで）")
    mood = st.text_input("今日の気分（例：疲れた、寒い、元気）")
st.markdown(
    """
    

    # 🍱 ボタン
    if st.button("レシピを提案して！"):
        if not ingredients or not mood:
            st.warning("⚠️ 食材と気分の両方を入力してください。")
        else:
            with st.spinner("レシピを考え中...👩‍🍳"):
                prompt = f"""
                あなたは日本料理の専門家であり、栄養士でもあります。
                次の食材を使って日本風の家庭料理を1つ提案してください。

                食材: {ingredients}
                気分: {mood}

                以下の形式で答えてください：
                1. レシピ名
                2. 説明
                3. 材料
                4. 作り方
                5. 栄養情報（目安で構いません）
                   - カロリー（kcal）
                   - タンパク質（g）
                   - 脂質（g）
                   - 炭水化物（g）
                """

                # 🧠 ChatGPTでレシピ生成
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful Japanese cooking assistant."},
                        {"role": "user", "content": prompt}
                    ],
                )
                recipe = response.choices[0].message.content
st.markdown(
    """
    <div style="
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top:20px;
    ">
    """,
    unsafe_allow_html=True
)

st.markdown(recipe)

st.markdown("</div>", unsafe_allow_html=True)

            # ✅ レシピを表示
            st.success("🍽️ レシピができました！")
            st.markdown(recipe)

