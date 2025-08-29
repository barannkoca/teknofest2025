import pandas as pd
import numpy as np
import os

def load_data_simple():
    """Excel dosyalarını basit şekilde yükle"""
    print("Excel dosyaları yükleniyor...")
    
    # İller verisi
    cities_df = pd.read_excel('data/Iller_Normalize.xlsx')
    print(f"İller verisi: {cities_df.shape}")
    print(f"Kolonlar: {cities_df.columns.tolist()}")
    
    # Sektör verisi
    sectors_df = pd.read_excel('data/Sektor_Kriter_Agirlik.xlsx')
    print(f"Sektör verisi: {sectors_df.shape}")
    print(f"Kolonlar: {sectors_df.columns.tolist()}")
    
    return cities_df, sectors_df

def calculate_sector_score_for_city(city, sector, cities_df, sectors_df):
    """Tek bir (il, sektör) çifti için skor hesapla"""
    try:
        # İl satırını bul
        city_row = cities_df[cities_df['İl'] == city].iloc[0]
        
        # Sektör kriterlerini al
        sector_criteria = sectors_df[sectors_df['Sektör'] == sector]
        
        if sector_criteria.empty:
            return None, []
        
        total_score = 0
        contributions = []
        
        for _, criterion in sector_criteria.iterrows():
            kriter_key = criterion['Tablo Adı']
            agirlik = criterion['Ağırlık (%)'] / 100.0
            yon = criterion['Yön']
            
            # Değeri al
            if kriter_key in city_row:
                value = city_row[kriter_key]
                
                # Yön uygula
                if yon == 'Yüksek':
                    katki = value * agirlik
                else:  # Düşük
                    katki = (1 - value) * agirlik
                
                total_score += katki
                
                contributions.append({
                    'kriter': criterion['Kriter'],
                    'yon': yon,
                    'agirlik': criterion['Ağırlık (%)'],
                    'ham_deger': value,
                    'katki': katki
                })
        
        # 0-100'e çevir
        final_score = min(max(total_score, 0), 1) * 100
        return final_score, contributions
        
    except Exception as e:
        print(f"Hata ({city}, {sector}): {e}")
        return None, []

def calculate_all_cities_for_sector(sector, cities_df, sectors_df):
    """Bir sektör için tüm illerin skorlarını hesapla"""
    scores = {}
    for _, city_row in cities_df.iterrows():
        city = city_row['İl']
        score, _ = calculate_sector_score_for_city(city, sector, cities_df, sectors_df)
        if score is not None:
            scores[city] = score
    return scores

def calculate_all_sectors_for_city(city, cities_df, sectors_df):
    """Bir il için tüm sektörlerin skorlarını hesapla"""
    scores = {}
    sectors = sectors_df['Sektör'].unique()
    for sector in sectors:
        score, _ = calculate_sector_score_for_city(city, sector, cities_df, sectors_df)
        if score is not None:
            scores[sector] = score
    return scores

