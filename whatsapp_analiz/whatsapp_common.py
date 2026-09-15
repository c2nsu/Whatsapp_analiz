"""
Tüm sayfaların ortak kullandığı WhatsApp parse ve metin temizleme
mantığı. Bu modül burada tek bir yerde tutulur ki her sayfa aynı
kuralları uygulasın (regex'ler, stopwords, vs. tekrar tekrar
kopyalanmasın).
"""

import re
from collections import Counter

import pandas as pd


# ============================================================
# WHATSAPP SİSTEM/PLACEHOLDER METİNLERİ
# ============================================================
# Bunlar gerçek mesaj içeriği değil, istatistikleri kirletmesin diye
# ayrı tutuyoruz.

MEDIA_PATTERN = re.compile(
    r"‎?(GIF|belge|görüntü|ses|video|sticker|çıkartma|fotoğraf) dahil edilmedi",
    flags=re.IGNORECASE
)
DELETED_PATTERN = re.compile(r"‎?Bu mesajı? sildiniz\.?|‎?Bu mesaj silindi\.?")
EDITED_TAG_PATTERN = re.compile(r"\s*‎?<Bu mesaj düzenlendi>\s*$")
SYSTEM_PATTERN = re.compile(
    r"‎?Mesajlar ve aramalar uçtan uca şifrelidir"
)

# Türkçe yaygın kelimeler (kelime/bigram analizinde filtrelenir)
STOPWORDS = {
    "ve", "veya", "bir", "bu", "şu", "o",
    "da", "de", "ta", "te",
    "için", "ile", "ama", "fakat",
    "çok", "daha", "en",
    "ben", "sen", "biz", "siz",
    "ne", "mi", "mı", "mu", "mü",
    "ki", "ya", "hem",
    "var", "yok",
    "olan", "olarak",
    "diye", "gibi",
    "şey", "şeyi",
    "benim", "senin",
    "bana", "sana",
    "onun", "bunu",
    "nasıl", "neden",
    "hangi", "her",
    "şimdi", "zaten",
    "evet", "hayır"
}


def read_lines(source):

    # source bir dosya yolu ya da Streamlit'in file_uploader'dan
    # döndürdüğü yüklenmiş dosya nesnesi olabilir.
    if hasattr(source, "getvalue"):

        raw_bytes = source.getvalue()

        text = raw_bytes.decode("utf-8-sig")

        return text.splitlines()

    with open(source, "r", encoding="utf-8-sig") as file:

        return file.readlines()


def parse_whatsapp_chat(lines):

    # Farklı WhatsApp dışa aktarma formatlarını destekle
    patterns = [

        # 09.09.2026, 14:32 - Cansu: Merhaba
        re.compile(
            r"^(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}),?\s+"
            r"(\d{1,2}:\d{2}(?::\d{2})?)\s+-\s+"
            r"([^:]+):\s?(.*)$"
        ),

        # 09.09.2026 14:32 - Cansu: Merhaba
        re.compile(
            r"^(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\s+"
            r"(\d{1,2}:\d{2}(?::\d{2})?)\s+-\s+"
            r"([^:]+):\s?(.*)$"
        ),

        # [09.09.2026, 14:32:10] Cansu: Merhaba
        re.compile(
            r"^\[(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}),?\s+"
            r"(\d{1,2}:\d{2}(?::\d{2})?)\]\s+"
            r"([^:]+):\s?(.*)$"
        ),

        # [09.09.2026 14:32] Cansu: Merhaba
        re.compile(
            r"^\[(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\s+"
            r"(\d{1,2}:\d{2}(?::\d{2})?)\]\s+"
            r"([^:]+):\s?(.*)$"
        )
    ]

    messages = []

    for line in lines:

        line = line.rstrip("\n\r")

        # WhatsApp bazı sistem/medya satırlarının BAŞINA görünmez bir
        # "left-to-right mark" (\u200e) karakteri koyuyor. Bu karakter
        # orada kaldığında "^\[" ile başlayan regex'ler satırı hiç
        # yakalayamıyor ve satır yanlışlıkla önceki mesajın devamı
        # sanılıp ona ekleniyor.
        line = line.lstrip("\u200e\u200f\ufeff")

        matched = False

        for pattern in patterns:

            match = pattern.match(line)

            if match:

                date = match.group(1)
                time = match.group(2)
                user = match.group(3).strip()
                message = match.group(4).strip()

                # WhatsApp, düzenlenen mesajların SONUNA "<Bu mesaj
                # düzenlendi>" etiketini ekliyor (ayrı bir satır değil).
                duzenlendi = bool(EDITED_TAG_PATTERN.search(message))
                message = EDITED_TAG_PATTERN.sub("", message).strip()

                if SYSTEM_PATTERN.search(message):
                    # Grup/sohbet sistem bildirimi, kullanıcı mesajı değil
                    matched = True
                    break

                if MEDIA_PATTERN.search(message):
                    tur = "medya"
                elif DELETED_PATTERN.search(message):
                    tur = "silindi"
                else:
                    tur = "mesaj"

                messages.append({
                    "Tarih": date,
                    "Saat": time,
                    "Kullanıcı": user,
                    "Mesaj": message,
                    "Tur": tur,
                    "Düzenlendi": duzenlendi
                })

                matched = True
                break

        # Yeni mesaj değilse önceki mesajın devamı olabilir
        if not matched and messages and line.strip():

            messages[-1]["Mesaj"] += " " + line.strip()

    df = pd.DataFrame(messages)

    if not df.empty:

        df["Tarih_DT"] = pd.to_datetime(
            df["Tarih"],
            dayfirst=True,
            errors="coerce"
        )

        df["Saat_Sayi"] = pd.to_numeric(
            df["Saat"].str[:2],
            errors="coerce"
        )

    return df


def clean_text(text):

    text = text.lower()

    # URL'leri kaldır
    text = re.sub(r"http\S+|www\S+", "", text)

    # Sayıları kaldır
    text = re.sub(r"\d+", "", text)

    # Noktalama işaretlerini kaldır
    text = re.sub(
        r"[^\w\sçğıöşüİĞÜŞÖÇ]", " ", text, flags=re.UNICODE
    )

    words = text.split()

    return [
        word
        for word in words
        if len(word) > 2 and word not in STOPWORDS
    ]


def word_counts_from(messages):

    counter = Counter()

    for message in messages:

        counter.update(clean_text(str(message)))

    return counter
