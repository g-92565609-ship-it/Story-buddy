import streamlit as st
import os
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
    with st.spinner("✨ Creating your storybook..."):
        try:
            # Secure connection to your Streamlit secrets block
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("❌ API key missing! Please check your Streamlit App Secrets.")
                st.stop()
                
            client = Client(api_key=api_key)

            # Strictly forcing easy vocabulary tailored for Malaysian Year 4 & 5 school students
            story_prompt = f"""
            Write a simple, short 3-page children's story about a {character} in {setting} feeling {emotion}.
            
            Target Audience: Malaysian primary school students in Year 4 and Year 5 (9-11 years old).
            Language Rules:
            - Use very simple vocabulary, short sentences, and high-frequency school words.
            - Keep the Bahasa Melayu translation simple, direct, and aligned with standard primary school level.
            - Avoid complex metaphors or advanced tenses.
            
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

            # Extract clean search keywords from selections to make the image match the story dynamically!
            char_keyword = character.split("(")[-1].replace(")", "").strip().lower()
            place_keyword = setting.split("(")[-1].replace(")", "").strip().lower().replace(" ", "")

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    en_key = f"p{i}_en"
                    bm_key = f"p{i}_bm"
                    
                    # Generates a dynamic cartoon illustration matching your exact chosen character and setting!
                    image_url = f"https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800&auto=format&fit=crop&q=60" 
                    # Alternate query string fallback logic to append customized tags dynamically
                    dynamic_fallback_url = f"https://api.unsplash.com/search/photos?query=cartoon,{char_keyword},{place_keyword}&per_page=1"
                    
                    # For a reliable colorful kid's book feel, we pull live illustration parameters matching the theme:
                    st.image(f"https://loremflickr.com/800/450/cartoon,{char_keyword},{place_keyword}/all", caption=f"{character} di {setting}")
                    
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
            st.error("An execution or formatting error occurred.")
            st.exception(err)
