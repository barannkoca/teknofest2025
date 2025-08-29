import React, { useState } from 'react';
import './App.css';
import TurkeyMap from './components/TurkeyMap';

function App() {
  const [selectedCity, setSelectedCity] = useState<string>('');

  const handleCityClick = (cityName: string) => {
    setSelectedCity(cityName);
    console.log(`Seçilen şehir: ${cityName}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌱 ECOMINDS</h1>
        <p>İl ve Sektör Bazlı Karar Destek Sistemi</p>
        <p>Teknofest 2025</p>
      </header>

      <main className="App-main">
        <section className="hero-section">
          <h2>Eco-friendly Business Scoring API</h2>
          <p>81 ili 14 normalize gösterge ile 20 sektör açısından sayısal olarak puanlayan ve iki yönlü öneri veren karar destek sistemi</p>
        </section>

        <section className="map-section">
          <h2>🗺️ Türkiye Haritası</h2>
          <p>İllere tıklayarak en iyi sektörlerini görün</p>
          <TurkeyMap onCityClick={handleCityClick} />
          {selectedCity && (
            <div className="selected-city-info">
              <h3>Seçilen Şehir: {selectedCity}</h3>
              <p>Bu şehrin detaylı sektör analizi için API entegrasyonu yapılacak.</p>
            </div>
          )}
        </section>

        <section className="features-section">
          <div className="feature-card">
            <h3>📊 Mod-1: Sektör → İl</h3>
            <p>Bir sektör seçildiğinde 81 ilin o sektör için puanını hesaplar ve en iyi 5 ili sıralar</p>
          </div>
          
          <div className="feature-card">
            <h3>🏙️ Mod-2: İl → Sektör</h3>
            <p>Bir il seçildiğinde 20 sektörün o il için puanını hesaplar ve en iyi 5 sektörü sıralar</p>
          </div>
          
          <div className="feature-card">
            <h3>⚖️ YÖN Dönüşümü</h3>
            <p>Her kriter için "Yüksek" veya "Düşük" avantaj kuralları</p>
          </div>
          
          <div className="feature-card">
            <h3>📈 Ağırlıklı Skorlama</h3>
            <p>Sektöre özel kriter ağırlıkları ile hesaplama</p>
          </div>
        </section>

        <section className="results-section">
          <h2>📋 Sonuçlar</h2>
          <div className="results-grid">
            <div className="result-card">
              <h3>En Yüksek Ortalama Skorlu Sektörler</h3>
              <ol>
                <li>Lojistik: 63.7</li>
                <li>Sosyal Hizmetler: 50.8</li>
                <li>Ulaşım: 44.8</li>
                <li>Sağlık: 44.5</li>
                <li>Sanayi / Üretim: 43.8</li>
              </ol>
            </div>
            
            <div className="result-card">
              <h3>En Yüksek Ortalama Skorlu İller</h3>
              <ol>
                <li>İstanbul: 54.9</li>
                <li>Ankara: 52.4</li>
                <li>Bursa: 49.4</li>
                <li>Konya: 48.9</li>
                <li>Kocaeli: 48.6</li>
              </ol>
            </div>
          </div>
        </section>

        <section className="stats-section">
          <h2>📊 İstatistikler</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>19</h3>
              <p>Sektör</p>
            </div>
            <div className="stat-card">
              <h3>81</h3>
              <p>İl</p>
            </div>
            <div className="stat-card">
              <h3>1,539</h3>
              <p>Toplam Hesaplama</p>
            </div>
            <div className="stat-card">
              <h3>4</h3>
              <p>CSV Dosyası</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="App-footer">
        <p>© 2025 ECOMINDS - Teknofest 2025 Yarışması</p>
        <p>Backend: FastAPI (Python) | Frontend: React (TypeScript) | Harita: Mapbox</p>
      </footer>
    </div>
  );
}

export default App;
