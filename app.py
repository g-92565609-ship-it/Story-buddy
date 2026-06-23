import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image

# App configuration line
st.set_page_config(page_title="Sahabat Cerita AI", page_icon="📖", layout="wide")

# App Styling for Primary Students
st.title("📖 Sahabat Cerita AI / AI Story Buddy")
st.write("Cipta cerita pengembaraan kamu sendiri! / Create your own adventure story!")

# 1. THE INTERACTIVE INPUT ZONE
st.header("🎨 Pilih Elemen Cerita / Choose Story Elements")

col1, col2, col3 = st.columns(3)

with col1:
    character = st.selectbox(
        "🐱 Pilih Watak / Choose Character",
        ["Kucing Comel (Cute Cat)", "Anjing Setia (Loyal Dog)", "Burung Bijak (Wise Bird)", "Arnab Pintar (Clever Rabbit)"]
    )

with col2:
    setting = st.selectbox(
        "🚀 Pilih Tempat / Choose Setting",
        ["Pulau Harta Karun (Treasure Island)", "Hutan Magik (Magic Forest)", "Angkasa Lepas (Outer Space)", "Istana Awan (Cloud Castle)"]
    )

with col3:
    emotion = st.selectbox(
        "😊 Pilih Emosi / Choose Emotion",
        ["Gembira (Happy)", "Teruja (Excited)", "Berani (Brave)", "Misteri (Mysterious)"]
    )

if st.button("🚀 Bina Cerita Saya! / Generate My Story!", type="primary"):
    with st.spinner("✨ Sedang mencipta cerita magik & lukisan kamu... / Creating your story & illustrations..."):
        try:
            # Safe inline imports to prevent boot crashes
            from gtts import gTTS
            import google.generativeai as genai
            
            if "GEMINI_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            else:
                for key in st.secrets:
                    if "KEY" in key.upper():
                        genai.configure(api_key=st.secrets[key])

            text_model = genai.GenerativeModel("gemini-2.5-flash")

            story_prompt = f"""
            Write a 3-page children's story based on: Character: {character}, Setting: {setting}, Emotion: {emotion}.
            For each page, provide exactly one page of English and its translation in Bahasa Melayu.
            Format your final response strictly as a Python dictionary with keys:
            'p1_en', 'p1_bm', 'p2_en', 'p2_bm', 'p3_en', 'p3_bm'
            Output ONLY the raw dictionary formatting structure. No markdown formatting blocks or surrounding text.
            """
            response = text_model.generate_content(story_prompt)
            
            clean_text = response.text.strip().replace("```python", "").replace("```", "")
            pages = eval(clean_text)

            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")
            tab1, tab2, tab3 = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            # Cleaned function to request image bytes via gemini-2.5-flash
            def generate_page_illustration(story_text):
                try:
                    img_prompt = f"Return a beautiful, vibrant cartoon illustration for a children's storybook based on this scene: {story_text}. Use your image generation modality output."
                    # We call your active, working text_model directly but specify image response modalities
                    img_resp = text_model.generate_content(
                        img_prompt,
                        generation_config={"response_modalities": ["IMAGE"]}
                    )
                    
                    # Extract the raw image bytes from the model parts
                    for part in img_resp.candidates[0].content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data:
                            img_bytes = base64.b64decode(part.inline_data.data)
                            return Image.open(BytesIO(img_bytes))
                except Exception as e:
                    return f"⚠️ Image generation profile error: {str(e)}"
                return None

            with tab1:
                if 'p1_en' in pages:
                    img1 = generate_page_illustration(pages['p1_en'])
                    if isinstance(img1, str):
                        st.warning(img1)
                    elif img1:
                        st.image(img1, use_container_width=True)
                    st.subheader("🇬🇧 English")
                    st.info(pages['p1_en'])
                    tts_en = gTTS(text=pages['p1_en'], lang='en')
                    tts_en.save("p1_en.mp3")
                    st.audio("p1_en.mp3", format="audio/mp3")
                if 'p1_bm' in pages:
                    st.subheader("🇲🇾 Bahasa Melayu")
                    st.success(pages['p1_bm'])
                    tts_ms = gTTS(text=pages['p1_bm'], lang='ms')
                    tts_ms.save("p1_ms.mp3")
                    st.audio("p1_ms.mp3", format="audio/mp3")

            with tab2:
                if 'p2_en' in pages:
                    img2 = generate_page_illustration(pages['p2_en'])
                    if isinstance(img2, str):
                        st.warning(img2)
                    elif img2:
                        st.image(img2, use_container_width=True)
                    st.subheader("🇬🇧 English")
                    st.info(pages['p2_en'])
                    tts_en = gTTS(text=pages['p2_en'], lang='en')
                    tts_en.save("p2_en.mp3")
                    st.audio("p2_en.mp3", format="audio/mp3")
                if 'p2_bm' in pages:
                    st.subheader("🇲🇾 Bahasa Melayu")
                    st.success(pages['p2_bm'])
                    tts_ms = gTTS(text=pages['p2_bm'], lang='ms')
                    tts_ms.save("p2_ms.mp3")
                    st.audio("p2_ms.mp3", format="audio/mp3")

            with tab3:
                if 'p3_en' in pages:
                    img3 = generate_page_illustration(pages['p3_en'])
                    if isinstance(img3, str):
                        st.warning(img3)
                    elif img3:
                        st.image(img3, use_container_width=True)
                    st.subheader("🇬🇧 English")
                    st.info(pages['p3_en'])
                    tts_en = gTTS(text=pages['p3_en'], lang='en')
                    tts_en.save("p3_en.mp3")
                    st.audio("p3_en.mp3", format="audio/mp3")
                if 'p3_bm' in pages:
                    st.subheader("🇲🇾 Bahasa Melayu")
                    st.success(pages['p3_bm'])
                    tts_ms = gTTS(text=pages['p3_bm'], lang='ms')
                    tts_ms.save("p3_ms.mp3")
                    st.audio("p3_ms.mp3", format="audio/mp3")

        except Exception as global_err:
            st.error("An issue occurred generating the content layout.")
            st.exception(global_err)
