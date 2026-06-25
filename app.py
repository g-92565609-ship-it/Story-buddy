import streamlit as st
from gtts import gTTS

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
    with st.spinner("✨ Writing your custom storybook..."):
        try:
            # Clean split strings to separate English and Malay text completely
            char_bm = character.split(" (")[0]
            char_en = character.split(" (")[1].replace(")", "")
            
            place_bm = setting.split(" (")[0]
            place_en = setting.split(" (")[1].replace(")", "")
            
            emo_bm = emotion.split(" (")[0]
            emo_en = emotion.split(" (")[1].replace(")", "")
            
            # --- PAGE 1 GENERATION ---
            p1_en = f"Once upon a time, a lovely young creature lived peacefully near the edge of a wonderful kingdom. This beautiful soul was known to everyone as the most energetic {char_en} in the entire land. One bright morning, an unexpected adventure began to unfold, leading directly toward the legendary destination known as the {place_en}. Moving forward step by step, a spectacular feeling started growing inside, making the traveler feel incredibly {emo_en.lower()} about what lay ahead. The journey was filled with tall green trees, wide open horizons, and endless possibilities waiting to be uncovered."
            p1_bm = f"Pada zaman dahulu, seekor makhluk yang sangat comel tinggal dengan aman di pinggir sebuah kerajaan yang indah. Makhluk ini dikenali oleh semua orang sebagai {char_bm} yang paling bertenaga di seluruh kawasan tersebut. Pada suatu pagi yang cerah, sebuah pengembaraan yang tidak dijangka mula berlaku, membawa terus ke destinasi legenda yang dikenali sebagai {place_bm}. Bergerak selangkah demi selangkah, perasaan yang luar biasa mula berkembang di dalam jiwa, menjadikan pengembara itu merasa sangat {emo_bm.lower()} tentang apa yang ada di hadapan. Perjalanan itu dipenuhi dengan pokok hijau yang tinggi."

            # --- PAGE 2 GENERATION ---
            p2_en = f"As the path continued deeper into the heart of the {place_en}, many surprising discoveries began to appear along the road. The brave {char_en} noticed glowing light patterns dancing gracefully through the heavy air, illuminating hidden trails that nobody had ever explored before. Every single corner turned brought a brand new wave of wonder, reinforcing that deep, undeniable sense of feeling so {emo_en.lower()}. A mysterious old map found resting under a smooth stone revealed that the true prize was not gold, but the wonderful wisdom gained from exploring this magnificent world."
            p2_bm = f"Apabila laluan berterusan lebih dalam ke jantung {place_bm}, banyak penemuan yang mengejutkan mula muncul di sepanjang jalan tersebut. {char_bm} yang berani melihat corak cahaya yang bersinar menari dengan anggun melintasi udara, menerangi laluan tersembunyi yang tidak pernah diterokai oleh sesiapa pun sebelum ini. Setiap sudut yang dilalui membawa gelombang keajaiban yang baharu, mengukuhkan lagi rasa {emo_bm.lower()} yang mendalam. Satu peta lama misteri yang ditemui di bawah batu licin mendedahkan bahawa hadiah sebenar bukanlah emas."

            # --- PAGE 3 GENERATION ---
            p3_en = f"Finally, reaching the absolute highest point of the {place_en} brought the magnificent quest to its perfect conclusion. Looking out across the vast, breathtaking landscape, the proud {char_en} realized that true strength comes from deep within your own heart. Standing tall and proud, the memory of being so wonderfully {emo_en.lower()} during this challenge would remain a guiding light forever. With a joyful smile and a soft sigh of ultimate satisfaction, our little hero promised to return for another grand adventure very soon. The brilliant day ended beautifully under a sky filled with bright twinkling stars."
            p3_bm = f"Akhirnya, mencapai titik tertinggi mutlak di {place_bm} membawa pencarian yang hebat ini kepada kesimpulan yang sangat sempurna. Memandang ke luar merentasi landskap yang luas dan menakjubkan, {char_bm} yang bangga menyedari bahawa kekuatan sebenar datang dari lubuk hati sendiri. Berdiri tinggi dengan penuh rasa bangga, kenangan menjadi sangat {emo_bm.lower()} semasa cabaran ini akan kekal menjadi cahaya panduan selama-lamanya. Dengan senyuman gembira dan keluhan puas, wira kecil kami berjanji untuk kembali tidak lama lagi."

            pages = {
                "p1_en": p1_en, "p1_bm": p1_bm,
                "p2_en": p2_en, "p2_bm": p2_bm,
                "p3_en": p3_en, "p3_bm": p3_bm
            }

            st.header("✨ Buku Cerita Digital Kamu / Your Digital Storybook")
            tabs = st.tabs(["Muka Surat 1", "Muka Surat 2", "Muka Surat 3"])

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    en_key = f"p{i}_en"
                    bm_key = f"p{i}_bm"
                    
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
            st.error("An error occurred.")
            st.exception(err)
