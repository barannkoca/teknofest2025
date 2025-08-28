"""
schemas.py
- FastAPI istek/yanıt şemaları
- Loader/Scoring katmanları için yardımcı veri modelleri
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple
from pydantic import BaseModel, Field, ConfigDict

# ---- Genel tipler ----------------------------------------------------------

WeightDirection = Literal["YUKSEK", "DUSUK"]  # kriter yönü

ScoreDict = Dict[str, float]  # {"İzmir": 60.6, "Antalya": 78.3, ...} veya {"Turizm": 60.6, ...}
LegendBreaks = List[float]    # [0, 20, 40, 60, 80, 100] gibi

# ---- Loader için satır modelleri -------------------------------------------

class SectorCriterion(BaseModel):
    """
    Sektor_Kriter_Agirlik.xlsx satırı temsili:
    - Sektor: "Turizm", "Lojistik", ...
    - KriterKey: Iller_Normalize.xlsx'deki kolon anahtarı (örn. 'KonutSatis...BOLUNUFUS')
    - Agirlik: 0–100 arasında, aynı sektör içinde toplamları = 100
    - Yon: 'YUKSEK' (yüksek iyi) | 'DUSUK' (düşük iyi)
    """
    model_config = ConfigDict(extra="forbid")

    Sektor: str = Field(..., description="Sektör adı")
    KriterKey: str = Field(..., description="Normalize veri setindeki kolon adı")
    Agirlik: float = Field(..., ge=0, le=100, description="Ağırlık (yüzde)")
    Yon: WeightDirection = Field(..., description="Yön: YUKSEK | DUSUK")


class CityFeatures(BaseModel):
    """
    Iller_Normalize.xlsx’ten bir ilin tüm özellikleri (sadece sayısal kolonlar dahil).
    Örnek alanlar loader tarafından dinamik işlenir; burada tip sözleşmesi amaçlıdır.
    """
    model_config = ConfigDict(extra="allow")  # kolonlar dinamik geldiği için allow
    Sehir: str = Field(..., description="İl adı (kanonik)")

# ---- Skorlama & açıklama yardımcıları --------------------------------------

class Contribution(BaseModel):
    """
    Bir kriterin skora katkısını açıklama için taşır.
    """
    model_config = ConfigDict(extra="forbid")

    kriter: str = Field(..., description="Kriter anahtarı")
    katkı: float = Field(..., description="0–1 bandında katkı (ağırlık uyg.).")
    yon: WeightDirection = Field(..., description="Kriter yönü")
    agirlik: float = Field(..., ge=0, le=100, description="Kriter ağırlığı (yüzde)")
    ham_deger: float = Field(..., ge=0, le=1, description="Normalize ham değer (0–1)")

# ---- API yanıt listeleri ---------------------------------------------------

class ScoreEntry(BaseModel):
    """
    Tablo/Top-5 satırı.
    """
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="İl veya sektör adı")
    score: float = Field(..., ge=0, le=100, description="0–100 puan")
    reasons: List[str] = Field(default_factory=list, description="Kısa gerekçe rozetleri (+, ⚠)")

class Mod1Response(BaseModel):
    """
    Mod-1: Sektör → İl
    """
    model_config = ConfigDict(extra="forbid")

    sector: str
    scoresByCity: ScoreDict
    top5: List[ScoreEntry]
    legend: Optional[LegendBreaks] = None  # choropleth eşiği (opsiyonel)

class Mod2Response(BaseModel):
    """
    Mod-2: İl → Sektör
    """
    model_config = ConfigDict(extra="forbid")

    city: str
    scoresBySector: ScoreDict
    top5: List[ScoreEntry]
    legend: Optional[LegendBreaks] = None

# ---- Sağlık/teknik uçlar için küçük modeller -------------------------------

class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    backend: str = "fastapi"
    version: str = "1.0.0"

# ---- İsteğe bağlı: Body alanı kullanmak istersen ---------------------------

class SectorRequest(BaseModel):
    """
    Eğer query param yerine body ile sektör almak istersen (opsiyonel kullanım).
    """
    model_config = ConfigDict(extra="forbid")

    sector: str = Field(..., description="Sektör adı")

class CityRequest(BaseModel):
    """
    Eğer query param yerine body ile il almak istersen (opsiyonel kullanım).
    """
    model_config = ConfigDict(extra="forbid")

    city: str = Field(..., description="İl adı")

__all__ = [
    "WeightDirection",
    "ScoreDict",
    "LegendBreaks",
    "SectorCriterion",
    "CityFeatures",
    "Contribution",
    "ScoreEntry",
    "Mod1Response",
    "Mod2Response",
    "HealthResponse",
    "SectorRequest",
    "CityRequest",
]