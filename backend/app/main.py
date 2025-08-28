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

# ---- Yaşam döngüsü ---------------------------------------------------------

@app.on_event("startup")
def _startup() -> None:
    # İlk istekten önce veriyi yükleyip doğrula
    try:
        load_dataframes(force_reload=False)
    except Exception as e:
        # Yükleme hatası uygulamayı düşürmesin; ilk istekte yine denenir
        print(f"[WARN] Veri yükleme başlangıçta başarısız: {e}")

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
    Excel dosyaları güncellendiğinde cache'i sıfırlamak için.
    """
    try:
        invalidate_cache()
        load_dataframes(force_reload=True)
        return {"status": "ok", "message": "Veri yeniden yüklendi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yeniden yükleme hatası: {e}")

@app.get("/api/mod1", response_model=Mod1Response, tags=["scoring"])
def mod1_sector_to_cities(
    sector: str = Query(..., description="Sektör adı (ör. 'Turizm')"),
    topn: int = Query(5, ge=1, le=20, description="Top-N il sayısı"),
):
    """
    Mod-1: Seçili sektör için 81 ilin puanlarını hesapla, Top-N liste ve kısa gerekçelerle döndür.
    """
    try:
        scores_by_city, legend = score_all_cities(sector)
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hesaplama hatası: {e}")

    # Top-N
    top_pairs = sort_top_n(scores_by_city, n=topn)

    top_entries: List[ScoreEntry] = []
    for city, _score in top_pairs:
        # Her Top-N satırı için katkılardan gerekçe üret
        try:
            score_value, contribs = score_sector_for_city(city, sector, return_contributions=True)
        except KeyError:
            # City/sector bulunamadıysa atla (olası değil)
            continue
        reasons = build_reasons_from_contributions(contribs, top_k_pos=2, include_risk=True)
        top_entries.append(
            ScoreEntry(
                name=city,
                score=round(score_value, 1),
                reasons=reasons,
            )
        )

    return Mod1Response(
        sector=sector,
        scoresByCity=_round_scores(scores_by_city, ndigits=1),
        top5=top_entries,
        legend=legend,
    )

@app.get("/api/mod2", response_model=Mod2Response, tags=["scoring"])
def mod2_city_to_sectors(
    city: str = Query(..., description="İl adı (ör. 'İzmir')"),
    topn: int = Query(5, ge=1, le=20, description="Top-N sektör sayısı"),
):
    """
    Mod-2: Seçili il için 20 sektörün puanlarını hesapla, Top-N liste ve kısa gerekçelerle döndür.
    """
    try:
        scores_by_sector, legend = score_all_sectors(city)
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hesaplama hatası: {e}")

    # Top-N
    top_pairs = sort_top_n(scores_by_sector, n=topn)

    top_entries: List[ScoreEntry] = []
    for sector, _score in top_pairs:
        try:
            score_value, contribs = score_sector_for_city(city, sector, return_contributions=True)
        except KeyError:
            continue
        reasons = build_reasons_from_contributions(contribs, top_k_pos=2, include_risk=True)
        top_entries.append(
            ScoreEntry(
                name=sector,
                score=round(score_value, 1),
                reasons=reasons,
            )
        )

    return Mod2Response(
        city=city,
        scoresBySector=_round_scores(scores_by_sector, ndigits=1),
        top5=top_entries,
        legend=legend,
    )