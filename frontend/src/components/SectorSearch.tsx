import React, { useState } from 'react';

interface CitySearchData {
  name: string;
  score: number;
  reasons: string[];
}

interface SectorSearchData {
  name: string;
  score: number;
  reasons: string[];
}

const SectorSearch: React.FC = () => {
  const [selectedSector, setSelectedSector] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [searchResults, setSearchResults] = useState<CitySearchData[]>([]);
  const [citySearchResults, setCitySearchResults] = useState<SectorSearchData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [cityIsLoading, setCityIsLoading] = useState<boolean>(false);

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

  // Türkiye illeri
  const cities = [
    'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Amasya', 'Ankara', 'Antalya', 'Artvin', 'Aydın', 'Balıkesir',
    'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum', 'Denizli',
    'Diyarbakır', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari',
    'Hatay', 'Isparta', 'Mersin', 'İstanbul', 'İzmir', 'Kars', 'Kastamonu', 'Kayseri', 'Kırklareli', 'Kırşehir',
    'Kocaeli', 'Konya', 'Kütahya', 'Malatya', 'Manisa', 'Kahramanmaraş', 'Mardin', 'Muğla', 'Muş', 'Nevşehir',
    'Niğde', 'Ordu', 'Rize', 'Sakarya', 'Samsun', 'Siirt', 'Sinop', 'Sivas', 'Tekirdağ', 'Tokat',
    'Trabzon', 'Tunceli', 'Şanlıurfa', 'Uşak', 'Van', 'Yozgat', 'Zonguldak', 'Aksaray', 'Bayburt', 'Karaman',
    'Kırıkkale', 'Batman', 'Şırnak', 'Bartın', 'Ardahan', 'Iğdır', 'Yalova', 'Karabük', 'Kilis', 'Osmaniye', 'Düzce'
  ];

  // Sıra etiketi
  const rankLabel = (rank: number) => `${rank}. il`;
  const sectorRankLabel = (rank: number) => `${rank}. sektör`;

  // Varsayılan (eşleşmeyen sektör olursa)
  const defaultSentence = (c: string, r: number) =>
    `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, seçilen sektörde ölçeklenebilir bir pazar ve operasyonel avantajlar sunmaktadır.`;

  // Sektör -> cümle üretici
  const sectorSentenceMap: Record<string, (c: string, r: number) => string> = {
    'Turizm / Otelcilik': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, yüksek turizm potansiyeli ve markalaşma fırsatlarıyla yeni tesis/hizmet yatırımlarından hızlı geri dönüş sağlayacaktır.`,
    'Teknoloji / Yazılım': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, güçlü teknoloji altyapısı ve nitelikli genç iş gücüyle Ar-Ge ve teknolojik gelişmeleri hızlandıracak bir ekosisteme sahiptir.`,
    'Sanayi / Üretim': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, OSB/tedarik zincirine yakınlığı ve ölçeklenebilir üretim kapasitesiyle verimlilik ve rekabet avantajı sunar.`,
    'Tarım ve Hayvancılık': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, verimli araziler ve güçlü hammadde arzı sayesinde birincil üretim ve işleme yatırımlarında yüksek etki üretir.`,
    'Sağlık': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c} ilinde ciddi bir sağlık altyapısı yetersizliği vardır ve yatak/uzman kapasitesi artışına ihtiyaç vardır; yatırımlar erişilebilirliği ve hizmet kalitesini yükseltecektir.`,
    'Enerji': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, kaynaklara/iletim hatlarına erişim ve yenilenebilir potansiyeliyle enerji yatırımlarında stratejik konumdadır.`,
    'Konut & İnşaat': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, kentsel dönüşüm ve artan konut talebiyle projelerin sürdürülebilir talep ve istihdam yaratmasını sağlar.`,
    'Lojistik': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, kara/deniz/hava ağlarının kavşağında olup depolama ve dağıtım yatırımlarında büyük rol üstlenir.`,
    'Perakende': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, nüfus yoğunluğu ve tüketim gücüyle mağaza/ağ genişletme yatırımlarında hızlı ölçeklenmeyi mümkün kılar.`,
    'Eğitim Kurumları': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü bölgede eğitim ihtiyacı giderek artmaktadır, eğitim altyapısının güçlendirilmesi bölgesel insan kaynağını ve ilin kalkınmasını hızla iyileştirecektir.`,
    'Gıda İşleme': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, hammaddeye yakınlık ve tedarik avantajıyla gıda işleme tesisleri için düşük lojistik maliyet ve taze üretim sağlar.`,
    'Finans': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, gelişmiş finansal altyapı, sermayeye erişim ve nitelikli iş gücü ile genişleyen finans hizmetleri için sağlam bir zemine sahiptir.`,
    'Otomotiv': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, güçlü yan sanayi ve ihracat kanalları sayesinde otomotiv üretim/yeni nesil mobilite yatırımlarında büyük avantaj sağlar.`,
    'Mobilya': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, mobilya kümelenmesi ve lojistik erişimle üretimde ölçek ekonomisi ve tedarik sürekliliği sağlar.`,
    'Telekom': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, fiber/5G şebekesinin genişletilmesine elverişlidir; yatırımlar dijital dönüşüm ve hizmet kalitesini hızlandıracaktır.`,
    'Çevre / Atık': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü bölgede çevresel yük ve atık birikimi dikkat çekmekte, bazı alanlarda kirlilik halk sağlığını tehdit etmektedir; geri dönüşüm, atık ayrıştırma ve bertaraf yatırımları acil ihtiyaçtır.`,
    'Sosyal Hizmetler': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, dezavantajlı gruplara erişim ve kapsayıcı hizmetler için yetersiz olduğundan kapasite artışına ihtiyaç duymaktadır; yatırımlar yaşam kalitesini artıracaktır.`,
    'Kültür & Sanat': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}, kültürel mirası görünür kılacak ve yaratıcı endüstrileri canlandıracak etkinlik/mekân yatırımlarıyla şehir markasını ve yaşam kalitesini belirgin biçimde yükseltebilir.`,
    'Ulaşım': (c, r) =>
      `Yatırım yapılacak ${rankLabel(r)} ${c} olmalıdır. Çünkü ${c}'de ulaşımın zor olduğu hatlarda kapasite ve bağlantı eksikleri bulunmaktadır; çeşitli ulaşım yatırımları erişilebilirliği ve ekonomik hareketliliği artıracaktır.`
  };

  // Şehir -> sektör cümle üretici - DÜZELTİLDİ!
  const citySectorSentenceMap: Record<string, (city: string, r: number) => string> = {
    'Turizm / Otelcilik': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Turizm / Otelcilik olmalıdır. Çünkü Turizm / Otelcilik, yüksek turizm potansiyeli ve markalaşma fırsatlarıyla yeni tesis/hizmet yatırımlarından hızlı geri dönüş sağlayacaktır.`,
    'Teknoloji / Yazılım': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Teknoloji / Yazılım olmalıdır. Çünkü Teknoloji / Yazılım, güçlü teknoloji altyapısı ve nitelikli genç iş gücüyle Ar-Ge ve teknolojik gelişmeleri hızlandıracak bir ekosisteme sahiptir.`,
    'Sanayi / Üretim': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Sanayi / Üretim olmalıdır. Çünkü Sanayi / Üretim, OSB/tedarik zincirine yakınlığı ve ölçeklenebilir üretim kapasitesiyle verimlilik ve rekabet avantajı sunar.`,
    'Tarım ve Hayvancılık': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Tarım ve Hayvancılık olmalıdır. Çünkü Tarım ve Hayvancılık, verimli araziler ve güçlü hammadde arzı sayesinde birincil üretim ve işleme yatırımlarında yüksek etki üretir.`,
    'Sağlık': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Sağlık olmalıdır. Çünkü Sağlık sektöründe ciddi bir altyapı yetersizliği vardır ve yatak/uzman kapasitesi artışına ihtiyaç vardır; yatırımlar erişilebilirliği ve hizmet kalitesini yükseltecektir.`,
    'Enerji': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Enerji olmalıdır. Çünkü Enerji, kaynaklara/iletim hatlarına erişim ve yenilenebilir potansiyeliyle enerji yatırımlarında stratejik konumdadır.`,
    'Konut & İnşaat': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Konut & İnşaat olmalıdır. Çünkü Konut & İnşaat, kentsel dönüşüm ve artan konut talebiyle projelerin sürdürülebilir talep ve istihdam yaratmasını sağlar.`,
    'Lojistik': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Lojistik olmalıdır. Çünkü Lojistik, kara/deniz/hava ağlarının kavşağında olup depolama ve dağıtım yatırımlarında büyük rol üstlenir.`,
    'Perakende': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Perakende olmalıdır. Çünkü Perakende, nüfus yoğunluğu ve tüketim gücüyle mağaza/ağ genişletme yatırımlarında hızlı ölçeklenmeyi mümkün kılar.`,
    'Eğitim Kurumları': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Eğitim Kurumları olmalıdır. Çünkü bölgede eğitim ihtiyacı giderek artmaktadır, eğitim altyapısının güçlendirilmesi bölgesel insan kaynağını ve ilin kalkınmasını hızla iyileştirecektir.`,
    'Gıda İşleme': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Gıda İşleme olmalıdır. Çünkü Gıda İşleme, hammaddeye yakınlık ve tedarik avantajıyla gıda işleme tesisleri için düşük lojistik maliyet ve taze üretim sağlar.`,
    'Finans': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Finans olmalıdır. Çünkü Finans, gelişmiş finansal altyapı, sermayeye erişim ve nitelikli iş gücü ile genişleyen finans hizmetleri için sağlam bir zemine sahiptir.`,
    'Otomotiv': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Otomotiv olmalıdır. Çünkü Otomotiv, güçlü yan sanayi ve ihracat kanalları sayesinde otomotiv üretim/yeni nesil mobilite yatırımlarında büyük avantaj sağlar.`,
    'Mobilya': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Mobilya olmalıdır. Çünkü Mobilya, mobilya kümelenmesi ve lojistik erişimle üretimde ölçek ekonomisi ve tedarik sürekliliği sağlar.`,
    'Telekom': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Telekom olmalıdır. Çünkü Telekom, fiber/5G şebekesinin genişletilmesine elverişlidir; yatırımlar dijital dönüşüm ve hizmet kalitesini hızlandıracaktır.`,
    'Çevre / Atık': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Çevre / Atık olmalıdır. Çünkü bölgede çevresel yük ve atık birikimi dikkat çekmekte, bazı alanlarda kirlilik halk sağlığını tehdit etmektedir; geri dönüşüm, atık ayrıştırma ve bertaraf yatırımları acil ihtiyaçtır.`,
    'Sosyal Hizmetler': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Sosyal Hizmetler olmalıdır. Çünkü Sosyal Hizmetler sektöründe dezavantajlı gruplara erişim ve kapsayıcı hizmetler için yetersiz olduğundan kapasite artışına ihtiyaç duymaktadır; yatırımlar yaşam kalitesini artıracaktır.`,
    'Kültür & Sanat': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Kültür & Sanat olmalıdır. Çünkü Kültür & Sanat, kültürel mirası görünür kılacak ve yaratıcı endüstrileri canlandıracak etkinlik/mekân yatırımlarıyla şehir markasını ve yaşam kalitesini belirgin biçimde yükseltebilir.`,
    'Ulaşım': (city, r) =>
      `${city} ilinde ${sectorRankLabel(r)} Ulaşım olmalıdır. Çünkü Ulaşım sektöründe kapasite ve bağlantı eksikleri bulunmaktadır; çeşitli ulaşım yatırımları erişilebilirliği ve ekonomik hareketliliği artıracaktır.`
  };

  // Sektör için şehir verilerini backend'den al
  const getCitiesForSector = async (sectorName: string): Promise<CitySearchData[]> => {
    try {
      setIsLoading(true);
      const encodedSectorName = encodeURIComponent(sectorName);
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/mod1?sector=${encodedSectorName}&topn=5`);
      if (!response.ok) throw new Error('Veri alınamadı');
      const data = await response.json();
      return (data?.top5 ?? []) as CitySearchData[];
    } catch (error) {
      console.error('Şehir verisi alınırken hata:', error);
      return [];
    } finally {
      setIsLoading(false);
    }
  };

  // Şehir için sektör verilerini backend'den al
  const getSectorsForCity = async (cityName: string): Promise<SectorSearchData[]> => {
    try {
      setCityIsLoading(true);
      const encodedCityName = encodeURIComponent(cityName);
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/mod2?city=${encodedCityName}&topn=5`);
      if (!response.ok) throw new Error('Veri alınamadı');
      const data = await response.json();
      return (data?.top5 ?? []) as SectorSearchData[];
    } catch (error) {
      console.error('Sektör verisi alınırken hata:', error);
      return [];
    } finally {
      setCityIsLoading(false);
    }
  };

  // Sektör seçim fonksiyonu
  const handleSectorChange = async (sectorName: string) => {
    setSelectedSector(sectorName);
    setSelectedCity(''); // Şehir seçimini temizle
    setCitySearchResults([]); // Şehir arama sonuçlarını temizle
    if (sectorName) {
      const results = await getCitiesForSector(sectorName);
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  };

  // Şehir seçim fonksiyonu
  const handleCityChange = async (cityName: string) => {
    setSelectedCity(cityName);
    setSelectedSector(''); // Sektör seçimini temizle
    setSearchResults([]); // Sektör arama sonuçlarını temizle
    if (cityName) {
      const results = await getSectorsForCity(cityName);
      setCitySearchResults(results);
    } else {
      setCitySearchResults([]);
    }
  };

  const buildSentence = (sector: string, city: string, rank: number) =>
    (sectorSentenceMap[sector] ?? defaultSentence)(city, rank);

  const buildCitySectorSentence = (sector: string, city: string, rank: number) =>
    (citySectorSentenceMap[sector] ?? ((city, r) => `${city} ilinde ${sectorRankLabel(r)} ${sector} olmalıdır. Çünkü ${sector}, seçilen ilde ölçeklenebilir bir pazar ve operasyonel avantajlar sunmaktadır.`))(city, rank);

  return (
    <div className="sector-search-wrapper">
      <div className="search-header">
        <h2>🔍 Sektör ve İl Bazlı Yatırım Analizi</h2>
        <p>Bir sektör seçin ve en iyi 5 şehri, veya bir şehir seçin ve en iyi 5 sektörü keşfedin</p>
      </div>
      
      {/* Sektör Arama Bölümü */}
      <div className="search-section">
        <h3>🏭 Sektör Bazlı Şehir Analizi</h3>
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
        
        {/* Sektör Arama Sonuçları */}
        {searchResults.length > 0 && (
          <div className="results-section">
            <div className="results-title">
              <h4>🏆 {selectedSector} Sektöründe En İyi 5 Şehir</h4>
              <span className="results-count">{searchResults.length} şehir bulundu</span>
            </div>
            
            <div className="cities-list">
              {searchResults.map((city, index) => {
                const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅';
                const rank = index + 1;
                
                return (
                  <div key={index} className={`city-item rank-${rank}`}>
                    <div className="city-medal">
                      <span className="medal-icon">{medal}</span>
                      <span className="rank-badge">#{rank}</span>
                    </div>

                    <div className="city-details">
                      <div className="city-name">{city.name}</div>
                      <div className="city-score">Skor: {city.score.toFixed(1)}</div>
                    </div>

                    <div className="score-bar">
                      <div 
                        className="score-fill" 
                        style={{ 
                          width: `${Math.max(0, Math.min(100, Number(city.score)))}%`,
                          background: index === 0 ? '#FFD700' : index === 1 ? '#C0C0C0' : index === 2 ? '#CD7F32' : '#4ecdc4'
                        }}
                      />
                    </div>

                    {/* Gerekçeler */}
                    <div className="city-reasons">
                      <div className="reasons-title">📊 Gerekçeler:</div>
                      <ul className="reasons-list">
                        <li className="reason-item">
                          {buildSentence(selectedSector, city.name, rank)}
                        </li>
                        {Array.isArray(city.reasons) && city.reasons.map((reason, i) => (
                          <li key={i} className="reason-item">{reason}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Şehir Arama Bölümü */}
      <div className="search-section">
        <h3>🏙️ Şehir Bazlı Sektör Analizi</h3>
        <div className="search-controls">
          <label htmlFor="city-select">
            <span className="label-icon">🏙️</span>
            Şehir Seçin:
          </label>
          <div className="dropdown-wrapper">
            <select
              id="city-select"
              value={selectedCity}
              onChange={(e) => handleCityChange(e.target.value)}
              className="city-select"
              disabled={cityIsLoading}
            >
              <option value="">-- Şehir Seçin --</option>
              {cities.map((city, index) => (
                <option key={index} value={city}>
                  {city}
                </option>
              ))}
            </select>
            {cityIsLoading && (
              <div className="loading-spinner">
                <div className="spinner"></div>
              </div>
            )}
          </div>
        </div>
        
        {/* Şehir Arama Sonuçları */}
        {citySearchResults.length > 0 && (
          <div className="results-section">
            <div className="results-title">
              <h4>🏆 {selectedCity} İlinde En İyi 5 Sektör</h4>
              <span className="results-count">{citySearchResults.length} sektör bulundu</span>
            </div>
            
            <div className="sectors-list">
              {citySearchResults.map((sector, index) => {
                const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅';
                const rank = index + 1;
                
                return (
                  <div key={index} className={`sector-item rank-${rank}`}>
                    <div className="sector-medal">
                      <span className="medal-icon">{medal}</span>
                      <span className="rank-badge">#{rank}</span>
                    </div>

                    <div className="sector-details">
                      <div className="sector-name">{sector.name}</div>
                      <div className="sector-score">Skor: {sector.score.toFixed(1)}</div>
                    </div>

                    <div className="score-bar">
                      <div 
                        className="score-fill" 
                        style={{ 
                          width: `${Math.max(0, Math.min(100, Number(sector.score)))}%`,
                          background: index === 0 ? '#FFD700' : index === 1 ? '#C0C0C0' : index === 2 ? '#CD7F32' : '#4ecdc4'
                        }}
                      />
                    </div>

                    {/* Gerekçeler */}
                    <div className="sector-reasons">
                      <div className="reasons-title">📊 Gerekçeler:</div>
                      <ul className="reasons-list">
                        <li className="reason-item">
                          {buildCitySectorSentence(sector.name, selectedCity, rank)}
                        </li>
                        {Array.isArray(sector.reasons) && sector.reasons.map((reason, i) => (
                          <li key={i} className="reason-item">{reason}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
      
      {/* Boş durumlar */}
      {selectedSector && searchResults.length === 0 && !isLoading && (
        <div className="empty-message">
          <div className="empty-icon">📊</div>
          <h3>Veri Bulunamadı</h3>
          <p>{selectedSector} sektörü için şehir verisi bulunamadı.</p>
        </div>
      )}

      {selectedCity && citySearchResults.length === 0 && !cityIsLoading && (
        <div className="empty-message">
          <div className="empty-icon">📊</div>
          <h3>Veri Bulunamadı</h3>
          <p>{selectedCity} şehri için sektör verisi bulunamadı.</p>
        </div>
      )}
    </div>
  );
};

export default SectorSearch;
