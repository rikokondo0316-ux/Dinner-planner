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
    st.title("🍳 AIレシピアシスタント（画像表示つき）")
    st.write("食材と気分を入力すると、レシピ・栄養情報・画像を提案します！")

    # 🥕 入力欄
    ingredients = st.text_input("食材を入力（カンマ区切りで）")
    mood = st.text_input("今日の気分（例：疲れた、寒い、元気）")

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

            # ✅ レシピを表示
            st.success("🍽️ レシピができました！")
            st.markdown(recipe)

          # 🖼️ Pixabay画像を表示（精度アップ版！）
try:
    recipe_name = recipe.splitlines()[0].replace("1. ", "").strip()

    PIXABAY_KEY = st.secrets["PIXABAY_API_KEY"]

    # ✅ 和食の料理っぽさを強化したクエリ
    query = f"{recipe_name} Japanese food dish 和食 料理 食べ物"

    url = (
        f"https://pixabay.com/api/?key={PIXABAY_KEY}"
        f"&q={query}"
        f"&image_type=photo"
        f"&category=food"
        f"&orientation=horizontal"
    )

    res = requests.get(url)
    data = res.json()

    if "hits" not in data or len(data["hits"]) == 0:
        st.warning("⚠️ 合う画像が見つかりませんでした。")
    else:
        img_url = data["hits"][0]["webformatURL"]
        st.image(img_url, caption=f"{recipe_name}（Pixabay画像）")

except Exception as e:
    st.warning("⚠️ 画像の取得でエラーが出ました。")
    st.write(e)


