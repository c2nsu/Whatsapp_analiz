from collections import Counter

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Emoji Analizi", page_icon="😊", layout="wide")

if "df_real" not in st.session_state:

    st.warning(
        "Önce ana sayfadan bir WhatsApp sohbet dosyası yükleyin."
    )

    st.stop()

df_real = st.session_state["df_real"].copy()

st.title("😊 Emoji Analizi")

try:

    import emoji

    def extract_emojis(text):

        return [item["emoji"] for item in emoji.emoji_list(str(text))]

    df_real["Emojiler"] = df_real["Mesaj"].apply(extract_emojis)

    all_emojis = [
        e
        for emoji_list in df_real["Emojiler"]
        for e in emoji_list
    ]

    emoji_counts = Counter(all_emojis)

    if emoji_counts:

        top_emojis = pd.DataFrame(
            emoji_counts.most_common(15),
            columns=["Emoji", "Kullanım"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.bar_chart(top_emojis.set_index("Emoji"))

        with col2:

            st.dataframe(top_emojis, width=350, hide_index=True)

        st.markdown("**👤 Kullanıcı Bazında Emoji Kullanımı**")

        user_emoji_rows = []

        for user, group in df_real.groupby("Kullanıcı"):

            user_emojis = [
                e
                for emoji_list in group["Emojiler"]
                for e in emoji_list
            ]

            if user_emojis:

                user_counter = Counter(user_emojis)

                top3 = user_counter.most_common(3)

                top3_text = "  ".join(
                    f"{symbol} ×{count}"
                    for symbol, count in top3
                )

                user_emoji_rows.append({
                    "Kullanıcı": user,
                    "Toplam Emoji": len(user_emojis),
                    "En Çok Kullandığı 3 Emoji": top3_text
                })

        user_emoji_df = pd.DataFrame(user_emoji_rows).sort_values(
            "Toplam Emoji", ascending=False
        )

        st.dataframe(user_emoji_df, width=700, hide_index=True)

    else:

        st.warning("Sohbette emoji bulunamadı.")

except ImportError:

    st.info(
        "Emoji analizi için `emoji` paketi gerekli: "
        "`pip install emoji`"
    )
