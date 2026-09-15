# 💬 WhatsApp Chat Analysis

WhatsApp sohbet geçmişlerini analiz ederek mesajlaşma alışkanlıklarını, kullanıcı aktivitelerini, yoğun saatleri, kullanılan kelimeleri ve emojileri inceleyen **Python + Streamlit** tabanlı bir veri analizi uygulamasıdır.

Proje, WhatsApp sohbet dışa aktarma dosyasını okuyarak ham veriyi yapılandırır ve elde edilen veriler üzerinden farklı analizleri interaktif bir dashboard üzerinde sunar.

---

## 🎯 Projenin Amacı

Bu projenin temel amacı, WhatsApp sohbet verilerini yalnızca mesaj listesi olarak görmek yerine, **veri analizi teknikleri kullanarak anlamlı bilgilere dönüştürmektir.**

Uygulama sayesinde:

* 👥 Katılımcıların mesaj aktiviteleri karşılaştırılabilir.
* ⏰ Sohbetlerin hangi saatlerde yoğunlaştığı görülebilir.
* 📅 Günlük ve aylık mesaj trendleri incelenebilir.
* 📝 En sık kullanılan kelimeler analiz edilebilir.
* 🧠 Sık kullanılan iki kelimelik ifadeler (Bigram) bulunabilir.
* ☁️ Word Cloud oluşturulabilir.
* 😊 En çok kullanılan emojiler analiz edilebilir.
* 📋 İşlenmiş ve ham mesaj verileri incelenebilir.
* 🔥 Katılımcılar için aktivite skoru hesaplanabilir.

---

## 🖥️ Uygulama Sayfaları

### 🏠 Ana Sayfa

WhatsApp sohbet dosyası uygulamaya yüklenir ve temel istatistikler gösterilir.

* Toplam mesaj sayısı
* Katılımcı sayısı
* Toplam kelime sayısı
* Ortalama kelime sayısı
* Sohbetin başlangıç ve bitiş tarihi
* Medya ve silinen mesaj sayıları

---

### 👤 Kullanıcı Analizi

Katılımcıların sohbet içerisindeki aktiviteleri karşılaştırılır.

Mesaj sayısının yanı sıra aşağıdaki metrikler kullanılarak **0–100 arasında Aktivite Skoru** oluşturulur:

| Metrik                 | Ağırlık |
| ---------------------- | ------: |
| Mesaj Sayısı           |     %50 |
| Kelime Sayısı          |     %20 |
| Aktif Gün Sayısı       |     %15 |
| Aktif Saat Çeşitliliği |     %15 |

Her metrik katılımcılar arasında normalize edilir ve ağırlıklı olarak birleştirilir.

---

### ⏰ Zaman Analizi

Mesajların zamansal dağılımı incelenir.

* Saatlere göre mesaj yoğunluğu
* En aktif saat
* Gün × Saat yoğunluk haritası
* Günlük mesaj sayısı
* En aktif gün
* Aylık mesaj trendi
* En yoğun ay

Bu bölüm sayesinde sohbetin hangi zaman dilimlerinde daha aktif olduğu görülebilir.

---

### 📝 Kelime Analizi

Mesaj içerikleri üzerinden metin analizi gerçekleştirilir.

Uygulamada:

* En sık kullanılan kelimeler
* Word Cloud
* Bigram analizi

bulunmaktadır.

Metin temizleme aşamasında URL, sayı ve noktalama işaretleri kaldırılır. Ayrıca yaygın Türkçe stopword'ler filtrelenerek analizde daha anlamlı kelimelerin öne çıkması sağlanır.

---

### 😊 Emoji Analizi

Sohbette kullanılan emojiler analiz edilir.

* En çok kullanılan emojiler
* Emoji kullanım sıklıkları
* Kullanıcı bazında toplam emoji kullanımı
* Her kullanıcının en çok kullandığı 3 emoji

görüntülenebilir.

---

### 📋 Ham Veri

İşlenmiş WhatsApp mesajları tablo halinde incelenebilir.

Ayrıca mesaj uzunluğu analizi ile:

* Ortalama mesaj uzunluğu
* En uzun mesaj
* En kısa mesaj

gösterilir.

---

## ⚙️ Veri İşleme

WhatsApp sohbet dışa aktarma dosyası uygulamaya yüklendikten sonra farklı WhatsApp mesaj formatlarını destekleyen regex ifadeleriyle ayrıştırılır.

Veriler aşağıdaki temel alanlara dönüştürülür:

```text
Tarih
Saat
Kullanıcı
Mesaj
Tur
Düzenlendi
```

Ayrıca analizlerde kullanılmak üzere:

```text
Tarih_DT
Saat_Sayi
```

