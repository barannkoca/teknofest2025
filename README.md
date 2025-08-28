# ECOMINDS - Teknofest 2025

Eco-friendly business scoring API - İl ve sektör bazlı karar destek sistemi.

## Proje Açıklaması

ECOMINDS, 81 ili 14 normalize gösterge ile 20 sektör açısından sayısal olarak puanlayan ve iki yönlü öneri veren bir karar destek sistemidir.

### Özellikler

- **Mod-1 (Sektör → İl)**: Bir sektör seçildiğinde 81 ilin o sektör için puanını hesaplar ve en iyi 5 ili sıralar
- **Mod-2 (İl → Sektör)**: Bir il seçildiğinde 20 sektörün o il için puanını hesaplar ve en iyi 5 sektörü sıralar
- **YÖN dönüşümü**: Her kriter için "Yüksek" veya "Düşük" avantaj kuralları
- **Ağırlıklı skorlama**: Sektöre özel kriter ağırlıkları ile hesaplama

## Teknolojiler

- **Backend**: FastAPI (Python)
- **Veri İşleme**: Pandas, NumPy
- **Veri Kaynağı**: Excel dosyaları (TÜİK tabanlı göstergeler)

## Kurulum

```bash
# Repository'yi klonla
git clone https://github.com/yourusername/teknofest2025.git
cd teknofest2025

# Backend klasörüne geç
cd backend

# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Gerekli paketleri yükle
pip install fastapi uvicorn pandas openpyxl numpy

# Uygulamayı çalıştır
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /` - Ana sayfa
- `GET /health` - Sağlık kontrolü
- `GET /sectors` - Sektör listesi
- `GET /cities` - İl listesi
- `POST /rank/cities-for-sector` - Sektör için il sıralaması
- `POST /rank/sectors-for-city` - İl için sektör sıralaması
- `GET /scores/matrix` - Tüm skor matrisi

## Skor Hesaplama Mantığı

1. **YÖN uygulaması**:
   - Yüksek avantaj: `katkı = değer`
   - Düşük avantaj: `katkı = 1 - değer`

2. **Ağırlıklı toplam**:
   - `Skor = Σ (katkı_kriter × ağırlık_kriter / 100)`

3. **Final skor**: 0-1 arasından 0-100'e çevrilir

## Örnek Kullanım

```python
# İzmir - Turizm skoru hesaplama
score, contributions = calculate_sector_score_for_city("İzmir", "Turizm / Otelcilik", iller_df, sektor_df)
print(f"İzmir - Turizm skoru: {score:.1f}/100")

# Tüm iller için Turizm skorları
all_scores = calculate_all_cities_for_sector("Turizm / Otelcilik", iller_df, sektor_df)
```

## Proje Yapısı

```
ECOMINDS/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI giriş
│   │   ├── config.py            # Dosya yolları, sabitler
│   │   ├── loader.py            # Excel okuma & doğrulama
│   │   ├── scoring.py           # YÖN dönüşümü + ağırlıklı skor motoru
│   │   ├── explain.py           # Kısa gerekçe üretimi
│   │   ├── schemas.py           # Pydantic modelleri
│   │   ├── calculateScore.py    # Skor hesaplama modülü
│   │   └── test_scoring.py      # Test modülü
│   ├── data/
│   │   ├── Iller_Normalize.xlsx
│   │   └── Sektor_Kriter_Agirlik.xlsx
│   └── venv/
└── frontend/                    # (Gelecekte eklenecek)
```

## Lisans

Bu proje Teknofest 2025 yarışması için geliştirilmiştir.

## İletişim

- Proje: ECOMINDS
- Yarışma: Teknofest 2025
