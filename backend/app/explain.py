"""
explain.py
- Skor katkılarından (+) güçlü alanlar ve (⚠) risk/iyileştirme rozetlerini üretir.
- Kriter anahtarlarını okunur kısa etiketlere dönüştürür.
"""

from __future__ import annotations

import re
from typing import Dict, List

# ---- Kriter anahtarını okunur etikete çevirme ------------------------------

def _soft_title(s: str) -> str:
    # "AlinanFARKVerilenGocBOLUNUFUS" -> "Alinan FARK Verilen Goc"
    s = s.replace("_", " ").replace("-", " ").replace(".", " ")
    s = re.sub(r"BOLUNUFUS", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+", " ", s).strip()

    # Büyük harf öncesi boşluk koy
    s = re.sub(r"(?<!^)(?=[A-ZÇĞİÖŞÜ])", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # İlk harfleri büyüt (Türkçe özel durumlarını basit geçiyoruz)
    return s[:1].upper() + s[1:]

def _label_from_key(key: str) -> str:
    """
    Heuristik eşleştirme: metrik key'ini kısa, anlaşılır etikete çevirir.
    Bilinen örnekler için daha güzel adlar; bilinmeyende makul bir başlık üretir.
    """
    k = key.lower()

    def has(*subs: str) -> bool:
        return all(sub in k for sub in subs)

    # Bilinen/örnek isimler
    if "konut" in k and ("satis" in k or "satış" in k):
        return "Konut satışı"
    if ("toplu" in k and ("tasima" in k or "taşıma" in k)) and "memnun" in k:
        return "Toplu taşıma memnuniyeti"
    if "universite" in k or "üniversite" in k:
        return "Üniversite ve üstü oranı"
    if "ihracat" in k or "ithalat" in k:
        return "İhracat–İthalat farkı"
    if "goc" in k or "göç" in k:
        return "Göç cazibesi"
    if "tarim" in k or "tarım" in k:
        return "Tarım alanı"
    if "hastane" in k and ("hekim" in k or "doktor" in k):
        return "Hekim/Hastane oranı"
    if "ortalama" in k and ("yas" in k or "yaş" in k):
        return "Ortalama yaş"
    if "istihdam" in k:
        return "İstihdam oranı"
    if "toplu" in k and ("tasima" in k or "taşıma" in k):
        return "Toplu taşıma"

    # Fallback: anahtarı yumuşak başlığa çevir
    return _soft_title(key)

# ---- Gerekçe üretimi -------------------------------------------------------

def build_reasons_from_contributions(
    contributions: List[Dict],
    top_k_pos: int = 2,
    include_risk: bool = True,
) -> List[str]:
    """
    scoring.score_sector_for_city(..., return_contributions=True) çıktısını alır,
    en yüksek katkıdan başlayarak + rozetlerini ve en düşük katkı için ⚠ rozetini üretir.

    contributions[i]: {
      'kriter': str, 'yon': 'YUKSEK'|'DUSUK', 'agirlik': float,
      'ham_deger': float (0..1), 'katki': float (0..1)
    }
    """
    if not contributions:
        return []

    # Katkıya göre sırala (yüksek → düşük)
    contrib_sorted = sorted(contributions, key=lambda c: c.get("katki", 0.0), reverse=True)

    reasons: List[str] = []

    # (+) En güçlüler
    for c in contrib_sorted[:max(0, top_k_pos)]:
        label = _label_from_key(str(c.get("kriter", "")))
        # İsteğe bağlı olarak yön bilgisini paranteze ekleyebilirsin:
        # dir_note = "yüksek" if c.get("yon") == "YUKSEK" else "düşük"
        # reasons.append(f"+ {label} ({dir_note})")
        reasons.append(f"+ {label}")

    # (⚠) En zayıf
    if include_risk and len(contrib_sorted) > 0:
        weakest = contrib_sorted[-1]
        label_w = _label_from_key(str(weakest.get("kriter", "")))
        reasons.append(f"⚠ {label_w}")

    return reasons

__all__ = ["build_reasons_from_contributions"]