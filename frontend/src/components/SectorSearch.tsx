import React, { useState } from 'react';

interface CitySearchData {
  name: string;
  score: number;
  reasons: string[];
}

const SectorSearch: React.FC = () => {
  const [selectedSector, setSelectedSector] = useState<string>('');
  const [searchResults, setSearchResults] = useState<CitySearchData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // CSV'deki gerçek sektör isimleri
  const sectors = [
    'Turizm / Otelcilik',
    'Teknoloji / Yazılım',
    'Sanayi / Üretim',
    'Tarım ve Hayvancılık',
    'Sağlık',
    'Enerji',
    'Konut & İnşaat',
    'Lojistik',
    'Perakende',
    'Eğitim Kurumları',
    'Gıda İşleme',
    'Finans',
    'Otomotiv',
    'Mobilya',
    'Telekom',
    'Çevre / Atık',
    'Sosyal Hizmetler',
    'Kültür & Sanat',
    'Ulaşım'
  ];

  // Sektör için şehir verilerini backend'den al
  const getCitiesForSector = async (sectorName: string): Promise<CitySearchData[]> => {
    try {
      setIsLoading(true);
      // Sektör ismini URL'de encode et
      const encodedSectorName = encodeURIComponent(sectorName);
      const response = await fetch(`http://localhost:8000/api/mod1?sector=${encodedSectorName}&topn=5`);
      if (!response.ok) {
        throw new Error('Veri alınamadı');
      }
      const data = await response.json();
      return data.top5 || [];
    } catch (error) {
      console.error('Şehir verisi alınırken hata:', error);
      return [];
    } finally {
      setIsLoading(false);
    }
  };

  // Sektör seçim fonksiyonu
  const handleSectorChange = async (sectorName: string) => {
    setSelectedSector(sectorName);
    if (sectorName) {
      const results = await getCitiesForSector(sectorName);
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  };

  return (
    <div className="sector-search-wrapper">
      <div className="search-header">
        <h2>🔍 Sektör Bazlı Şehir Analizi</h2>
        <p>Bir sektör seçin ve o sektörde en iyi performans gösteren 5 şehri keşfedin</p>
      </div>
      
      <div className="search-controls">
        <label htmlFor="sector-select">
          <span className="label-icon">🏭</span>
          Sektör Seçin:
        </label>
        <div className="dropdown-wrapper">
          <select
            id="sector-select"
            value={selectedSector}
            onChange={(e) => handleSectorChange(e.target.value)}
            className="sector-select"
            disabled={isLoading}
          >
            <option value="">-- Sektör Seçin --</option>
            {sectors.map((sector, index) => (
              <option key={index} value={sector}>
                {sector}
              </option>
            ))}
          </select>
          {isLoading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
            </div>
          )}
        </div>
      </div>
      
      {/* Arama Sonuçları */}
      {searchResults.length > 0 && (
        <div className="results-section">
          <div className="results-title">
            <h3>🏆 {selectedSector} Sektöründe En İyi 5 Şehir</h3>
            <span className="results-count">{searchResults.length} şehir bulundu</span>
          </div>
          
          <div className="cities-list">
            {searchResults.map((city, index) => {
              const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅';
              
              return (
                <div key={index} className={`city-item rank-${index + 1}`}>
                  <div className="city-medal">
                    <span className="medal-icon">{medal}</span>
                    <span className="rank-badge">#{index + 1}</span>
                  </div>
                  <div className="city-details">
                    <div className="city-name">{city.name}</div>
                    <div className="city-score">Skor: {city.score.toFixed(1)}</div>
                  </div>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{ 
                        width: `${(city.score / 100) * 100}%`,
                        background: index === 0 ? '#FFD700' : index === 1 ? '#C0C0C0' : index === 2 ? '#CD7F32' : '#4ecdc4'
                      }}
                    ></div>
                  </div>
                  {/* Gerekçeler */}
                  {city.reasons && city.reasons.length > 0 && (
                    <div className="city-reasons">
                      <div className="reasons-title">📊 Gerekçeler:</div>
                      <ul className="reasons-list">
                        {city.reasons.map((reason, reasonIndex) => (
                          <li key={reasonIndex} className="reason-item">{reason}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
      
      {/* Boş durum */}
      {selectedSector && searchResults.length === 0 && !isLoading && (
        <div className="empty-message">
          <div className="empty-icon">📊</div>
          <h3>Veri Bulunamadı</h3>
          <p>{selectedSector} sektörü için şehir verisi bulunamadı.</p>
        </div>
      )}
    </div>
  );
};

export default SectorSearch;
