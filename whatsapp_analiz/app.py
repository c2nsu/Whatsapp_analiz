import streamlit as st

from whatsapp_common import read_lines, parse_whatsapp_chat

# ============================================================
# SAYFA AYARLARI
# ============================================================

st.set_page_config(
    page_title="WhatsApp Sohbet Analizi",
    page_icon="💬",
    layout="wide"
)

st.title("💬 WhatsApp Sohbet Analizi")
st.caption("WhatsApp sohbet verilerini veri bilimi ile analiz et")

# ============================================================
# DOSYA YÜKLEME
# ============================================================

uploaded_file = st.file_uploader(
    "📂 WhatsApp sohbet dosyanızı yükleyin (.txt)",
    type="txt"
)

if uploaded_file is None:

    st.info(
        "Analiz için bir WhatsApp sohbet dışa aktarma dosyası (.txt) "
        "yükleyin. Yükledikten sonra soldaki menüden diğer analiz "
        "sayfalarına geçebilirsiniz."
    )

    st.stop()

# ============================================================
# VERİYİ OKU VE İŞLE
# ============================================================
# Not: Bu işlem sadece burada, ana sayfada yapılır. Sonuç
# st.session_state'e yazılır ki pages/ altındaki diğer sayfalar
# dosyayı yeniden okumak/parse etmek zorunda kalmasın ve hepsi
# aynı veri üzerinde çalışsın.

try:

    lines = read_lines(uploaded_file)

    df = parse_whatsapp_chat(lines)

except UnicodeDecodeError:

    st.error("❌ Dosya UTF-8 formatında okunamadı.")

    st.stop()

except Exception as e:

    st.error(f"❌ Dosya okunurken hata oluştu: {e}")

    st.stop()

if df.empty:

    st.error("❌ Sohbet dosyası okundu ancak mesaj bulunamadı.")

    st.warning(
        "WhatsApp sohbet formatı kullandığımız formatlardan farklı olabilir."
    )

    st.stop()

df_real = df[df["Tur"] == "mesaj"].copy()
df_media = df[df["Tur"] == "medya"]
df_deleted = df[df["Tur"] == "silindi"]

# Diğer sayfaların kullanması için session_state'e yaz
st.session_state["df"] = df
st.session_state["df_real"] = df_real
st.session_state["df_media"] = df_media
st.session_state["df_deleted"] = df_deleted
st.session_state["dosya_adi"] = uploaded_file.name

# ============================================================
# TEMEL İSTATİSTİKLER
# ============================================================

total_messages = len(df_real)
total_users = df_real["Kullanıcı"].nunique()

total_words = df_real["Mesaj"].str.split().str.len().sum()
average_words = df_real["Mesaj"].str.split().str.len().mean()

total_media = len(df_media)
total_deleted = len(df_deleted)

st.success(
    f"✅ **{uploaded_file.name}** başarıyla analiz edildi! "
    f"{total_messages:,} mesaj bulundu."
)

if total_media or total_deleted:

    st.caption(
        f"ℹ️ Ayrıca {total_media:,} medya paylaşımı ve "
        f"{total_deleted:,} silinen mesaj tespit edildi "
        f"(istatistiklere dahil edilmedi)."
    )

st.info(
    "👈 Soldaki menüden **Kullanıcılar**, **Zaman Analizi**, "
    "**Kelime Analizi**, **Emoji Analizi** ve **Ham Veri** "
    "sayfalarına geçebilirsiniz."
)

# ============================================================
# GENEL ÖZET METRİKLERİ
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric("💬 Toplam Mesaj", f"{total_messages:,}")

with col2:

    st.metric("👥 Katılımcı", total_users)

with col3:

    st.metric("📝 Toplam Kelime", f"{int(total_words):,}")

with col4:

    st.metric("📊 Ort. Kelime", f"{average_words:.1f}")

if df_real["Tarih_DT"].notna().any():

    gun_sayisi = (
        df_real["Tarih_DT"].max() - df_real["Tarih_DT"].min()
    ).days + 1

    st.caption(
        f"🗓️ Konuşma süresi: **{gun_sayisi} gün** "
        f"({df_real['Tarih_DT'].min().strftime('%d.%m.%Y')} — "
        f"{df_real['Tarih_DT'].max().strftime('%d.%m.%Y')})"
    )