gibi yardımcı değişkenler oluşturulur.

Uygulama;

* Normal mesajları
* Medya mesajlarını
* Silinen mesajları
* Düzenlenmiş mesajları
* WhatsApp sistem bildirimlerini

birbirinden ayırır.

---

## 🛠️ Kullanılan Teknolojiler

* 🐍 Python
* 📊 Pandas
* 🎨 Streamlit
* ☁️ WordCloud
* 😊 Emoji
* 📈 Matplotlib
* 🔎 Regex

---

## 📁 Proje Yapısı

```text
whatsapp_analiz/
│
├── app.py
├── whatsapp_common.py
│
└── pages/
    ├── 1_Kullanicilar.py
    ├── 2_Zaman_Analizi.py
    ├── 3_Kelime_Analizi.py
    ├── 4_Emoji_Analizi.py
    └── 5_Ham_Veri.py
```

### `app.py`

Uygulamanın ana sayfasıdır. WhatsApp dosyasının yüklenmesi, veri setinin oluşturulması ve temel istatistiklerin gösterilmesinden sorumludur.

### `whatsapp_common.py`

WhatsApp verisinin parse edilmesi ve metin temizleme işlemlerinin ortak olarak yönetildiği modüldür.

### `pages/`

Streamlit'in çok sayfalı uygulama yapısı kullanılarak analiz bölümleri ayrı sayfalara ayrılmıştır.

---

## 🚀 Kurulum

Projeyi bilgisayarınıza klonlayın:

```bash
git clone https://github.com/kullanici-adiniz/whatsapp-analiz.git
```

Proje klasörüne geçin:

```bash
cd whatsapp-analiz
```

Gerekli kütüphaneleri yükleyin:

```bash
pip install streamlit pandas matplotlib wordcloud emoji
```

Uygulamayı çalıştırın:

```bash
streamlit run app.py
```

Ardından tarayıcı üzerinden Streamlit uygulamasını açarak WhatsApp sohbet dosyanızı yükleyebilirsiniz.

---

## 📱 WhatsApp Verisi Nasıl Kullanılır?

WhatsApp içerisinden analiz etmek istediğiniz sohbeti dışa aktarabilirsiniz.

Genellikle:

**Sohbet Bilgisi → Sohbeti Dışa Aktar → Medyasız**

seçeneğiyle elde edilen `.txt` dosyası kullanılabilir.

> 🔒 **Gizlilik:** Sohbet verileri analiz için yerel olarak uygulamaya yüklenir. Projeyi kullanırken kişisel ve hassas verilerinizi GitHub'a yüklememeye dikkat edin.

---

## 📊 Kullanılan Veri Analizi Yaklaşımları

Projede temel veri analizi ve metin madenciliği yaklaşımları birlikte kullanılmıştır.

```text
WhatsApp .txt
     │
     ▼
Veri Okuma
     │
     ▼
Regex ile Parse Etme
     │
     ▼
DataFrame
     │
     ├── Kullanıcı Analizi
     │
     ├── Zaman Analizi
     │
     ├── Kelime Analizi
     │
     ├── Emoji Analizi
     │
     └── Ham Veri
              │
              ▼
       İnteraktif Dashboard
```

---

## 💡 Öne Çıkan Özellikler

* Çok sayfalı Streamlit arayüzü
* Farklı WhatsApp export formatlarını destekleyen parser
* Türkçe stopword filtreleme
* Kelime ve Bigram analizi
* Word Cloud oluşturma
* Emoji analizi
* Kullanıcı bazlı aktivite skoru
* Günlük, aylık ve saatlik analizler
* Ham veri görüntüleme
* Medya ve silinen mesajların ayrı tutulması
* Düzenlenmiş mesajların tespit edilmesi

---

## 📌 Gelecekte Eklenebilecek Özellikler

* 📈 Daha gelişmiş istatistiksel analizler
* 🔍 Kullanıcı bazlı kelime analizi
* 😊 Duygu analizi
* 📊 Daha gelişmiş interaktif grafikler
* 📤 Analiz sonuçlarını PDF/Excel olarak dışa aktarma
* 🗂️ Birden fazla sohbetin karşılaştırılması
* 🔎 Gelişmiş filtreleme ve arama
* 🌙 Dark/Light tema desteği

---

## 👩‍💻 Geliştirici

**Sakine Cansu Topci**

Yönetim Bilişim Sistemleri mezunu | Data Analytics

Bu proje, Python ile veri analizi, metin işleme ve Streamlit kullanarak interaktif veri uygulamaları geliştirme pratiği amacıyla hazırlanmıştır.

---

⭐ Projeyi beğendiyseniz repository'ye yıldız bırakabilirsiniz!
