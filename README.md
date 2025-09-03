# 🌍 ECOMINDS - Yatırım Karar Destek Sistemi

Projemiz, Türkiye’nin 81 ilini resmi istatistiklerle analiz ederek yatırımcılara “Hangi ilde hangi sektöre yatırım yapılmalı?” sorusuna veriye dayalı ve görsel bir çözüm sunan akıllı bir karar destek sistemidir.
Sistem iki farklı modda çalışır:
Mod 1 (Sektör → İl): Kullanıcı bir sektör seçer ve sistem o alanda yatırım için en uygun 5 ili sıralar.
Mod 2 (İl → Sektör): Kullanıcı bir il seçer ve sistem o şehirde öne çıkan 5 yatırım sektörünü önerir.
Her iki modda da sonuçlar yalnızca liste olarak değil; kısa gerekçeler ve Türkiye haritası üzerinde görsel gösterimler ile desteklenir.

## 📁 Proje Yapısı 

```
ECOMINDS/
├── backend/                 # FastAPI Backend
│   ├── app/                # Backend uygulama kodları
│   ├── data/               # CSV veri dosyaları
│   └── venv/               # Python virtual environment
└── frontend/               # React Frontend
    ├── src/                # Frontend kaynak kodları
    └── public/             # Statik dosyalar
```


## Tüm verilerimizi TÜİK üzerinden elde ettik.
## ÖNEMLİ: Tüm veri analizi,matematik,veri işleme,normalizasyon gibi işlemlerimizin hepsini excelden yaptık. (Pythondaki tüm fonksiyonlar, Excel'de matematiksel ve başka türlü işlemler kullanılarak yapılabildiği için Excel kullandık.)
## TÜİK üzerinden çektiğimiz tablolardaki tüm verilerimize derin bir veri analizi ve matematiksel işlemler yaparak her ilin verisini karşılaştırmaya hazır hale getirdik. (Burada yeni veriler de elde ettik.)
## Sonrasında iller arası adil bir kaşılaştırma yapabilmek amacıyla çıkan her değeri kendi ilinin nüfusuna böldük. Mesela Aydın ilinde 100 kişi olsun ve 100 hastane yatağı olsun, aynı zamanda İzmir ilinde 400 kişi olsun ama 300 hasta yatağı olsun dersek; bu durumda asta yatağı Aydın'da daha az olmasına rağmen İzmir'e yatırım yapmalıyız. Çünkü kişi başına daha az düşüyor.
## Bu işlemlerden sonra tüm verilerimize normalizasyon işlemi uyguladık.
### Kullandığımız TÜİK Tablolarının her birisinin isimleri şunlardır:
- İkamet edilen il ve doğum yerine göre nüfus
- İllere Göre Tarım Alanları
- İllere Göre İhracat
- İllere Göre İthalat
- Sağlık Personeli Sayılarının İlere göre Dağılımı
- İlere Göre Belediye Hizmetlerinden Hasta ve Yoksullara Yardım, Yeşil Alanların Miktarı ve Engellere Yönelik Düzenleme Hizmetlerinden Memnuniyet
- Göç etme nedeni ve cinsiyete göre iller arası göç eden nüfus ve oranı
- Hastane Sayılarının İllere Göre Dağılımı
- İllere göre bitirilen eğitim durumu(6+yas)
- Bitirilen Eğitim durumu ve cinsiyete göre nüfus_15+
- İl düzeyinde istihdam oranı
- İllere Göre Konut Satış Sayıları
- İllere ve ikamet edilen konutta ısınma amacıyla en çok kullanılan ana yakıt türüne göre hanehalkı sayısı ve oranı
- İllere Göre Belediye Hizmetlerinden Çöp ve Çevresel Atık Toplama, Kanalizasyon, Şebeke Suyu ve Toplu Taşıma Hizmetlerinden Memnuniyet
- İllere ve Cinsiyete Göre Ortanca Yaş
- İllere Göre Annenin Ortalama Yaşı
- Göç etme nedenine göre illerin verdiği göç
- Göç etme nedenine göre illerin aldığı göç
- Göç etme nedenine göre iller arası göç eden nüfus ve oranı
- İl düzeyinde işgücüne katılma oranı


