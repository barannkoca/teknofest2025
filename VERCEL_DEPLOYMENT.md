# 🚀 Vercel Deployment Rehberi - ECOMINDS

Bu rehber, ECOMINDS projenizi Vercel'de deploy etmek için gerekli tüm adımları içerir.

## 📋 Ön Gereksinimler

1. **Vercel Hesabı**: [vercel.com](https://vercel.com) adresinden ücretsiz hesap oluşturun
2. **GitHub Repository**: Projenizi GitHub'a push etmiş olmalısınız
3. **Mapbox Token**: Harita özelliği için Mapbox API token'ı gerekli

## 🔧 Hazırlık Adımları

### 1. Mapbox Token Alma

1. [Mapbox](https://www.mapbox.com/) sitesine gidin
2. Ücretsiz hesap oluşturun
3. Dashboard'dan "Access Token" alın
4. Token'ı not edin (production'da kullanacaksınız)

### 2. Proje Dosyalarını Kontrol Edin

Aşağıdaki dosyaların projenizde mevcut olduğundan emin olun:

```
ECOMINDS/
├── vercel.json                    # ✅ Oluşturuldu
├── .gitignore                     # ✅ Oluşturuldu
├── backend/
│   ├── requirements.txt           # ✅ Oluşturuldu
│   └── api/
│       └── index.py               # ✅ Oluşturuldu
└── frontend/
    ├── vercel.json                # ✅ Oluşturuldu
    └── env.example                # ✅ Oluşturuldu
```

## 🚀 Vercel Deployment Adımları

### Adım 1: Vercel'e Giriş Yapın

1. [vercel.com](https://vercel.com) adresine gidin
2. "Sign Up" ile GitHub hesabınızla giriş yapın
3. Dashboard'a erişin

### Adım 2: Projeyi Import Edin

1. Dashboard'da "New Project" butonuna tıklayın
2. GitHub repository'nizi seçin
3. "Import" butonuna tıklayın

### Adım 3: Build Ayarları

Vercel otomatik olarak proje yapınızı algılayacak, ancak manuel ayarlar yapabilirsiniz:

**Framework Preset**: `Create React App`
**Root Directory**: `/` (proje kökü)
**Build Command**: `cd frontend && npm run build`
**Output Directory**: `frontend/build`

### Adım 4: Environment Variables Ayarlayın

Vercel dashboard'da "Environment Variables" sekmesine gidin ve şunları ekleyin:

```
REACT_APP_MAPBOX_TOKEN = your_mapbox_token_here
REACT_APP_API_URL = https://your-project-name.vercel.app/api
```

**Önemli**: `your_mapbox_token_here` kısmını gerçek Mapbox token'ınızla değiştirin.

### Adım 5: Deploy Edin

1. "Deploy" butonuna tıklayın
2. Build sürecini bekleyin (2-3 dakika)
3. Deployment tamamlandığında URL'nizi alın

## 🔍 Deployment Sonrası Kontroller

### 1. Frontend Kontrolü

- Ana sayfa yükleniyor mu?
- Harita görünüyor mu?
- Sektör arama çalışıyor mu?

### 2. Backend API Kontrolü

Aşağıdaki URL'leri test edin:

```
https://your-project-name.vercel.app/health
https://your-project-name.vercel.app/api/mod1?sector=Teknoloji%20%2F%20Yazılım&topn=5
https://your-project-name.vercel.app/api/mod2?city=İstanbul&topn=5
```

### 3. CORS Ayarları

Backend'de CORS ayarları production için güncellenebilir:

```python
# backend/app/main.py içinde
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-project-name.vercel.app"],  # Sadece kendi domain'iniz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🛠️ Sorun Giderme

### Build Hatası Alıyorsanız

1. **Python Dependencies**: `backend/requirements.txt` dosyasını kontrol edin
2. **Node Dependencies**: `frontend/package.json` dosyasını kontrol edin
3. **Environment Variables**: Tüm gerekli değişkenlerin ayarlandığından emin olun

### API Çalışmıyorsa

1. **Function Timeout**: Vercel'de Python function'ları 10 saniye limiti var
2. **Memory Limit**: Büyük CSV dosyaları için memory limiti aşılabilir
3. **Cold Start**: İlk istek yavaş olabilir

### Harita Görünmüyorsa

1. **Mapbox Token**: Environment variable'ın doğru ayarlandığından emin olun
2. **Domain Restrictions**: Mapbox token'ında domain kısıtlaması olabilir

## 📊 Performance Optimizasyonu

### 1. CSV Dosyalarını Optimize Edin

- Gereksiz kolonları kaldırın
- Veri tiplerini optimize edin
- Dosya boyutlarını küçültün

### 2. Caching Stratejisi

```python
# Backend'de caching ekleyin
from functools import lru_cache

@lru_cache(maxsize=128)
def load_csv_data(filename: str):
    return pd.read_csv(filename)
```

### 3. CDN Kullanımı

- Statik dosyalar için Vercel CDN'i otomatik kullanılır
- Büyük CSV dosyalarını CDN'e taşıyabilirsiniz

## 🔄 Güncelleme Süreci

1. **Kod Değişiklikleri**: GitHub'a push edin
2. **Otomatik Deploy**: Vercel otomatik olarak yeniden deploy eder
3. **Environment Variables**: Dashboard'dan güncelleyin
4. **Domain Ayarları**: Custom domain ekleyebilirsiniz

## 📱 Mobile Optimizasyon

- Responsive tasarım zaten mevcut
- Touch events harita için optimize edilmiş
- PWA özellikleri eklenebilir

## 🔒 Güvenlik

1. **API Rate Limiting**: Vercel'de otomatik rate limiting var
2. **HTTPS**: Tüm trafik otomatik HTTPS
3. **Environment Variables**: Hassas bilgileri environment variables'da saklayın

## 📈 Monitoring

- Vercel Analytics kullanabilirsiniz
- Function logs'ları dashboard'da görülebilir
- Performance metrics takip edilebilir

## 🆘 Destek

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI on Vercel**: [vercel.com/docs/functions/serverless-functions/runtimes/python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- **React on Vercel**: [vercel.com/docs/frameworks/react](https://vercel.com/docs/frameworks/react)

---

**🎉 Tebrikler!** Projeniz artık Vercel'de canlı! 

**URL**: `https://your-project-name.vercel.app`

Herhangi bir sorun yaşarsanız, yukarıdaki sorun giderme bölümünü kontrol edin veya Vercel support'a başvurun.
