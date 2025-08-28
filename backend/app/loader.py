"""
loader.py
- Excel kaynaklarını okur
- Şema & kalite doğrulamaları yapar
- Şehir isimlerini kanonikleştirir
- Sektör kriterlerini ve şehir feature'larını kullanıma hazır verir
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from .config import (
    ILLER_FILE,
    SEKTOR_FILE,
    CACHE_DATAFRAMES,
    canonicalize_city_name,
)

# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

EPS = 1e-6

# Module-level cache
_CITIES_DF: pd.DataFrame | None = None
_CRITERIA_DF: pd.DataFrame | None = None
_FEATURE_COLS: List[str] | None = None
_SECTOR_LIST: List[str] | None = None
_CITY_LIST: List[str] | None = None

# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DataShapes:
    n_cities: int
    n_features: int
    n_criteria_rows: int
    n_sectors: int


def _read_excel_safe(path) -> pd.DataFrame:
    try:
        df = pd.read_excel(path)
        if df.empty:
            raise ValueError(f"Excel boş: {path}")
        return df
    except Exception as e:
        raise RuntimeError(f"Excel okuma hatası ({path}): {e}") from e


def _validate_and_prepare_cities(df_cities_raw: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Beklenen minimum kolon: 'Sehir' + (normalize edilmiş 0–1 metrik kolonları)
    - Sehir'i kanonik hale getir
    - Tüm diğer kolonları sayısal yap
    - 0–1 bandı dışında varsa hata ver
    - Sehir tekrarları varsa hata ver
    """
    if "Sehir" not in df_cities_raw.columns:
        raise ValueError("Iller_Normalize.xlsx içinde 'Sehir' kolonu bulunamadı.")

    df = df_cities_raw.copy()

    # Orijinali sakla (debug için faydalı)
    df["Sehir_Original"] = df["Sehir"].astype(str)
    df["Sehir"] = df["Sehir"].astype(str).map(canonicalize_city_name)

    # Şehir tekrarı var mı?
    dup = df.duplicated(subset=["Sehir"])
    if dup.any():
        dups = df.loc[dup, "Sehir"].unique().tolist()
        raise ValueError(f"Aynı il birden fazla satırda görünüyor: {dups}")

    # Feature kolonları: Sehir ve Sehir_Original dışındaki tüm sayısal kolonlar
    ignore_cols = {"Sehir", "Sehir_Original"}
    num_cols: List[str] = []
    for c in df.columns:
        if c in ignore_cols:
            continue
        # sayısala zorla (metin gelirse NaN olacaktır)
        df[c] = pd.to_numeric(df[c], errors="coerce")
        num_cols.append(c)

    # NaN kontrol
    if df[num_cols].isna().any().any():
        na_cells = df[num_cols].isna().sum().sum()
        raise ValueError(f"Iller_Normalize.xlsx içinde sayısal olmayan/NaN hücreler var (adet={na_cells}). Lütfen temizleyin.")

    # 0–1 bandı kontrolü
    min_all = df[num_cols].min().min()
    max_all = df[num_cols].max().max()
    if (min_all < -EPS) or (max_all > 1 + EPS):
        raise ValueError(f"Normalize değerler 0–1 bandı dışında görünüyor (min={min_all}, max={max_all}).")

    # 0< değerler <1 tolerans içine yuvarla (ör: 1.0000001 → 1)
    df[num_cols] = df[num_cols].clip(lower=0.0, upper=1.0)

    city_list = df["Sehir"].tolist()
    return df[["Sehir", "Sehir_Original"] + num_cols], num_cols, city_list


def _validate_and_prepare_criteria(df_criteria_raw: pd.DataFrame, feature_cols: List[str]) -> Tuple[pd.DataFrame, List[str]]:
    """
    Beklenen kolonlar: Sektor, KriterKey, Agirlik, Yon
    - Yon: {YUKSEK, DUSUK}
    - Ağırlıklar sektör bazında %100 toplam vermeli
    - KriterKey şehir feature'ları içinde olmalı
    """
    required = {"Sektor", "KriterKey", "Agirlik", "Yon"}
    missing = required - set(df_criteria_raw.columns)
    if missing:
        raise ValueError(f"Sektor_Kriter_Agirlik.xlsx zorunlu kolonlar eksik: {missing}")

    df = df_criteria_raw.copy()

    # Tip/normalize
    df["Sektor"] = df["Sektor"].astype(str)
    df["KriterKey"] = df["KriterKey"].astype(str)

    # Yon normalize
    df["Yon"] = df["Yon"].astype(str).str.upper().str.strip()
    valid_dirs = {"YUKSEK", "DUSUK"}
    if not set(df["Yon"]).issubset(valid_dirs):
        bad = sorted(set(df["Yon"]) - valid_dirs)
        raise ValueError(f"Geçersiz 'Yon' değerleri: {bad} (yalnızca {valid_dirs})")

    # Agirlik sayısal
    df["Agirlik"] = pd.to_numeric(df["Agirlik"], errors="coerce")
    if df["Agirlik"].isna().any():
        raise ValueError("Agirlik sütununda sayısal olmayan değerler var.")

    # KriterKey şehir kolonları içinde mi?
    missing_keys = sorted(set(df["KriterKey"]) - set(feature_cols))
    if missing_keys:
        raise ValueError(
            "Sektor_Kriter_Agirlik.xlsx içindeki bazı KriterKey alanları Iller_Normalize.xlsx feature'larında bulunamadı: "
            + ", ".join(missing_keys)
        )

    # Ağırlık toplamı sektör bazında ~100
    grp = df.groupby("Sektor")["Agirlik"].sum()
    bad_weight = grp[(grp < 100 - EPS) | (grp > 100 + EPS)]
    if not bad_weight.empty:
        details = ", ".join(f"{k}={v:.2f}" for k, v in bad_weight.items())
        raise ValueError(f"Ağırlık toplamı 100 değil: {details}")

    sector_list = sorted(df["Sektor"].unique().tolist())
    return df[["Sektor", "KriterKey", "Agirlik", "Yon"]], sector_list


