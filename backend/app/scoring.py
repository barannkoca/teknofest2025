"""
scoring.py
- Yön dönüşümü + ağırlıklı toplam ile skor hesaplar
- 0–1 skorları 0–100 puana çevirir
- Tüm iller / tüm sektörler için hesaplama fonksiyonları sunar
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from .config import SCORE_SCALE_MAX
from .loader import (
    load_dataframes,
    get_sector_slice,
    get_city_row,
)

# ---------------------------------------------------------------------------

def _apply_direction(values: pd.Series, direction: str) -> pd.Series:
    """
    Yon=YUKSEK -> katkı = değer
    Yon=DUSUK  -> katkı = 1 - değer
    """
    direction = (direction or "").upper()
    if direction == "YUKSEK":
        return values
    elif direction == "DUSUK":
        return 1.0 - values
    else:
        raise ValueError(f"Geçersiz yön: {direction}")


def _score_vector_for_sector(df_cities: pd.DataFrame, sector_slice: pd.DataFrame) -> pd.Series:
    """
    Verilen sektör için (KriterKey, Agirlik, Yon) satırlarına göre
    tüm iller için 0–1 skor vektörü döndürür.
    """
    # Başlangıç 0
    score = pd.Series(0.0, index=df_cities.index)

    for _, row in sector_slice.iterrows():
        key = row["KriterKey"]
        w = float(row["Agirlik"]) / 100.0
        direction = row["Yon"]

        contrib = _apply_direction(df_cities[key], direction) * w
        score = score.add(contrib, fill_value=0.0)

    # Skor 0..1 aralığında kalmalı (işlem hatalarını tolere et)
    score = score.clip(lower=0.0, upper=1.0)
    return score


def score_all_cities(sector: str) -> Tuple[Dict[str, float], List[float]]:
    """
    Mod-1: Belirli bir sektör için 81 ilin skorlarını hesaplar (0–100'e ölçekli).
    Döner:
      - scores_by_city: { "İzmir": 60.6, ... }
      - legend: [0, 20, 40, 60, 80, 100] (basit linear eşik; UI'da quantile de yapılabilir)
    """
    df_cities, df_criteria, feature_cols, sector_list, city_list, _ = load_dataframes()

    sector_slice = get_sector_slice(df_criteria, sector)  # KriterKey, Agirlik, Yon
    score_0_1 = _score_vector_for_sector(df_cities, sector_slice)

    scores_by_city = {
        df_cities.loc[i, "Sehir"]: float(score_0_1.iloc[idx] * SCORE_SCALE_MAX)
        for idx, i in enumerate(score_0_1.index)
    }

    legend = [0, 20, 40, 60, 80, 100]
    return scores_by_city, legend


def score_all_sectors(city: str) -> Tuple[Dict[str, float], List[float]]:
    """
    Mod-2: Belirli bir il için tüm sektörlerin skorlarını hesaplar (0–100'e ölçekli).
    Döner:
      - scores_by_sector: { "Turizm": 60.6, ... }
      - legend: [0, 20, 40, 60, 80, 100]
    """
    df_cities, df_criteria, feature_cols, sector_list, city_list, _ = load_dataframes()

    # İlgili şehir satırını alın
    row = get_city_row(df_cities, city)  # Series
    # Hesaplamayı kolaylaştırmak için tek satırlık DataFrame'e çevir
    one_city_df = pd.DataFrame([row]).set_index(pd.Index([0]))

    scores_by_sector: Dict[str, float] = {}
    for sector in sector_list:
        sector_slice = df_criteria.loc[df_criteria["Sektor"].str.casefold() == sector.casefold(), ["KriterKey", "Agirlik", "Yon"]]
        score_0_1 = _score_vector_for_sector(one_city_df, sector_slice)
        scores_by_sector[sector] = float(score_0_1.iloc[0] * SCORE_SCALE_MAX)

    legend = [0, 20, 40, 60, 80, 100]
    return scores_by_sector, legend


def score_sector_for_city(city: str, sector: str, return_contributions: bool = False):
    """
    Tek bir (il, sektör) çifti için skoru hesaplar.
    return_contributions=True ise, kriter bazlı katkıları da döndürür.
    Döner:
      - score: float (0–100)
      - contributions (opsiyonel): List[dict]  -> explain.py için uygun
            { 'kriter': 'Konut...', 'yon': 'YUKSEK', 'agirlik': 24.0,
              'ham_deger': 0.62, 'katki': 0.1488 }   # (katki 0–1 bandında)
    """
    df_cities, df_criteria, feature_cols, sector_list, city_list, _ = load_dataframes()

    row = get_city_row(df_cities, city)  # Series
    sec_slice = get_sector_slice(df_criteria, sector)

    score_0_1 = 0.0
    contribs: List[dict] = []

    for _, r in sec_slice.iterrows():
        key = r["KriterKey"]
        w = float(r["Agirlik"]) / 100.0
        direction = r["Yon"]
        val = float(row[key])

        val_dir = val if direction == "YUKSEK" else (1.0 - val)
        katki = val_dir * w
        score_0_1 += katki

        if return_contributions:
            contribs.append({
                "kriter": key,
                "yon": direction,
                "agirlik": float(r["Agirlik"]),
                "ham_deger": val,
                "katki": float(katki),  # 0–1 bandında
            })

    score_0_1 = min(max(score_0_1, 0.0), 1.0)
    score = float(score_0_1 * SCORE_SCALE_MAX)

    if return_contributions:
        return score, contribs
    return score


def sort_top_n(score_dict: Dict[str, float], n: int = 5) -> List[Tuple[str, float]]:
    """
    Puan sözlüğünü (isim → puan) azalan sıralar, ilk n çifti döndürür.
    """
    return sorted(score_dict.items(), key=lambda kv: kv[1], reverse=True)[:n]