import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kullanıcı Analizi", page_icon="👤", layout="wide")

if "df_real" not in st.session_state:

    st.warning(
        "Önce ana sayfadan bir WhatsApp sohbet dosyası yükleyin."
    )

    st.stop()

df_real = st.session_state["df_real"]

st.title("👤 Kullanıcı Analizi")

# ============================================================
# MESAJ SAYISI
# ============================================================

user_counts = (
    df_real["Kullanıcı"]
    .value_counts()
    .reset_index()
)

user_counts.columns = ["Kullanıcı", "Mesaj Sayısı"]

col1, col2 = st.columns(2)

with col1:

    st.bar_chart(user_counts.set_index("Kullanıcı"))

with col2:

    st.dataframe(user_counts, width=350, hide_index=True)


# ============================================================
# AKTİVİTE SKORU (feature engineering)
# ============================================================

st.divider()

st.subheader("🔥 Aktivite Skoru")

st.caption(
    "Mesaj sayısı (%50) + kelime sayısı (%20) + aktif gün sayısı (%15) "
    "+ aktif saat çeşitliliği (%15) — her metrik katılımcılar arasında "
    "0-100 aralığına ölçeklenip ağırlıklı toplanır."
)

activity_df = df_real.groupby("Kullanıcı").agg(
    Mesaj_Sayısı=("Mesaj", "count"),
    Kelime_Sayısı=("Mesaj", lambda s: s.str.split().str.len().sum()),
    Aktif_Gün=("Tarih_DT", lambda s: s.dt.date.nunique()),
    Aktif_Saat=("Saat_Sayi", lambda s: s.dropna().nunique())
).reset_index()


def normalize_0_100(col):

    if col.max() == col.min():
        return pd.Series([100.0] * len(col), index=col.index)

    return (col - col.min()) / (col.max() - col.min()) * 100


activity_df["Skor"] = (
    normalize_0_100(activity_df["Mesaj_Sayısı"]) * 0.50
    + normalize_0_100(activity_df["Kelime_Sayısı"]) * 0.20
    + normalize_0_100(activity_df["Aktif_Gün"]) * 0.15
    + normalize_0_100(activity_df["Aktif_Saat"]) * 0.15
).round(1)

activity_df = activity_df.sort_values(
    "Skor", ascending=False
).reset_index(drop=True)

medals = ["🥇", "🥈", "🥉"]

for i, row in activity_df.iterrows():

    medal = medals[i] if i < len(medals) else f"{i + 1}."

    st.write(f"{medal} **{row['Kullanıcı']}** — {row['Skor']}")

st.dataframe(activity_df, width=700, hide_index=True)