## 🚀 Kurulum ve Çalıştırma

### Ön Gereksinimler

- Python 3.9+
- Node.js 16+
- npm veya yarn
- **🗺️ Mapbox API Token** (Harita görselleştirme için)

### 🔑 Mapbox Token Kurulumu

Frontend'in harita özelliğini kullanabilmek için Mapbox token'ı gerekli:

1. [Mapbox](https://www.mapbox.com/) sitesinden ücretsiz hesap oluşturun
2. Access Token alın
3. `frontend/` klasöründe `.env` dosyası oluşturun:

```bash
cd frontend
echo "REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here" > .env
```

**⚠️ Önemli:** `.env` dosyasını Git'e commit etmeyin (`.gitignore`'da olmalı)

### 🛠️ Makefile ile Kolay Kurulum (Önerilen)

Proje kök dizininde aşağıdaki komutları kullanabilirsiniz:

```bash
# 📋 Tüm komutları göster
make help

# 🔧 İlk kurulum - gerekli paketleri yükle
make setup

# 🚀 Hem backend hem frontend'i başlat (paralel)
make start

# 🔑 Mapbox token kontrolü
make check-mapbox
```

# ⚡ Portları temizle ve başlat
make quick-start

# 📊 Servislerin durumunu kontrol et
make status

# 🧪 API endpoint'lerini test et
make test

# ⏹️ Çalışan servisleri durdur
make stop

# 🧹 Geçici dosyaları temizle
make clean

# 🔄 Tam reset (node_modules'u da sil)
make reset
```

### 📚 Detaylı Makefile Komutları

| Komut | Açıklama |
|-------|----------|
| `make help` | 📋 Kullanılabilir komutları göster |
| `make setup` | 🔧 İlk kurulum - gerekli paketleri yükle |
| `make start` | 🚀 Hem backend hem frontend'i başlat (paralel) |
| `make start-backend` | 🔧 Sadece backend'i başlat |
| `make start-frontend` | ⚛️ Sadece frontend'i başlat |
| `make dev` | 🛠️ Geliştirme modu (alias for start) |
| `make stop` | ⏹️ Çalışan servisleri durdur |
| `make test` | 🧪 API endpoint'lerini test et |
| `make test-quick` | ⚡ Hızlı health check |
| `make status` | 📊 Servislerin durumunu kontrol et |
| `make clean` | 🧹 Geçici dosyaları temizle |
| `make reset` | 🔄 Tam reset - node_modules'u da sil |
| `make ports` | 🔍 Kullanılan portları göster |
| `make kill-ports` | ⚔️ 8000 ve 3000 portlarındaki işlemleri öldür |
| `make quick-start` | ⚡ Portları temizle ve başlat |
| `make info` | ℹ️ Proje bilgileri |
| `make validate` | ✅ Proje yapısını doğrula |
| `make check-mapbox` | 🔑 Mapbox token varlığını kontrol et |

### 1️⃣ Manuel Backend Kurulumu

```bash
# Proje klasörüne git
cd ECOMINDS/backend

# Virtual environment'ı aktif et
source venv/bin/activate

# Gerekli paketler zaten yüklü, direkt başlat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend http://localhost:8000 adresinde çalışacak

### 2️⃣ Manuel Frontend Kurulumu

Yeni bir terminal açın:

```bash
# Frontend klasörüne git
cd ECOMINDS/frontend

# Gerekli paketleri yükle (ilk kurulumda)
npm install

# Frontend'i başlat
npm start
```

✅ Frontend http://localhost:3000 adresinde çalışacak

## 🎯 Kullanım

### Ana Özellikler

1. **🗺️ Türkiye Haritası**: İllere tıklayarak o ilin en iyi 5 sektörünü görün
2. **🔍 Sektör Analizi**: Bir sektör seçerek o sektörde en başarılı 5 şehri keşfedin

