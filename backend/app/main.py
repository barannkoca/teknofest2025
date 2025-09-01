"""
main.py
- FastAPI giriş noktası
- Mod-1 (Sektör → İl) ve Mod-2 (İl → Sektör) endpoint'leri
- Healthcheck ve cache reload yardımcı uçları
"""

from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from .schemas import (
    HealthResponse,
    Mod1Response,
    Mod2Response,
    ScoreEntry,
)
from .loader import (
    load_dataframes,
    invalidate_cache,
)
from .scoring import (
    score_all_cities,
    score_all_sectors,
    score_sector_for_city,
    sort_top_n,
)
from .explain import build_reasons_from_contributions

APP_VERSION = "1.0.0"

app = FastAPI(
    title="Yatırım Karar Destek API",
    version=APP_VERSION,
    description="81 il × 20 sektör için açıklanabilir skorlar ve kısa gerekçeler.",
)

# ---- CORS (geliştirme için serbest, prod'da alanları daralt) ---------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prod: ["https://senin-frontend-domainin.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- CSV dosya yolları ------------------------------------------------------

CSV_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TOP5_ILLER_PER_SEKTOR_CSV = os.path.join(CSV_DIR, "Top5_Iller_Per_Sektor.csv")
TOP5_SEKTORLER_PER_IL_CSV = os.path.join(CSV_DIR, "Top5_Sektorler_Per_Il.csv")

# ---- CSV veri yükleme fonksiyonları ----------------------------------------

def load_top5_iller_per_sektor() -> pd.DataFrame:
    """Top5_Iller_Per_Sektor.csv dosyasını yükler"""
    try:
        df = pd.read_csv(TOP5_ILLER_PER_SEKTOR_CSV)
        return df
    except Exception as e:
        print(f"Top5_Iller_Per_Sektor.csv yükleme hatası: {e}")
        return pd.DataFrame()

def load_top5_sektorler_per_il() -> pd.DataFrame:
    """Top5_Sektorler_Per_Il.csv dosyasını yükler"""
    try:
        df = pd.read_csv(TOP5_SEKTORLER_PER_IL_CSV)
        return df
    except Exception as e:
        print(f"Top5_Sektorler_Per_Il.csv yükleme hatası: {e}")
        return pd.DataFrame()

def get_top5_cities_for_sector(sector: str) -> List[ScoreEntry]:
    """Belirli bir sektör için top5 şehirleri CSV'den çeker"""
    try:
        df = load_top5_iller_per_sektor()
        if df.empty:
            print(f"CSV dosyası boş veya yüklenemedi")
            return []
        
        # Sektör adını normalize et (büyük/küçük harf duyarsız)
        # Önce tam eşleşme dene
        sector_data = df[df['Sektor'] == sector]
        
        # Tam eşleşme yoksa kısmi eşleşme dene
        if sector_data.empty:
            sector_data = df[df['Sektor'].str.contains(sector, case=False, na=False)]
        
        if sector_data.empty:
            print(f"'{sector}' sektörü CSV'de bulunamadı")
            return []
        
        # Top5'i al ve ScoreEntry listesine dönüştür
        top5_entries = []
        for _, row in sector_data.head(5).iterrows():
            try:
                top5_entries.append(
                    ScoreEntry(
                        name=str(row['Sehir']),
                        score=round(float(row['Skor']), 1),
                        reasons=[f"{row['Sehir']} bu sektörde {row['Skor']:.1f} puan ile {row['Sira']}. sırada"]
                    )
                )
            except Exception as e:
                print(f"Satır işlenirken hata: {e}, satır: {row}")
                continue
        
        print(f"'{sector}' sektörü için {len(top5_entries)} şehir bulundu")
        return top5_entries
        
    except Exception as e:
        print(f"get_top5_cities_for_sector hatası: {e}")
        return []

