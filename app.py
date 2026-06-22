import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# Configure the free Gemini API service directly using your secrets asset
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    # Fallback to check if it's stored under a different variable identifier
    for key in st.secrets:
        if "KEY" in key.upper():
            genai.configure(api_key=st.secrets[key])

def generate_cartoon_illustration(story_text):
    """Generates a child-friendly cartoon image using Gemini's free Imagen model."""
    try:
        prompt = f"A vibrant, child-friendly digital cartoon illustration for a children's book. Watercolor style, simple friendly shapes, bright colors. Scene description: {story_text}"
        model = genai.ImageGenerationModel("imagen-3.0-generate-002")
        result = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            file_output_format="jpeg"
        )
        return result.generated_images[0].image
    except Exception as e:
        print(f"Gemini Imagen Error: {e}")
        return None

# Your existing configuration line
st.set_page_config(page_title="Sahabat Cerita AI", page_icon="📖", layout="wide")

# App Styling for Primary Students
st.title("📖 Sahabat Cerita AI / AI Story Buddy")
st.write("Cipta cerita pengembaraan kamu sendiri! / Create your own adventure story!")

# 1. THE INTERACTIVE INPUT ZONE (Emoji Buttons)
st.header("🎨 Pilih Elemen Cerita / Choose Story Elements")

coll, col2, col3 = st.columns(3)

with coll:
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
    with st.spinner("✨ Sedang mencipta cerita magik kamu... / Creating your magic story..."):
        try:
            # Generate Text using Gemini
            text_model = genai.GenerativeModel("gemini-1.5-flash")
            story_prompt = f"""
            Write a 3-page children's story based on: Character: {character}, Setting: {setting}, Emotion: {emotion}.
            For each page, provide exactly one page of English and its translation in Bahasa Melayu.
            Format your final response strictly as a Python dictionary with keys:
            'p1_en', 'p1_bm', 'p2_en', 'p2_bm', 'p3_en', 'p3_bm'
            Output ONLY the raw dictionary formatting structure. No markdown formatting blocks or surrounding text.
            """
            response = text_model.generate_content(story_prompt)
            
            # Clean response text up and safely parse dictionary
            clean_text = response.text.strip().replace("```python", "").replace("```", "")
            pages = eval(clean_text)

            # 3. INTERACTIVE BILINGUAL DISPLAY ZONE
            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")

            # Tabbed interface mimicking turning pages
            tab1, tab2, tab3 = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            with tab1:
                if 'p1_en' in pages:
                    story_img = generate_cartoon_illustration(pages['p1_en'])
                    if story_img:
                        st.image(story_img, use_container_width=True, caption="AI Illustrated Scene")
                    else:
                        st.warning("Could not load page illustration.")

                if 'p1_en' in pages:
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
                    story_img = generate_cartoon_illustration(pages['p2_en'])
                    if story_img:
                        st.image(story_img, use_container_width=True, caption="AI Illustrated Scene")
                    else:
                        st.warning("Could not load page illustration.")

                if 'p2_en' in pages:
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
                    story_img = generate_cartoon_illustration(pages['p3_en'])
                    if story_img:
                        st.image(story_img, use_container_width=True, caption="AI Illustrated Scene")
                    else:
                        st.warning("Could not load page illustration.")

                if 'p3_en' in pages:
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