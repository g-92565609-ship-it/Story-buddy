import streamlit as st
from openai import OpenAI
from gtts import gTTS
import os

# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "YOUR_FALLBACK_API_KEY"))

def generate_cartoon_illustration(story_text):
    """Generates a child-friendly cartoon image based on the page text."""
    try:
        prompt = f"A vibrant, child-friendly digital cartoon illustration for a children's book. Watercolor style, simple friendly shapes, bright colors. Scene description: {story_text}"
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        # Directly return the web URL string from the response object
        return response.data[0].url
    except Exception as e:
        # This will print the exact hidden error to your Streamlit logs so you can see it!
        print(f"DALL-E Generation Error: {e}")
        return None

# Your existing configuration line
st.set_page_config(page_title="Sahabat Cerita AI", page_icon="📖", layout="wide")

# App Styling for Primary Students
st.title("📖 Sahabat Cerita AI / AI Story Buddy")
st.write("Cipta cerita pengembaraan kamu sendiri! / Create your own adventure story!")



# 1. THE INTERACTIVE INPUT ZONE (Emoji Buttons)
st.header("🎨 Pilih Elemen Cerita / Choose Story Elements")

col1, col2, col3 = st.columns(3)

with col1:
    character = st.selectbox(
        "🐱 Pilih Watak / Choose Character",
        ["Kucing Comel (Cute Cat)", "Angkasawan Berani (Brave Astronaut)", "Naga Kecil (Little Dragon)", "Arnab Bijak (Clever Rabbit)"]
    )

with col2:
    setting = st.selectbox(
        "🚀 Pilih Tempat / Choose Setting",
        ["Pulau Harta Karun (Treasure Island)", "Hutan Ajaib (Magical Forest)", "Planet Marikh (Mars)", "Istana Awan (Cloud Castle)"]
    )

with col3:
    emotion = st.selectbox(
        "😊 Pilih Emosi / Choose Emotion",
        ["Gembira (Happy)", "Teruja (Excited)", "Misteri (Mysterious)"]
    )

# 2. GENERATION TRIGGER
if st.button("🚀 Bina Cerita Saya! / Generate My Story!", type="primary"):
    
    # System prompt forces the model to strictly return the requested format
    system_instruction = (
        "You are a primary school teacher specialized in bilingual English and Bahasa Melayu education. "
        "Create a simple, engaging, moral story for children aged 7-10 based on user selections. "
        "The story must have exactly 3 short pages/paragraphs. "
        "Format your entire response strictly as follows so it can be parsed easily:\n"
        "Page 1 EN: [English text]\nPage 1 BM: [Bahasa Melayu translation]\n"
        "Page 2 EN: [English text]\nPage 2 BM: [Bahasa Melayu translation]\n"
        "Page 3 EN: [English text]\nPage 3 BM: [Bahasa Melayu translation]\n"
        "Keep sentences structurally simple, encouraging vocabulary alignment."
    )
    
    user_prompt = f"Character: {character}. Setting: {setting}. Mood/Emotion: {emotion}."
    
    with st.spinner("Peri AI sedang menulis cerita kamu... 🪄"):
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Cost-effective and highly reliable for language structural matching
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            raw_story = response.choices[0].message.content
            
            # Parse the structured response into visual pages
            lines = raw_story.split("\n")
            pages = {}
            for line in lines:
                if "Page 1 EN:" in line: pages['p1_en'] = line.replace("Page 1 EN:", "").strip()
                if "Page 1 BM:" in line: pages['p1_bm'] = line.replace("Page 1 BM:", "").strip()
                if "Page 2 EN:" in line: pages['p2_en'] = line.replace("Page 2 EN:", "").strip()
                if "Page 2 BM:" in line: pages['p2_bm'] = line.replace("Page 2 BM:", "").strip()
                if "Page 3 EN:" in line: pages['p3_en'] = line.replace("Page 3 EN:", "").strip()
                if "Page 3 BM:" in line: pages['p3_bm'] = line.replace("Page 3 BM:", "").strip()

