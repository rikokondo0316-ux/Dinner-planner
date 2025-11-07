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

            # 🖼️ 無料でBing画像を1枚表示
            try:
                recipe_name = recipe.splitlines()[0].replace("1. ", "").strip()
                query = f"{recipe_name} 和食 料理"
                bing_url = f"https://www.bing.com/images/search?q={query}"

                # 🌐 Bing検索ページを取得
                headers = {"User-Agent": "Mozilla/5.0"}
                res = requests.get(bing_url, headers=headers)
                soup = BeautifulSoup(res.text, "html.parser")

                # 🖼️ 最初の画像URLを探す
                img_tag = soup.find("img")
                if img_tag and "src" in img_tag.attrs:
                    img_url = img_tag["src"]
                    st.image(img_url, caption=f"{recipe_name}（Bing画像）")
                else:
                    st.warning("⚠️ 画像を見つけられませんでした。")
                
                # 🔗 リンクも残しておく
                st.markdown(f"🔍 [もっと画像を見る]({bing_url})")

            except Exception as e:
                st.warning("⚠️ 画像の取得に失敗しました。")
                st.write(e)
