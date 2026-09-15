from collections import Counter

import pandas as pd
import streamlit as st

from whatsapp_common import clean_text

st.set_page_config(page_title="Kelime Analizi", page_icon="📝", layout="wide")

if "df_real" not in st.session_state:

    st.warning(
        "Önce ana sayfadan bir WhatsApp sohbet dosyası yükleyin."
    )

    st.stop()

df_real = st.session_state["df_real"]

st.title("📝 Kelime Analizi")

all_words = []

for message in df_real["Mesaj"]:

    all_words.extend(clean_text(str(message)))

word_counts = Counter(all_words)

# ============================================================
# EN SIK KULLANILAN KELİMELER
# ============================================================

st.subheader("En Sık Kullanılan Kelimeler")

top_words = pd.DataFrame(
    word_counts.most_common(20),
    columns=["Kelime", "Kullanım"]
)

if not top_words.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(top_words.set_index("Kelime"))

    with col2:

        st.dataframe(top_words, width=350, hide_index=True)

else:

    st.warning("Kelime analizi için yeterli metin bulunamadı.")


# ============================================================
# WORD CLOUD
# ============================================================

st.subheader("☁️ Word Cloud")

if word_counts:

    try:

        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        wc = WordCloud(
            width=1000,
            height=450,
            background_color="white",
            colormap="viridis",
            max_words=150
        ).generate_from_frequencies(word_counts)

        fig, ax = plt.subplots(figsize=(10, 4.5))

        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")

        st.pyplot(fig)

    except ImportError:

        st.info(
            "Word cloud için `wordcloud` paketi gerekli: "
            "`pip install wordcloud`"
        )

else:

    st.warning("Word cloud için yeterli metin bulunamadı.")


# ============================================================
# BİGRAM ANALİZİ
# ============================================================

st.divider()

st.subheader("🧠 Sık Kullanılan Kelime Öbekleri (Bigram)")

st.caption(
    "Aynı mesaj içinde art arda gelen iki kelimelik öbekler — tek "
    "kelime analizinden daha anlamlı kalıpları ortaya çıkarır."
)

bigram_counter = Counter()

for message in df_real["Mesaj"]:

    words = clean_text(str(message))

    for i in range(len(words) - 1):

        bigram_counter[f"{words[i]} {words[i + 1]}"] += 1

top_bigrams = pd.DataFrame(
    bigram_counter.most_common(15),
    columns=["Kelime Öbeği", "Kullanım"]
)

if not top_bigrams.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(top_bigrams.set_index("Kelime Öbeği"))

    with col2:

        st.dataframe(top_bigrams, width=350, hide_index=True)

else:

    st.warning("Bigram analizi için yeterli metin bulunamadı.")
