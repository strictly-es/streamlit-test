import streamlit as st
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_image(image_url):
    """
    Process the image by sending its URL to GPT-4 Vision.
    """
    st.write(f"Image URL: {image_url}")  # Log the provided URL

    # Send the image URL to the GPT-4 Vision model
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
       messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "次の画像は間取り画像ですか？ 'yes' または 'no' と答えてください。"
                            "そして、もし間取り画像であれば、この画像に基づいて以下の形式で応答してください:\n\n"
                            "{\n"
                            "  \"is_floor_plan\": true,\n"
                            "  \"ideas\": [\n"
                            "    \"具体的な暮らしのアイディア1（200文字以内）\",\n"
                            "    \"具体的な暮らしのアイディア2（200文字以内）\"\n"
                            "  ]\n"
                            "}\n"
                            "アイディアにはこの間取りの特徴を反映させてください。例えば、リビングの広さ、キッチンの位置、窓の数などを考慮してください。\n"
                            "間取り画像でない場合は以下の形式で応答してください:\n\n"
                            "{\n"
                            "  \"is_floor_plan\": false,\n"
                            "  \"ideas\": []\n"
                            "}"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"{image_url}"},
                    }
                ],
            }
        ],
        max_tokens=300,
    )

    # Log the response
    # st.write("API Response:")
    # st.json(response)

    # Parse and return JSON response
    return json.loads(response.choices[0].message.content.strip())

# Streamlit UI
st.title("間取り画像から暮らしのアイディア生成")

# URL入力UI
image_url = st.text_input("画像のURLを入力してください")

if image_url:
    st.image(image_url, caption="指定された画像")
    st.write("画像を解析しています...")

    try:
        # API呼び出し
        response = process_image(image_url)

        # 結果の表示
        if response["is_floor_plan"]:
            st.success("図面の画像が認識されました。以下は具体的な暮らしのアイディアです:")
            for i, idea in enumerate(response["ideas"], 1):
                st.write(f"{i}. {idea}")
        else:
            st.error("図面の画像ではありません。別のURLを指定してください。")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")