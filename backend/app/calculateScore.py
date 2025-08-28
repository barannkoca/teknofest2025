import pandas as pd
import numpy as np

def read_data():
    """Excel dosyalarını oku"""
    # İller verisi (81 il × 14 kriter, 0-1 normalize)
    iller_df = pd.read_excel('../data/Iller_Normalize.xlsx')
    
    # Sektör verisi (83 kayıt × 5 sütun: Sektör, Kriter, Tablo Adı, Ağırlık (%), Yön)
    sektor_df = pd.read_excel('../data/Sektor_Kriter_Agirlik.xlsx')
    
    return iller_df, sektor_df

def calculate_sector_score_for_city(city_name, sector_name, iller_df, sektor_df):
    """Bir il için bir sektörün skorunu hesapla"""
    
    # İl verisini al
    city_data = iller_df[iller_df['İl'] == city_name]
    if len(city_data) == 0:
        return None, f"İl bulunamadı: {city_name}"
    
    # Sektör kriterlerini al
    sector_criteria = sektor_df[sektor_df['Sektör'] == sector_name]
    if len(sector_criteria) == 0:
        return None, f"Sektör bulunamadı: {sector_name}"
    
    total_score = 0.0
    contributions = []
    
    # Her kriter için skor hesapla
    for _, criterion in sector_criteria.iterrows():
        kriter_adi = criterion['Kriter']
        tablo_adi = criterion['Tablo Adı']
        agirlik = criterion['Ağırlık (%)'] / 100.0  # Yüzdelikten ondalığa çevir
        yon = criterion['Yön']
        
        # İl verisinden kriter değerini al
        if tablo_adi in city_data.columns:
            raw_value = float(city_data[tablo_adi].iloc[0])
            
            # YÖN uygulaması
            if yon == "Yüksek":
                contribution = raw_value
            else:  # "Düşük"
                contribution = 1.0 - raw_value
            
            # Ağırlıklı katkı
            weighted_contribution = contribution * agirlik
            total_score += weighted_contribution
            
            contributions.append({
                'kriter': kriter_adi,
                'tablo_adi': tablo_adi,
                'raw_value': raw_value,
                'yon': yon,
                'contribution': contribution,
                'agirlik': agirlik,
                'weighted_contribution': weighted_contribution
            })
    
    # 0-1 arası skoru 0-100'e çevir
    final_score = total_score * 100.0
    
    return final_score, contributions

def calculate_all_cities_for_sector(sector_name, iller_df, sektor_df):
    """Bir sektör için tüm illerin skorlarını hesapla"""
    
    scores = {}
    for _, city_row in iller_df.iterrows():
        city_name = city_row['İl']
        score, _ = calculate_sector_score_for_city(city_name, sector_name, iller_df, sektor_df)
        if score is not None:
            scores[city_name] = score
    
    return scores

def main():
    """Ana fonksiyon - test çıktıları ile"""
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
    main()

