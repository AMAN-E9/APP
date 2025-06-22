import streamlit as st
from gptgod_features import chat_with_gptgod, generate_image

st.set_page_config(page_title="GPTGod Tools", page_icon="🔥")
st.title("🔥 GPTGod Feature Tester")

prompt = st.text_input("📝 Enter your prompt")

col1, col2 = st.columns(2)

with col1:
    if st.button("💬 Chat (Internet GPT)"):
        st.markdown("⌛ Getting answer from GPTGod...")
        output = chat_with_gptgod(prompt)
        st.markdown("### 🤖 Response:")
        st.markdown(output)

with col2:
    if st.button("🎨 Generate Image"):
        st.markdown("🖌️ Generating Image...")
        img_url = generate_image(prompt)
        if img_url.startswith("http"):
            st.image(img_url, caption="🖼️ AI Generated Image")
        else:
            st.markdown(img_url)