### Sektörler

- Turizm / Otelcilik
- Teknoloji / Yazılım  
- Sanayi / Üretim
- Tarım ve Hayvancılık
- Sağlık
- Enerji
- Konut & İnşaat
- Lojistik
- Perakende
- Eğitim Kurumları
- Gıda İşleme
- Finans
- Otomotiv
- Mobilya
- Telekom
- Çevre / Atık
- Sosyal Hizmetler
- Kültür & Sanat
- Ulaşım

## 🔧 API Endpoints

### Backend API'si

- **Health Check**: `GET /health`
- **Sektör → Şehirler**: `GET /api/mod1?sector={sector_name}&topn=5`
- **Şehir → Sektörler**: `GET /api/mod2?city={city_name}&topn=5`

### Örnek API Kullanımı

```bash
# Teknoloji sektöründe en iyi şehirler
curl "http://localhost:8000/api/mod1?sector=Teknoloji%20%2F%20Yazılım&topn=5"

# İstanbul'un en iyi sektörleri
curl "http://localhost:8000/api/mod2?city=İstanbul&topn=5"
```

## 📊 Veri Kaynakları

Proje aşağıdaki CSV dosyalarından veri okur:

- `backend/data/Top5_Iller_Per_Sektor.csv` - Sektör bazlı en iyi şehirler
- `backend/data/Top5_Sektorler_Per_Il.csv` - Şehir bazlı en iyi sektörler

## 🛠️ Teknoloji Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Veri işleme
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI framework
- **TypeScript** - Tip güvenliği
- **Mapbox GL JS** - Harita görselleştirme

## 🚨 Sorun Giderme

### 🛠️ Makefile ile Sorun Giderme (Önerilen)

```bash
# 📊 Servis durumunu kontrol et
make status

# ⚔️ Port çakışması varsa portları temizle
make kill-ports

# 🔄 Tam reset yap
make reset
make setup

# ⚡ Portları temizle ve yeniden başlat
make quick-start
```

### Backend Başlamazsa
```bash
# Virtual environment'ı kontrol et
cd backend
source venv/bin/activate
which python  # /Users/.../ECOMINDS/backend/venv/bin/python olmalı

# Veya Makefile ile:
make start-backend
```

### Frontend Başlamazsa
```bash
# Node modules'u yeniden yükle
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start

# Veya Makefile ile:
make reset
make setup
make start-frontend
```

### Port Çakışması
```bash
# Makefile ile portları temizle
make kill-ports

# Veya manuel olarak:
# Backend için: --port 8001 ekleyin
# Frontend için: farklı port otomatik önerilecek
```

## 📱 Geliştirme Notları

- Backend her değişiklikte otomatik yeniden başlar (`--reload`)
- Frontend hot reload destekler
- CSV dosyaları her API çağrısında yeniden okunur
- CORS tüm originlere açık (geliştirme için)

## 👥 Takım

Bu proje yatırım karar destek sistemi için geliştirilmiştir.

## 💡 Makefile Kullanım İpuçları

### 🚀 Hızlı Başlangıç
```bash
# İlk kez çalıştırıyorsanız:
make setup    # Paketleri yükle
make start    # Uygulamayı başlat

# Günlük kullanım:
make start    # Uygulamayı başlat
make stop     # Uygulamayı durdur
make status   # Durumu kontrol et
```

### 🔧 Geliştirici Komutları
```bash
make test        # API'leri test et
make clean       # Cache temizle
make logs-backend # Backend loglarını izle
make info        # Proje bilgilerini göster
make check-mapbox # Mapbox token kontrolü
```

### 🆘 Acil Durum Komutları
```bash
make kill-ports  # Port çakışması çöz
make reset       # Tam temizlik
make quick-start # Hızlı yeniden başlat
```

---

**🎉 Başarılı kurulum için her iki servisin de (backend:8000, frontend:3000) çalıştığından emin olun!**

**💡 İpucu: `make help` komutu ile tüm kullanılabilir komutları görebilirsiniz!**
