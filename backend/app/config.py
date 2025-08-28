"""
config.py
- Dosya yolları, sabitler ve şehir adı normalize yardımcıları
"""

from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path
from typing import Dict

# ---- Yol/Sabitler ---------------------------------------------------------

# Bu dosyanın bulunduğu klasör: backend/app/
APP_DIR = Path(__file__).resolve().parent
# Proje kökü: backend/
ROOT_DIR = APP_DIR.parent
# Veri klasörü: backend/data/
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT_DIR / "data")).resolve()

# Excel kaynakları
ILLER_FILE = Path(os.getenv("ILLER_FILE", DATA_DIR / "Iller_Normalize.xlsx")).resolve()
SEKTOR_FILE = Path(os.getenv("SEKTOR_FILE", DATA_DIR / "Sektor_Kriter_Agirlik.xlsx")).resolve()

# Puan ölçeği
SCORE_SCALE_MAX: float = 100.0

# Opsiyonel: Dataframe'leri RAM'de tutmak istersen loader içinde kullan
CACHE_DATAFRAMES: bool = True

# ---- Şehir adı normalize yardımcıları -------------------------------------

def strip_diacritics(text: str) -> str:
    """
    Türkçe karakterleri koruyarak 'anahtar' üretmek yerine,
    tüm aksanları kaldırıp ascii-benzeri sade bir anahtar üretir.
    Örn: 'İzmir' -> 'izmir', 'Şanlıurfa' -> 'sanliurfa'
    """
    nfkd = unicodedata.normalize("NFKD", text)
    without_marks = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    return without_marks

def normalize_city_key(text: str) -> str:
    """
    Şehir adını eşleştirmede kullanılacak anahtar:
    - baş/son boşluklar kırpılır
    - aksanlar kaldırılır
    - küçük harfe çevrilir
    - birden fazla whitespace tek boşluğa indirilir
    - tire/altçizgi noktalamaları boşluk olarak değerlendirilir
    """
    t = strip_diacritics(text or "").lower().strip()
    t = re.sub(r"[-_./]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t

# Sık karşılaşılan eşanlamlar/söylenişler → GeoJSON/Excel'deki kanonik isim
CITY_SYNONYMS: Dict[str, str] = {
    # Anadolu’daki yaygın kısaltma/alternatifler
    "afyon": "Afyonkarahisar",
    "sanliurfa": "Şanlıurfa",
    "urfa": "Şanlıurfa",
    "gaziantep": "Gaziantep",
    "gazi antep": "Gaziantep",
    "eskisehir": "Eskişehir",
    "mugla": "Muğla",
    "canakkale": "Çanakkale",
    "balikesir": "Balıkesir",
    "kucukcekmece": "İstanbul",  # ilçe adı girilirse il'e toplanmak istenirse örnek
    # Büyükşehirler (aksan/İ-i farkları)
    "istanbul": "İstanbul",
    "izmir": "İzmir",
    "ankara": "Ankara",
    # Antakya eskiden Hatay şehir adıyla karışabiliyor
    "antakya": "Hatay",
}

def canonicalize_city_name(name: str) -> str:
    """
    Excel ve GeoJSON il isimlerini eşlemek için kanonik isim döndürür.
    - Önce sözlükte eşleşme arar
    - Bulamazsa orijinali kırpıp geri verir (eşleşme loader tarafında raporlanır)
    """
    key = normalize_city_key(name)
    if key in CITY_SYNONYMS:
        return CITY_SYNONYMS[key]
    return (name or "").strip()

__all__ = [
    "APP_DIR",
    "ROOT_DIR",
    "DATA_DIR",
    "ILLER_FILE",
    "SEKTOR_FILE",
    "SCORE_SCALE_MAX",
    "CACHE_DATAFRAMES",
    "strip_diacritics",
    "normalize_city_key",
    "canonicalize_city_name",
    "CITY_SYNONYMS",
]