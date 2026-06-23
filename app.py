import streamlit as st
import os
from gtts import gTTS
import google.generativeai as genai

# Setup page layout
st.set_page_config(page_title="Sahabat Cerita AI", page_icon="📖", layout="wide")

st.title("📖 Sahabat Cerita AI / AI Story Buddy")
st.write("Cipta cerita pengembaraan kamu sendiri! / Create your own adventure story!")

st.header("🎨 Pilih Elemen Cerita / Choose Story Elements")
col1, col2, col3 = st.columns(3)

with col1:
    character = st.selectbox("🐱 Watak / Character", ["Cat", "Dog", "Bird", "Rabbit"])
with col2:
    setting = st.selectbox("🚀 Tempat / Setting", ["Treasure Island", "Magic Forest", "Outer Space", "Cloud Castle"])
with col3:
    emotion = st.selectbox("😊 Emosi / Emotion", ["Happy", "Excited", "Brave", "Mysterious"])

if st.button("🚀 Bina Cerita Saya! / Generate My Story!", type="primary"):
    with st.spinner("✨ Creating your storybook..."):
        try:
            # Secure connection to your Streamlit secrets block
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("❌ API key missing! Please check your Streamlit App Secrets.")
                st.stop()
                
            genai.configure(api_key=api_key)
            text_model = genai.GenerativeModel("gemini-2.5-flash")

            story_prompt = f"""
            Write a short 3-page children's story about a {character} in {setting} feeling {emotion}.
            For each page, write an English paragraph and a Bahasa Melayu translation.
            Format your output strictly as a Python dictionary like this:
            {{'p1_en': 'text', 'p1_bm': 'text', 'p2_en': 'text', 'p2_bm': 'text', 'p3_en': 'text', 'p3_bm': 'text'}}
            Do not wrap the dictionary in markdown blocks. Return ONLY the raw dictionary text string.
            """
            
            response = text_model.generate_content(story_prompt)
            clean_text = response.text.strip().replace("```python", "").replace("```", "")
            pages = eval(clean_text)

            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")
            tabs = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    en_key = f"p{i}_en"
                    bm_key = f"p{i}_bm"
                    
                    # Stable, permanent placeholder vector illustration to prevent network hangs
                    st.image("https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800&auto=format&fit=crop&q=60", caption="Buku Cerita Digital")
                    
                    if en_key in pages:
                        st.subheader("🇬🇧 English")
                        st.info(pages[en_key])
                        gTTS(text=pages[en_key], lang='en').save(f"p{i}_en.mp3")
                        st.audio(f"p{i}_en.mp3", format="audio/mp3")
                        
                    if bm_key in pages:
                        st.subheader("🇲🇾 Bahasa Melayu")
                        st.success(pages[bm_key])
                        gTTS(text=pages[bm_key], lang='ms').save(f"p{i}_bm.mp3")
                        st.audio(f"p{i}_bm.mp3", format="audio/mp3")

        except Exception as err:
            st.error("An authentication profile issue occurred.")
            st.exception(err)
