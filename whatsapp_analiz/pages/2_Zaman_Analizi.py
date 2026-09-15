import streamlit as st

st.set_page_config(page_title="Zaman Analizi", page_icon="⏰", layout="wide")

if "df_real" not in st.session_state:

    st.warning(
        "Önce ana sayfadan bir WhatsApp sohbet dosyası yükleyin."
    )

    st.stop()

df_real = st.session_state["df_real"]

st.title("⏰ Zaman Analizi")

# ============================================================
# SAAT ANALİZİ
# ============================================================

st.subheader("Konuşma Saatleri")

hour_counts = (
    df_real["Saat_Sayi"]
    .dropna()
    .astype(int)
    .value_counts()
    .sort_index()
)

hour_counts.index = [f"{hour:02d}:00" for hour in hour_counts.index]

st.bar_chart(hour_counts)

if not hour_counts.empty:

    busiest_hour = hour_counts.idxmax()

    st.info(f"🔥 En aktif saat: **{busiest_hour}**")


# ============================================================
# GÜN x SAAT HEATMAP
# ============================================================

st.subheader("🗓️ Gün x Saat Yoğunluk Haritası")

TURKISH_DAYS = [
    "Pazartesi", "Salı", "Çarşamba", "Perşembe",
    "Cuma", "Cumartesi", "Pazar"
]

heatmap_df = df_real.dropna(subset=["Tarih_DT", "Saat_Sayi"]).copy()

if not heatmap_df.empty:

    heatmap_df["Gün"] = heatmap_df["Tarih_DT"].dt.dayofweek.map(
        dict(enumerate(TURKISH_DAYS))
    )

    heatmap_table = (
        heatmap_df
        .groupby(["Gün", "Saat_Sayi"])
        .size()
        .unstack(fill_value=0)
        .reindex(TURKISH_DAYS)
        .reindex(columns=range(24), fill_value=0)
    )

    heatmap_table.columns = [f"{h:02d}" for h in heatmap_table.columns]

    st.dataframe(
        heatmap_table.style.background_gradient(
            cmap="YlOrRd", axis=None
        ).format(precision=0),
        width=1000
    )

else:

    st.warning("Heatmap için tarih/saat verisi yetersiz.")


# ============================================================
# GÜNLERE GÖRE MESAJ ANALİZİ
# ============================================================

st.divider()

st.subheader("📅 Günlere Göre Mesaj Sayısı")

if df_real["Tarih_DT"].notna().any():

    daily_counts = (
        df_real.dropna(subset=["Tarih_DT"])
        .groupby("Tarih_DT")
        .size()
    )

    st.line_chart(daily_counts)

    busiest_day = daily_counts.idxmax()

    st.info(
        f"🔥 En aktif gün: **{busiest_day.strftime('%d.%m.%Y')}** "
        f"({daily_counts.max():,} mesaj)"
    )

    # --------------------------------------------------------
    # AYLIK TREND
    # --------------------------------------------------------

    st.markdown("**📆 Aylık Mesaj Sayısı**")

    monthly_counts = (
        df_real.dropna(subset=["Tarih_DT"])
        .groupby(df_real["Tarih_DT"].dt.to_period("M"))
        .size()
    )

    monthly_counts.index = monthly_counts.index.strftime("%m.%Y")

    st.bar_chart(monthly_counts)

    busiest_month = monthly_counts.idxmax()

    st.info(
        f"🔥 En yoğun ay: **{busiest_month}** "
        f"({monthly_counts.max():,} mesaj)"
    )
