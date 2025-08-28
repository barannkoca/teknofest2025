import pandas as pd
import numpy as np
from calculateScore import read_data, calculate_sector_score_for_city, calculate_all_cities_for_sector

def test_scoring():
    """Scoring sistemini test et"""
    
    print("=== ECOMINDS SCORING SİSTEMİ TEST ===")
    
    # Veriyi oku
    iller_df, sektor_df = read_data()
    
    print(f"İller verisi: {iller_df.shape}")
    print(f"Sektör verisi: {sektor_df.shape}")
    
    # Mevcut sektörleri göster
    print(f"\nMevcut sektörler:")
    sectors = sektor_df['Sektör'].unique()
    for i, sector in enumerate(sectors, 1):
        print(f"{i}. {sector}")
    
    # Test 1: İzmir - Turizm skoru
    print("\n" + "="*50)
    print("TEST 1: İzmir - Turizm / Otelcilik")
    score, contributions = calculate_sector_score_for_city("İzmir", "Turizm / Otelcilik", iller_df, sektor_df)
    
    if score is not None:
        print(f"İzmir - Turizm skoru: {score:.1f}/100")
        
        # En büyük katkıları göster
        sorted_contributions = sorted(contributions, key=lambda x: x['weighted_contribution'], reverse=True)
        print(f"\nEn büyük katkılar:")
        for i, contrib in enumerate(sorted_contributions[:3], 1):
            print(f"{i}. {contrib['kriter']}: {contrib['weighted_contribution']:.3f}")
    
    # Test 2: Tüm iller için Turizm skorları
    print("\n" + "="*50)
    print("TEST 2: Tüm iller için Turizm skorları")
    all_scores = calculate_all_cities_for_sector("Turizm / Otelcilik", iller_df, sektor_df)
    
    # Top 5 il
    sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop 5 il:")
    for i, (city, score) in enumerate(sorted_scores[:5], 1):
        print(f"{i}. {city}: {score:.1f}")
    
    # Test 3: İzmir için tüm sektörler
    print("\n" + "="*50)
    print("TEST 3: İzmir için tüm sektörler")
    izmir_sector_scores = {}
    
    for sector in sectors:
        score, _ = calculate_sector_score_for_city("İzmir", sector, iller_df, sektor_df)
        if score is not None:
            izmir_sector_scores[sector] = score
    
    # Top 5 sektör
    sorted_sectors = sorted(izmir_sector_scores.items(), key=lambda x: x[1], reverse=True)
    print(f"\nİzmir için Top 5 sektör:")
    for i, (sector, score) in enumerate(sorted_sectors[:5], 1):
        print(f"{i}. {sector}: {score:.1f}")

if __name__ == "__main__":
    test_scoring()
