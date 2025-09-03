# 🌍 ECOMINDS - Yatırım Karar Destek Sistemi

Bu proje, Türkiye'nin 81 ili ve 19 farklı sektör için yatırım karar destek analizi sağlayan bir web uygulamasıdır.

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

## 🚀 Kurulum ve Çalıştırma

### Ön Gereksinimler

- Python 3.9+
- Node.js 16+
- npm veya yarn

### 🛠️ Makefile ile Kolay Kurulum (Önerilen)

Proje kök dizininde aşağıdaki komutları kullanabilirsiniz:

```bash
# 📋 Tüm komutları göster
make help

# 🔧 İlk kurulum - gerekli paketleri yükle
make setup

# 🚀 Hem backend hem frontend'i başlat (paralel)
make start

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
