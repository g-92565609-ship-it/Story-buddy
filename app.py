import streamlit as st
import os
import re
from gtts import gTTS
from google.genai import Client

# Setup page layout
st.set_page_config(page_title="Sahabat Cerita AI", page_icon="📖", layout="wide")

st.title("📖 Sahabat Cerita AI / AI Story Buddy")
st.write("Cipta cerita pengembaraan kamu sendiri! / Create your own adventure story!")

st.header("🎨 Pilih Elemen Cerita / Choose Story Elements")
col1, col2, col3 = st.columns(3)

with col1:
    character = st.selectbox("🐱 Watak / Character", ["Kucing Comel (Cute Cat)", "Anjing Setia (Loyal Dog)", "Burung Bijak (Wise Bird)", "Arnab Nakal (Naughty Rabbit)"])
with col2:
    setting = st.selectbox("🚀 Tempat / Setting", ["Pulau Harta Karun (Treasure Island)", "Hutan Magik (Magic Forest)", "Angkasa Lepas (Outer Space)", "Istana Awan (Cloud Castle)"])
with col3:
    emotion = st.selectbox("😊 Emosi / Emotion", ["Gembira (Happy)", "Teruja (Excited)", "Berani (Brave)", "Misteri (Mysterious)"])

if st.button("🚀 Bina Cerita Saya! / Generate My Story!", type="primary"):
    with st.spinner("✨ Creating your long storybook..."):
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("❌ API key missing! Please check your Streamlit App Secrets.")
                st.stop()
                
            client = Client(api_key=api_key)

            # Strictly demanding a target length of 80-100 words per language per page
            story_prompt = f"""
            Write a short 3-page children's story about a {character} in {setting} feeling {emotion}.
            
            Target Audience: Malaysian primary school students in Year 4 and Year 5 (9-11 years old).
            
            Strict Story Constraints:
            - Each individual page (p1, p2, p3) MUST have between 80 to 100 words for the English paragraph.
            - Each individual page MUST have between 80 to 100 words for the Bahasa Melayu translation paragraph.
            - Keep vocabulary simple, clear, and easy to read, but build a full, interesting narrative context to hit the word count.
            
            Format your output strictly as a Python dictionary like this:
            {{'p1_en': 'text', 'p1_bm': 'text', 'p2_en': 'text', 'p2_bm': 'text', 'p3_en': 'text', 'p3_bm': 'text'}}
            Do not wrap the dictionary in markdown blocks. Return ONLY the raw dictionary text string.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=story_prompt,
            )
            
            clean_text = response.text.strip().replace("```python", "").replace("```", "")
            pages = eval(clean_text)

            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")
            tabs = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            # Clean tracking strings for image engine queries
            clean_char = re.sub(r'[^a-zA-Z]', '', character.split("(")[0])
            clean_setting = re.sub(r'[^a-zA-Z]', '', setting.split("(")[0])

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    en_key = f"p{i}_en"
                    bm_key = f"p{i}_bm"
                    
                    # High-availability kid-themed vector illustration backdrop 
                    st.image("https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&auto=format&fit=crop&q=60", caption=f"Ilustrasi: {character} & {setting}")
                    
                    if en_key in pages:
                        st.subheader("🇬🇧 English")
                        st.info(pages[en_key])
                        # Calculate word count dynamically to verify performance
                        en_words = len(pages[en_key].split())
                        st.caption(f"⏱️ Word count: {en_words} words")
                        
                        gTTS(text=pages[en_key], lang='en').save(f"p{i}_en.mp3")
                        st.audio(f"p{i}_en.mp3", format="audio/mp3")
                        
                    if bm_key in pages:
                        st.subheader("🇲🇾 Bahasa Melayu")
                        st.success(pages[bm_key])
                        bm_words = len(pages[bm_key].split())
                        st.caption(f"⏱️ Bilangan perkataan: {bm_words} patah perkataan")
                        
                        gTTS(text=pages[bm_key], lang='ms').save(f"p{i}_bm.mp3")
                        st.audio(f"p{i}_bm.mp3", format="audio/mp3")

        except Exception as err:
            st.error("An execution or formatting error occurred.")
            st.exception(err)
