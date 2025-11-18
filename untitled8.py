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

/* 成功メッセージを水色化 */
div.stAlert.success {
    background-color: #e3f6ff;
    border-left: 5px solid #5cc0ff !important;
    color: #1479b8;
}

/* warning を優しい色に */
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



# 🔒 OpenAI APIキーの読み込み
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。Secrets または環境変数に設定してください。")
else:
    client = OpenAI(api_key=api_key)

    # 🌸 タイトル
    st.title("🍳 ディナープランナー")
    st.write("食材と気分から、ぴったりのレシピを提案します！")

    # ✅ 入力欄カード
    st.markdown('<div class="card">', unsafe_allow_html=True)

    ingredients = st.text_input("食材を入力（カンマ区切りで）")
    mood = st.text_input("今日の気分（例：疲れた、寒い、元気）")

    st.markdown("</div>", unsafe_allow_html=True)

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
                5. 栄養情報（目安）
                   - カロリー（kcal）
                   - タンパク質（g）
                   - 脂質（g）
                   - 炭水化物（g）
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful Japanese cooking assistant."},
                        {"role": "user", "content": prompt}
                    ],
                )

                recipe = response.choices[0].message.content

            # ✅ レシピ表示カード
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.success("🍽️ レシピができました！")
            st.markdown(recipe)

            st.markdown("</div>", unsafe_allow_html=True)
