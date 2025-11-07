import streamlit as st
from openai import OpenAI
import os

# 🔒 OpenAIのAPIキーを安全に読み込み
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。Secretsまたは環境変数に追加してください。")
else:
    client = OpenAI(api_key=api_key)

    # 🌸 タイトルと説明
    st.title("🍳 AIレシピアシスタント（無料画像つき）")
    st.write("食材と気分を入力すると、レシピと栄養情報を提案します！")
    st.write("※画像は無料のBing検索リンクで表示します。")

    # 🥕 入力欄
    ingredients = st.text_input("食材を入力（カンマ区切りで）")
    mood = st.text_input("今日の気分（例：疲れた、寒い、元気）")

    # 🍱 ボタンを押したとき
    if st.button("レシピを提案して！"):
        if not ingredients or not mood:
            st.warning("⚠️ 食材と気分の両方を入力してください。")
        else:
            with st.spinner("レシピを考え中...👩‍🍳"):
                # 🧠 AIへの指示
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

                # 🍳 レシピ生成
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful Japanese cooking assistant."},
                        {"role": "user", "content": prompt}
                    ],
                )

                recipe = response.choices[0].message.content

            # ✅ 結果を表示
            st.success("🍽️ レシピができました！")
            st.markdown(recipe)

            # 🖼️ 無料の画像検索リンクを作成（Bing）
            try:
                recipe_name = recipe.splitlines()[0].replace("1. ", "").strip()
                query = f"{recipe_name} 和食 料理"
                bing_url = f"https://www.bing.com/images/search?q={query}"

                st.markdown(f"🔍 [この料理の画像をBingで見る]({bing_url})")

            except Exception as e:
                st.warning("⚠️ 画像リンクの作成に失敗しました。")
                st.write(e)

            # 💾 保存機能
            if "history" not in st.session_state:
                st.session_state.history = []

            if st.button("このレシピを保存する"):
                st.session_state.history.append(recipe)
                st.success("💾 レシピを保存しました！")

    # 📖 保存したレシピを表示
    if "history" in st.session_state and st.session_state.history:
        st.subheader("📜 保存したレシピ")
        for i, r in enumerate(st.session_state.history):
            with st.expander(f"レシピ {i+1}"):
                st.markdown(r)