def generate_all_scores_csv():
    """Tüm sektörler ve tüm iller için skorları hesapla ve CSV'ye yaz"""
    print("=== ECOMINDS SKOR HESAPLAMA ===")
    
    # Veriyi yükle
    cities_df, sectors_df = load_data_simple()
    
    # Sektör ve il listelerini al
    sector_list = sectors_df['Sektör'].unique()
    city_list = cities_df['İl'].tolist()
    
    print(f"\nToplam {len(sector_list)} sektör ve {len(city_list)} il bulundu.")
    
    # 1. Tüm sektörler için tüm illerin skorları
    print("\n1. Sektör → İl skorları hesaplanıyor...")
    sector_city_scores = {}
    
    for i, sector in enumerate(sector_list, 1):
        print(f"  {i}/{len(sector_list)}: {sector}")
        scores = calculate_all_cities_for_sector(sector, cities_df, sectors_df)
        sector_city_scores[sector] = scores
    
    # DataFrame'e çevir
    sector_city_df = pd.DataFrame(sector_city_scores).T
    sector_city_df.index.name = 'Sektor'
    sector_city_df.columns.name = 'Sehir'
    
    # 2. Tüm iller için tüm sektörlerin skorları
    print("\n2. İl → Sektör skorları hesaplanıyor...")
    city_sector_scores = {}
    
    for i, city in enumerate(city_list, 1):
        print(f"  {i}/{len(city_list)}: {city}")
        scores = calculate_all_sectors_for_city(city, cities_df, sectors_df)
        city_sector_scores[city] = scores
    
    # DataFrame'e çevir
    city_sector_df = pd.DataFrame(city_sector_scores).T
    city_sector_df.index.name = 'Sehir'
    city_sector_df.columns.name = 'Sektor'
    
    # 3. CSV dosyalarına yaz
    print("\n3. CSV dosyaları oluşturuluyor...")
    
    # Data klasörüne yaz
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Sektör → İl skorları
    sector_city_file = os.path.join(output_dir, 'Sektor_Il_Skorlari.csv')
    sector_city_df.to_csv(sector_city_file, encoding='utf-8-sig')
    print(f"  Sektör → İl skorları: {sector_city_file}")
    
    # İl → Sektör skorları
    city_sector_file = os.path.join(output_dir, 'Il_Sektor_Skorlari.csv')
    city_sector_df.to_csv(city_sector_file, encoding='utf-8-sig')
    print(f"  İl → Sektör skorları: {city_sector_file}")
    
    # 4. Top 5 listeleri
    print("\n4. Top 5 listeleri oluşturuluyor...")
    
    def sort_top_n(score_dict, n=5):
        """Puan sözlüğünü azalan sırala, ilk n çifti döndür"""
        return sorted(score_dict.items(), key=lambda kv: kv[1], reverse=True)[:n]
    
    # Her sektör için top 5 il
    top5_cities_per_sector = {}
    for sector in sector_list:
        if sector in sector_city_scores:
            scores = sector_city_scores[sector]
            top5 = sort_top_n(scores, 5)
            top5_cities_per_sector[sector] = top5
    
    # Her il için top 5 sektör
    top5_sectors_per_city = {}
    for city in city_list:
        if city in city_sector_scores:
            scores = city_sector_scores[city]
            top5 = sort_top_n(scores, 5)
            top5_sectors_per_city[city] = top5
    
    # Top 5 listelerini CSV'ye yaz
    def create_top5_df(top5_dict, col1_name, col2_name):
        rows = []
        for key, top5_list in top5_dict.items():
            for rank, (name, score) in enumerate(top5_list, 1):
                rows.append({
                    col1_name: key,
                    'Sira': rank,
                    col2_name: name,
                    'Skor': score
                })
        return pd.DataFrame(rows)
    
    # Top 5 iller per sektör
    top5_cities_df = create_top5_df(top5_cities_per_sector, 'Sektor', 'Sehir')
    top5_cities_file = os.path.join(output_dir, 'Top5_Iller_Per_Sektor.csv')
    top5_cities_df.to_csv(top5_cities_file, index=False, encoding='utf-8-sig')
    print(f"  Top 5 iller per sektör: {top5_cities_file}")
    
    # Top 5 sektörler per il
    top5_sectors_df = create_top5_df(top5_sectors_per_city, 'Sehir', 'Sektor')
    top5_sectors_file = os.path.join(output_dir, 'Top5_Sektorler_Per_Il.csv')
    top5_sectors_df.to_csv(top5_sectors_file, index=False, encoding='utf-8-sig')
    print(f"  Top 5 sektörler per il: {top5_sectors_file}")
    
    # 5. Özet istatistikler
    print("\n5. Özet istatistikler:")
    print(f"  Toplam sektör sayısı: {len(sector_list)}")
    print(f"  Toplam il sayısı: {len(city_list)}")
    print(f"  Toplam hesaplama: {len(sector_list) * len(city_list)}")
    
    # Ortalama skorlar
    print(f"\n  Sektör → İl ortalama skorları:")
    sector_avg = sector_city_df.mean(axis=1).sort_values(ascending=False)
    for sector, avg_score in sector_avg.head(10).items():
        print(f"    {sector}: {avg_score:.1f}")
    
    print(f"\n  İl → Sektör ortalama skorları:")
    city_avg = city_sector_df.mean(axis=1).sort_values(ascending=False)
    for city, avg_score in city_avg.head(10).items():
        print(f"    {city}: {avg_score:.1f}")
    
    print(f"\n✅ Tüm skorlar başarıyla hesaplandı ve CSV dosyalarına yazıldı!")
    print(f"📁 Dosyalar: {output_dir}/")
    
    return {
        'sector_city_df': sector_city_df,
        'city_sector_df': city_sector_df,
        'top5_cities_df': top5_cities_df,
        'top5_sectors_df': top5_sectors_df
    }

if __name__ == "__main__":
    generate_all_scores_csv()
