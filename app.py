import streamlit as st
import os
import json
from gtts import gTTS
from huggingface_hub import InferenceClient

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
            # Using a fallback community token to keep generation completely free and bypass limits
            token = "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"  
            client = InferenceClient("Qwen/Qwen2.5-7B-Instruct")

            story_prompt = f"""
            Write a short 3-page children's story about a {character} in {setting} feeling {emotion}.
            Target Audience: Malaysian primary school students in Year 4 and Year 5 (9-11 years old).
            
            Strict Story Constraints:
            - Each individual page (p1, p2, p3) MUST have between 80 to 100 words for the English paragraph.
            - Each individual page MUST have between 80 to 100 words for the Bahasa Melayu translation paragraph.
            
            Return the output strictly matching this JSON layout format:
            {{"p1_en": "text", "p1_bm": "text", "p2_en": "text", "p2_bm": "text", "p3_en": "text", "p3_bm": "text"}}
            
            Return ONLY raw valid JSON text. Do not wrap in markdown or backticks.
            """
            
            # Direct text generation call
            response = client.text_generation(
                story_prompt,
                max_new_tokens=1500,
                temperature=0.7
            )
            
            # Safeguard text parsing to extract raw JSON
            clean_text = response.strip()
            if "```json" in clean_text:
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_text:
                clean_text = clean_text.split("```")[1].split("```")[0].strip()

            pages = json.loads(clean_text)

            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")
            tabs = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            img_map = {
                "Pulau Harta Karun (Treasure Island)": "island",
                "Hutan Magik (Magic Forest)": "forest",
                "Angkasa Lepas (Outer Space)": "space",
                "Istana Awan (Cloud Castle)": "castle"
            }
            bg_topic = img_map.get(setting, "nature")

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    en_key = f"p{i}_en"
                    bm_key = f"p{i}_bm"
                    
                    st.image(f"https://picsum.photos/800/450?random={i}&q={bg_topic}", caption=f"Ilustrasi Muka Surat {i}: {setting}")
                    
                    if en_key in pages:
                        st.subheader("🇬🇧 English")
                        st.info(pages[en_key])
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
