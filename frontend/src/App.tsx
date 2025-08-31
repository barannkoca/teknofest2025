import React, { useState } from 'react';
import './App.css';
import TurkeyMap from './components/TurkeyMap';
import SectorSearch from './components/SectorSearch';

function App() {
  const [selectedCity, setSelectedCity] = useState<string>('');

  const handleCityClick = (cityName: string) => {
    setSelectedCity(cityName);
    console.log(`Seçilen şehir: ${cityName}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MIYE</h1>
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
          <TurkeyMap />
        </section>

        <section className="sector-search-section">
          <SectorSearch />
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
