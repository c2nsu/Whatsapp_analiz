import streamlit as st

st.set_page_config(page_title="Ham Veri", page_icon="📋", layout="wide")

if "df_real" not in st.session_state:

    st.warning(
        "Önce ana sayfadan bir WhatsApp sohbet dosyası yükleyin."
    )

    st.stop()

df = st.session_state["df"]
df_real = st.session_state["df_real"].copy()

st.title("📋 Mesaj Uzunluğu ve Ham Veri")

# ============================================================
# MESAJ UZUNLUĞU
# ============================================================

st.subheader("📏 Mesaj Uzunluğu Analizi")

df_real["Kelime_Sayısı"] = df_real["Mesaj"].str.split().str.len()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric("Ortalama", f"{df_real['Kelime_Sayısı'].mean():.1f} kelime")

with col2:

    st.metric("En Uzun", f"{df_real['Kelime_Sayısı'].max()} kelime")

with col3:

    st.metric("En Kısa", f"{df_real['Kelime_Sayısı'].min()} kelime")


# ============================================================
# HAM VERİ
# ============================================================

st.divider()

st.subheader("Mesaj Verileri")

display_df = df[
    ["Tarih", "Saat", "Kullanıcı", "Mesaj", "Tur", "Düzenlendi"]
]

st.dataframe(display_df, width=1000, height=500, hide_index=True)