def load_dataframes(force_reload: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, List[str], List[str], List[str], DataShapes]:
    """
    Ana yükleme noktası.
    Döner:
      - df_cities: Sehir + feature kolonları
      - df_criteria: Sektor, KriterKey, Agirlik, Yon
      - feature_cols: List[str]
      - sector_list: List[str]
      - city_list: List[str]
      - shapes: DataShapes
    """
    global _CITIES_DF, _CRITERIA_DF, _FEATURE_COLS, _SECTOR_LIST, _CITY_LIST

    if (not force_reload) and CACHE_DATAFRAMES and _CITIES_DF is not None and _CRITERIA_DF is not None:
        shapes = DataShapes(
            n_cities=len(_CITY_LIST or []),
            n_features=len(_FEATURE_COLS or []),
            n_criteria_rows=len(_CRITERIA_DF),
            n_sectors=len(_SECTOR_LIST or []),
        )
        return _CITIES_DF.copy(), _CRITERIA_DF.copy(), list(_FEATURE_COLS or []), list(_SECTOR_LIST or []), list(_CITY_LIST or []), shapes

    logger.info("Excel dosyaları yükleniyor...")
    df_cities_raw = _read_excel_safe(ILLER_FILE)
    df_cities, feature_cols, city_list = _validate_and_prepare_cities(df_cities_raw)

    df_criteria_raw = _read_excel_safe(SEKTOR_FILE)
    df_criteria, sector_list = _validate_and_prepare_criteria(df_criteria_raw, feature_cols)

    shapes = DataShapes(
        n_cities=len(city_list),
        n_features=len(feature_cols),
        n_criteria_rows=len(df_criteria),
        n_sectors=len(sector_list),
    )

    logger.info(
        f"Yüklendi: {shapes.n_cities} il, {shapes.n_features} feature, "
        f"{shapes.n_criteria_rows} kriter satırı, {shapes.n_sectors} sektör."
    )

    if CACHE_DATAFRAMES:
        _CITIES_DF = df_cities.copy()
        _CRITERIA_DF = df_criteria.copy()
        _FEATURE_COLS = list(feature_cols)
        _SECTOR_LIST = list(sector_list)
        _CITY_LIST = list(city_list)

    return df_cities, df_criteria, feature_cols, sector_list, city_list, shapes


def get_feature_columns() -> List[str]:
    global _FEATURE_COLS
    if _FEATURE_COLS is None:
        load_dataframes()
    return list(_FEATURE_COLS or [])


def get_sector_list() -> List[str]:
    global _SECTOR_LIST
    if _SECTOR_LIST is None:
        load_dataframes()
    return list(_SECTOR_LIST or [])


def get_city_list() -> List[str]:
    global _CITY_LIST
    if _CITY_LIST is None:
        load_dataframes()
    return list(_CITY_LIST or [])


def get_city_row(df_cities: pd.DataFrame, city: str) -> pd.Series:
    """
    Kanonik şehir adını bekler; eşleşmezse hata verir.
    """
    mask = df_cities["Sehir"].str.casefold() == (city or "").casefold()
    if not mask.any():
        raise KeyError(f"Şehir bulunamadı: '{city}'")
    row = df_cities.loc[mask].iloc[0]
    return row


def get_sector_slice(df_criteria: pd.DataFrame, sector: str) -> pd.DataFrame:
    """
    Verilen sektör için kriter satırlarını döndürür.
    """
    mask = df_criteria["Sektor"].str.casefold() == (sector or "").casefold()
    if not mask.any():
        raise KeyError(f"Sektör bulunamadı: '{sector}'")
    return df_criteria.loc[mask, ["KriterKey", "Agirlik", "Yon"]].reset_index(drop=True)


def invalidate_cache() -> None:
    """
    Excel güncellendiğinde cache'i boşaltmak için.
    """
    global _CITIES_DF, _CRITERIA_DF, _FEATURE_COLS, _SECTOR_LIST, _CITY_LIST
    _CITIES_DF = None
    _CRITERIA_DF = None
    _FEATURE_COLS = None
    _SECTOR_LIST = None
    _CITY_LIST = None
    logger.info("Loader cache temizlendi.")