def get_top5_sectors_for_city(city: str) -> List[ScoreEntry]:
    """Belirli bir şehir için top5 sektörleri CSV'den çeker"""
    try:
        df = load_top5_sektorler_per_il()
        if df.empty:
            print(f"CSV dosyası boş veya yüklenemedi")
            return []
        
        # Şehir adını normalize et (büyük/küçük harf duyarsız)
        # Önce tam eşleşme dene
        city_data = df[df['Sehir'] == city]
        
        # Tam eşleşme yoksa kısmi eşleşme dene
        if city_data.empty:
            city_data = df[df['Sehir'].str.contains(city, case=False, na=False)]
        
        if city_data.empty:
            print(f"'{city}' şehri CSV'de bulunamadı")
            return []
        
        # Top5'i al ve ScoreEntry listesine dönüştür
        top5_entries = []
        for _, row in city_data.head(5).iterrows():
            try:
                top5_entries.append(
                    ScoreEntry(
                        name=str(row['Sektor']),
                        score=round(float(row['Skor']), 1),
                        reasons=[f"{row['Sektor']} sektöründe {row['Skor']:.1f} puan ile {row['Sira']}. sırada"]
                    )
                )
            except Exception as e:
                print(f"Satır işlenirken hata: {e}, satır: {row}")
                continue
        
        print(f"'{city}' şehri için {len(top5_entries)} sektör bulundu")
        return top5_entries
        
    except Exception as e:
        print(f"get_top5_sectors_for_city hatası: {e}")
        return []

# ---- Yaşam döngüsü ---------------------------------------------------------

@app.on_event("startup")
def _startup() -> None:
    # CSV dosyalarını kullandığımız için Excel yükleme yapmıyoruz
    print("[INFO] CSV tabanlı API hazır - Excel dosyası yüklenmedi")

# ---- Yardımcılar -----------------------------------------------------------

def _round_scores(d: Dict[str, float], ndigits: int = 1) -> Dict[str, float]:
    return {k: round(float(v), ndigits) for k, v in d.items()}

# ---- Endpoint'ler ----------------------------------------------------------

@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(version=APP_VERSION)

@app.post("/api/reload", tags=["system"])
def reload_data() -> Dict[str, str]:
    """
    CSV dosyaları güncellendiğinde yeniden yüklemek için.
    """
    try:
        # CSV dosyaları her istekte yeniden yüklendiği için cache temizlemeye gerek yok
        return {"status": "ok", "message": "CSV dosyaları her istekte yeniden okunuyor."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yeniden yükleme hatası: {e}")

@app.get("/api/mod1", response_model=Mod1Response, tags=["scoring"])
def mod1_sector_to_cities(
    sector: str = Query(..., description="Sektör adı (ör. 'Turizm / Otelcilik')"),
    topn: int = Query(5, ge=1, le=20, description="Top-N il sayısı"),
):
    """
    Mod-1: Seçili sektör için CSV'den top şehirleri getir.
    """
    try:
        # CSV'den direkt oku
        top_entries = get_top5_cities_for_sector(sector)
        
        if not top_entries:
            raise HTTPException(status_code=404, detail=f"'{sector}' sektörü için veri bulunamadı")
        
        # Sadece istenen sayıda döndür
        top_entries = top_entries[:topn]
        
        # scoresByCity dictionary'sini oluştur (geriye uyumluluk için)
        scores_by_city = {entry.name: entry.score for entry in top_entries}
        
        return Mod1Response(
            sector=sector,
            scoresByCity=scores_by_city,
            top5=top_entries,
            legend=None,  # CSV'den okurken legend gerekmiyor
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Veri okuma hatası: {e}")

@app.get("/api/mod2", response_model=Mod2Response, tags=["scoring"])
def mod2_city_to_sectors(
    city: str = Query(..., description="İl adı (ör. 'İzmir')"),
    topn: int = Query(5, ge=1, le=20, description="Top-N sektör sayısı"),
):
    """
    Mod-2: Seçili il için CSV'den top sektörleri getir.
    """
    try:
        # CSV'den direkt oku
        top_entries = get_top5_sectors_for_city(city)
        
        if not top_entries:
            raise HTTPException(status_code=404, detail=f"'{city}' şehri için veri bulunamadı")
        
        # Sadece istenen sayıda döndür
        top_entries = top_entries[:topn]
        
        # scoresBySector dictionary'sini oluştur (geriye uyumluluk için)
        scores_by_sector = {entry.name: entry.score for entry in top_entries}
        
        return Mod2Response(
            city=city,
            scoresBySector=scores_by_sector,
            top5=top_entries,
            legend=None,  # CSV'den okurken legend gerekmiyor
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Veri okuma hatası: {e}")