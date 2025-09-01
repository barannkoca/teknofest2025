import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

interface CityData {
  name: string;
  coordinates: [number, number];
}

interface SectorData {
  name: string;
  score: number;
  reasons: string[];
}

const TurkeyMap: React.FC = () => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const currentPopup = useRef<mapboxgl.Popup | null>(null);

  // Şehir için sektör verilerini backend'den al
  const getSectorsForCity = async (cityName: string): Promise<SectorData[]> => {
    try {
      // Şehir ismini URL'de encode et
      const encodedCityName = encodeURIComponent(cityName);
      const response = await fetch(`http://localhost:8000/api/mod2?city=${encodedCityName}&topn=5`);
      if (!response.ok) {
        throw new Error('Veri alınamadı');
      }
      const data = await response.json();
      return data.top5 || [];
    } catch (error) {
      console.error('Sektör verisi alınırken hata:', error);
      return [];
    }
  };

  // Türkiye illeri ve koordinatları
  const cities: CityData[] = [
    { name: 'Adana', coordinates: [35.3213, 37.0000] },
    { name: 'Adıyaman', coordinates: [38.2784, 37.7648] },
    { name: 'Afyonkarahisar', coordinates: [30.5456, 38.7507] },
    { name: 'Ağrı', coordinates: [43.0503, 39.7191] },
    { name: 'Aksaray', coordinates: [34.0297, 38.3726] },
    { name: 'Amasya', coordinates: [35.8333, 40.6499] },
    { name: 'Ankara', coordinates: [32.8597, 39.9334] },
    { name: 'Antalya', coordinates: [30.7133, 36.8969] },
    { name: 'Ardahan', coordinates: [42.7023, 41.1105] },
    { name: 'Artvin', coordinates: [41.8183, 41.1828] },
    { name: 'Aydın', coordinates: [27.8456, 37.8560] },
    { name: 'Balıkesir', coordinates: [27.8903, 39.6484] },
    { name: 'Bartın', coordinates: [32.3375, 41.6344] },
    { name: 'Batman', coordinates: [41.1292, 37.8812] },
    { name: 'Bayburt', coordinates: [40.2552, 40.2552] },
    { name: 'Bilecik', coordinates: [29.9792, 40.1451] },
    { name: 'Bingöl', coordinates: [40.4983, 38.8855] },
    { name: 'Bitlis', coordinates: [42.1093, 38.4006] },
    { name: 'Bolu', coordinates: [31.6082, 40.7397] },
    { name: 'Burdur', coordinates: [30.2868, 37.7205] },
    { name: 'Bursa', coordinates: [29.0610, 40.1885] },
    { name: 'Çanakkale', coordinates: [26.4086, 40.1553] },
    { name: 'Çankırı', coordinates: [33.6167, 40.6013] },
    { name: 'Çorum', coordinates: [34.9537, 40.5499] },
    { name: 'Denizli', coordinates: [29.0963, 37.7765] },
    { name: 'Diyarbakır', coordinates: [40.2346, 37.9144] },
    { name: 'Düzce', coordinates: [31.1626, 40.8438] },
    { name: 'Edirne', coordinates: [26.5557, 41.6771] },
    { name: 'Elazığ', coordinates: [39.2233, 38.6810] },
    { name: 'Erzincan', coordinates: [39.4903, 39.7500] },
    { name: 'Erzurum', coordinates: [41.2763, 39.9055] },
    { name: 'Eskişehir', coordinates: [30.5206, 39.7767] },
    { name: 'Gaziantep', coordinates: [37.3781, 37.0662] },
    { name: 'Giresun', coordinates: [38.3927, 40.9128] },
    { name: 'Gümüşhane', coordinates: [39.4814, 40.4603] },
    { name: 'Hakkari', coordinates: [43.7408, 37.5742] },
    { name: 'Hatay', coordinates: [36.1626, 36.2023] },
    { name: 'Iğdır', coordinates: [44.0442, 39.9167] },
    { name: 'Isparta', coordinates: [30.5536, 37.7648] },
    { name: 'İstanbul', coordinates: [28.9784, 41.0082] },
    { name: 'İzmir', coordinates: [27.1428, 38.4237] },
    { name: 'Kahramanmaraş', coordinates: [36.9228, 37.5858] },
    { name: 'Karabük', coordinates: [32.6277, 41.2061] },
    { name: 'Karaman', coordinates: [33.2154, 37.1759] },
    { name: 'Kars', coordinates: [43.0975, 40.6013] },
    { name: 'Kastamonu', coordinates: [33.7760, 41.3887] },
    { name: 'Kayseri', coordinates: [35.4889, 38.7205] },
    { name: 'Kırıkkale', coordinates: [33.5067, 39.8453] },
    { name: 'Kırklareli', coordinates: [27.2261, 41.7355] },
    { name: 'Kırşehir', coordinates: [34.1728, 39.1425] },
    { name: 'Kilis', coordinates: [37.1147, 36.7184] },
    { name: 'Kocaeli', coordinates: [29.9187, 40.8533] },
    { name: 'Konya', coordinates: [32.4847, 37.8667] },
    { name: 'Kütahya', coordinates: [29.9833, 39.4167] },
    { name: 'Malatya', coordinates: [38.3552, 38.3552] },
    { name: 'Manisa', coordinates: [27.4286, 38.6191] },
    { name: 'Mardin', coordinates: [40.7436, 37.3212] },
    { name: 'Mersin', coordinates: [34.6415, 36.8121] },
    { name: 'Muğla', coordinates: [28.3665, 37.2154] },
    { name: 'Muş', coordinates: [41.4911, 38.7432] },
    { name: 'Nevşehir', coordinates: [34.7144, 38.6244] },
    { name: 'Niğde', coordinates: [34.6764, 37.9667] },
    { name: 'Ordu', coordinates: [37.8797, 40.9862] },
    { name: 'Osmaniye', coordinates: [36.2479, 37.0742] },
    { name: 'Rize', coordinates: [40.5219, 41.0201] },
    { name: 'Sakarya', coordinates: [30.4033, 40.7569] },
    { name: 'Samsun', coordinates: [36.3361, 41.2867] },
    { name: 'Siirt', coordinates: [41.9417, 37.9333] },
    { name: 'Sinop', coordinates: [35.1551, 42.0231] },
    { name: 'Sivas', coordinates: [37.0150, 39.7477] },
    { name: 'Şanlıurfa', coordinates: [38.7955, 37.1591] },
    { name: 'Şırnak', coordinates: [42.4542, 37.5164] },
    { name: 'Tekirdağ', coordinates: [27.5111, 40.9781] },
    { name: 'Tokat', coordinates: [36.5541, 40.3167] },
    { name: 'Trabzon', coordinates: [39.7168, 41.0015] },
    { name: 'Tunceli', coordinates: [39.5444, 39.1079] },
    { name: 'Uşak', coordinates: [29.4058, 38.6742] },
    { name: 'Van', coordinates: [43.4089, 38.4891] },
    { name: 'Yalova', coordinates: [29.2769, 40.6500] },
    { name: 'Yozgat', coordinates: [34.8083, 39.8181] },
    { name: 'Zonguldak', coordinates: [31.7937, 41.4564] }
  ];

  useEffect(() => {
    if (map.current) return; // initialize map only once
    
    mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN;
    
    map.current = new mapboxgl.Map({
      container: mapContainer.current!,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [35.243322, 38.963745], // Türkiye merkezi
      zoom: 5
    });

    // Harita yüklendiğinde pin'leri ekle
    map.current.on('load', () => {
      console.log('Harita yüklendi, pin\'ler ekleniyor...');
      
      // Her şehir için pin ekle
      cities.forEach(city => {
        // Pin elementi oluştur
        const el = document.createElement('div');
        el.className = 'city-marker';
        el.style.width = '20px';
        el.style.height = '20px';
        el.style.borderRadius = '50%';
        el.style.backgroundColor = '#4ecdc4';
        el.style.border = '2px solid white';
        el.style.cursor = 'pointer';
        el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';

        // Pin'i haritaya ekle
        const marker = new mapboxgl.Marker(el)
          .setLngLat(city.coordinates)
          .addTo(map.current!);

        // Pin'e tıklama olayı ekle
        marker.getElement().addEventListener('click', async () => {
          console.log(`${city.name} tıklandı!`);
          
          // Önceki popup'ı kapat
          if (currentPopup.current) {
            currentPopup.current.remove();
            currentPopup.current = null;
          }

          // Şehir için sektör verilerini backend'den al
          const citySectors = await getSectorsForCity(city.name);
          
          // Popup HTML'ini oluştur
          let popupHTML = `
            <div style="padding: 10px; min-width: 200px; max-width: 220px;">
              <h3 style="margin: 0 0 8px 0; color: #4ecdc4; font-size: 14px; font-weight: bold; text-align: center;">
                ${city.name}
              </h3>
              <h4 style="margin: 0 0 6px 0; color: #333; font-size: 11px; font-weight: bold;">
                🏆 En İyi 5 Sektör
              </h4>
          `;

          if (citySectors.length > 0) {
            citySectors.forEach((sector: SectorData, index: number) => {
              const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅';
              popupHTML += `
                <div style="margin: 4px 0; padding: 5px; background: #f8f9fa; border-radius: 4px; border-left: 2px solid #4ecdc4;">
                  <div style="display: flex; justify-content: space-between; align-items: center; gap: 5px;">
                    <span style="font-size: 12px; flex-shrink: 0;">${medal}</span>
                    <span style="font-weight: bold; color: #333; font-size: 10px; flex: 1; text-align: left; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${sector.name}</span>
                    <span style="font-weight: bold; color: #4ecdc4; font-size: 10px; flex-shrink: 0;">${sector.score.toFixed(1)}</span>
                  </div>
                </div>
              `;
            });
          } else {
            popupHTML += `
              <div style="text-align: center; color: #666; font-style: italic; padding: 10px 0; font-size: 10px;">
                Bu şehir için sektör verisi bulunamadı
              </div>
            `;
          }

          popupHTML += '</div>';

          // Yeni popup oluştur
          const newPopup = new mapboxgl.Popup({ 
            closeButton: true,
            closeOnClick: false,
            maxWidth: '240px'
          })
            .setLngLat(city.coordinates)
            .setHTML(popupHTML);

          // Popup'ı haritaya ekle
          newPopup.addTo(map.current!);
          currentPopup.current = newPopup;
        });
      });
    });

  }, []);

  return (
    <div style={{ width: '100%', height: '500px', borderRadius: '15px', overflow: 'hidden' }}>
      <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />
    </div>
  );
};

export default TurkeyMap;
