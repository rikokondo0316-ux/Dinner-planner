import streamlit as st
from openai import OpenAI
import os

# 🔒 APIキーの安全な読み込み
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。Secretsまたは環境変数に追加してください。")
else:
    client = OpenAI(api_key=api_key)

    # 🌸 アプリのタイトルと説明
    st.title("🍳 AIレシピアシスタント")
    st.write("食材と気分を入力すると、レシピ・栄養情報・完成イメージを提案します！")

    # 🥕 入力フォーム
    ingredients = st.text_input("食材を入力（カンマ区切りで）")
    mood = st.text_input("今日の気分（例：疲れた、寒い、元気）")

    # 🍱 ボタンが押されたらレシピを生成
    if st.button("レシピを提案して！"):
        if not ingredients or not mood:
            st.warning("⚠️ 食材と気分の両方を入力してください。")
        else:
            with st.spinner("レシピを考え中...👩‍🍳"):
                # 🧠 レシピ生成プロンプト
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

                # 🍳 ChatGPTにレシピ生成を依頼
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful Japanese cooking assistant."},
                        {"role": "user", "content": prompt}
                    ],
                )

                recipe = response.choices[0].message.content

            # 🖼️ 料理画像を生成
            with st.spinner("完成イメージを作成中...🍱"):
                image_prompt = f"{recipe.splitlines()[0]} の完成料理写真のようなリアルな画像。和食スタイル、自然光。"
                try:
                    image_response = client.images.generate(
                        model="gpt-image-1",
                        prompt=image_prompt,
                        size="1024x1024"
                    )
                    image_url = image_response.data[0].url
                    st.image(image_url, caption="完成イメージ🍽️")
                except Exception as e:
                    st.warning("⚠️ 画像生成に失敗しました。APIの設定を確認してください。")
                    st.write(e)

            # ✅ 結果の表示
            st.success("🍽️ レシピができました！")
            st.markdown(recipe)

            # 💾 オプション：保存機能
            if "history" not in st.session_state:
                st.session_state.history = []
            if st.button("このレシピを保存する"):
                st.session_state.history.append(recipe)
                st.success("💾 レシピを保存しました！")

    # 📜 履歴の表示
    if "history" in st.session_state and st.session_state.history:
        st.subheader("📖 保存したレシピ")
        for i, r in enumerate(st.session_state.history):
            with st.expander(f"レシピ {i+1}"):
                st.markdown(r)
