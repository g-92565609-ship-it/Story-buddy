import streamlit as st
import os
import json
from gtts import gTTS
from google.genai import Client
from google.genai import types

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
    with st.spinner("✨ Creating your long storybook and generating custom illustrations..."):
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("❌ API key missing! Please check your Streamlit App Secrets.")
                st.stop()
                
            client = Client(api_key=api_key)

            # Requesting a strict JSON structure instead of a text dictionary to prevent eval errors
            story_prompt = f"""
            Write a short 3-page children's story about a {character} in {setting} feeling {emotion}.
            
            Target Audience: Malaysian primary school students in Year 4 and Year 5 (9-11 years old).
            
            Strict Story Constraints:
            - Each individual page (p1, p2, p3) MUST have between 80 to 100 words for the English paragraph.
            - Each individual page MUST have between 80 to 100 words for the Bahasa Melayu translation paragraph.
            - Provide a detailed English descriptive prompt for an image generator showing the scene layout.
            
            Return the output strictly matching this JSON schema layout:
            {{
                "p1_en": "text", "p1_bm": "text", "p1_img_prompt": "description",
                "p2_en": "text", "p2_bm": "text", "p2_img_prompt": "description",
                "p3_en": "text", "p3_bm": "text", "p3_img_prompt": "description"
            }}
            Return ONLY the raw valid JSON object. Do not wrap in markdown or backticks.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=story_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            pages = json.loads(response.text.strip())

            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")
            tabs = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    en_key = f"p{i}_en"
                    bm_key = f"p{i}_bm"
                    img_prompt_key = f"p{i}_img_prompt"
                    
                    # Generate a native custom cartoon illustration using Imagen 3
                    if img_prompt_key in pages:
                        try:
                            raw_prompt = pages[img_prompt_key]
                            full_image_prompt = f"Cute children's book illustration, 3D cartoon style, vibrant colors, friendly character, safe for kids: {raw_prompt}"
                            
                            image_result = client.models.generate_images(
                                model='imagen-3.0-generate-002',
                                prompt=full_image_prompt,
                                config=types.GenerateImagesConfig(
                                    number_of_images=1,
                                    output_mime_type="image/jpeg",
                                    aspect_ratio="16:9"
                                )
                            )
                            
                            for generated_image in image_result.generated_images:
                                st.image(generated_image.image.image_bytes, caption=f"Ilustrasi Muka Surat {i}")
                        except Exception as img_err:
                            st.warning("⚠️ Could not generate custom illustration, rendering placeholder scene instead.")
                            st.image("https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800", caption="Ilustrasi Buku Cerita")
                    
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