# # 3. INTERACTIVE BILINGUAL DISPLAY ZONE
            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")

            # Tabbed interface mimicking turning pages
            tab1, tab2, tab3 = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            with tab1:
                # 1. Illustration
                if 'p1_en' in pages:
                    try:
                        prompt = f"A vibrant, child-friendly digital cartoon illustration for a children's book. Watercolor style, simple friendly shapes, bright colors. Scene description: {pages['p1_en']}"
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=prompt,
                            n=1,
                            size="1024x1024"
                        )
                        image_url = response.data[0].url
                        st.image(image_url, use_container_width=True, caption="AI Illustrated Scene")
                    except Exception as img_err:
                        st.error(f"⚠️ DALL-E Error on Page 1:")
                        st.exception(img_err)

                # 2. English Text Block & Audio
                if 'p1_en' in pages:
                    st.subheader("🇬🇧 English")
                    st.info(pages['p1_en'])
                    tts_en = gTTS(text=pages['p1_en'], lang='en')
                    tts_en.save("p1_en.mp3")
                    st.audio("p1_en.mp3", format="audio/mp3")

                # 3. Bahasa Melayu Text Block & Audio
                if 'p1_bm' in pages:
                    st.subheader("🇲🇾 Bahasa Melayu")
                    st.success(pages['p1_bm'])
                    tts_ms = gTTS(text=pages['p1_bm'], lang='ms')
                    tts_ms.save("p1_ms.mp3")
                    st.audio("p1_ms.mp3", format="audio/mp3")


            with tab2:
                # 1. Illustration
                if 'p2_en' in pages:
                    try:
                        prompt = f"A vibrant, child-friendly digital cartoon illustration for a children's book. Watercolor style, simple friendly shapes, bright colors. Scene description: {pages['p2_en']}"
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=prompt,
                            n=1,
                            size="1024x1024"
                        )
                        image_url = response.data[0].url
                        st.image(image_url, use_container_width=True, caption="AI Illustrated Scene")
                    except Exception as img_err:
                        st.error(f"⚠️ DALL-E Error on Page 2:")
                        st.exception(img_err)

                # 2. English Text Block & Audio
                if 'p2_en' in pages:
                    st.subheader("🇬🇧 English")
                    st.info(pages['p2_en'])
                    tts_en = gTTS(text=pages['p2_en'], lang='en')
                    tts_en.save("p2_en.mp3")
                    st.audio("p2_en.mp3", format="audio/mp3")

                # 3. Bahasa Melayu Text Block & Audio
                if 'p2_bm' in pages:
                    st.subheader("🇲🇾 Bahasa Melayu")
                    st.success(pages['p2_bm'])
                    tts_ms = gTTS(text=pages['p2_bm'], lang='ms')
                    tts_ms.save("p2_ms.mp3")
                    st.audio("p2_ms.mp3", format="audio/mp3")


            with tab3:
                # 1. Illustration
                if 'p3_en' in pages:
                    try:
                        prompt = f"A vibrant, child-friendly digital cartoon illustration for a children's book. Watercolor style, simple friendly shapes, bright colors. Scene description: {pages['p3_en']}"
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=prompt,
                            n=1,
                            size="1024x1024"
                        )
                        image_url = response.data[0].url
                        st.image(image_url, use_container_width=True, caption="AI Illustrated Scene")
                    except Exception as img_err:
                        st.error(f"⚠️ DALL-E Error on Page 3:")
                        st.exception(img_err)

                # 2. English Text Block & Audio
                if 'p3_en' in pages:
                    st.subheader("🇬🇧 English")
                    st.info(pages['p3_en'])
                    tts_en = gTTS(text=pages['p3_en'], lang='en')
                    tts_en.save("p3_en.mp3")
                    st.audio("p3_en.mp3", format="audio/mp3")

                # 3. Bahasa Melayu Text Block & Audio
                if 'p3_bm' in pages:
                    st.subheader("🇲🇾 Bahasa Melayu")
                    st.success(pages['p3_bm'])
                    tts_ms = gTTS(text=pages['p3_bm'], lang='ms')
                    tts_ms.save("p3_ms.mp3")
                    st.audio("p3_ms.mp3", format="audio/mp3")