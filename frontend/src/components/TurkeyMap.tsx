import React, { useState } from 'react';
import Map, { Source, Layer, Popup, ViewState } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// Mapbox token'ı (ücretsiz hesap için)
// Gerçek uygulamada: process.env.REACT_APP_MAPBOX_TOKEN
const MAPBOX_TOKEN = 'pk.eyJ1IjoiYmFyYW5rb2NhIiwiYSI6ImNsZ3h4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4In0.example';

interface CityData {
  name: string;
  coordinates: [number, number];
  topSectors: Array<{
    sector: string;
    score: number;
  }>;
}

interface TurkeyMapProps {
  onCityClick?: (cityName: string) => void;
}

const TurkeyMap: React.FC<TurkeyMapProps> = ({ onCityClick }) => {
  const [viewState, setViewState] = useState({
    longitude: 35.243322,
    latitude: 38.963745,
    zoom: 5.5
  });

  const [selectedCity, setSelectedCity] = useState<CityData | null>(null);
  const [popupInfo, setPopupInfo] = useState<{
    longitude: number;
    latitude: number;
    cityName: string;
    topSectors: Array<{ sector: string; score: number }>;
  } | null>(null);

  // Türkiye illeri ve koordinatları (örnek veri)
  const cities: CityData[] = [
    {
      name: 'İstanbul',
      coordinates: [28.9784, 41.0082],
      topSectors: [
        { sector: 'Lojistik', score: 85.2 },
        { sector: 'Finans', score: 82.1 },
        { sector: 'Teknoloji', score: 78.9 },
        { sector: 'Turizm', score: 76.5 },
        { sector: 'Sağlık', score: 74.3 }
      ]
    },
    {
      name: 'Ankara',
      coordinates: [32.8597, 39.9334],
      topSectors: [
        { sector: 'Sosyal Hizmetler', score: 88.7 },
        { sector: 'Eğitim', score: 85.4 },
        { sector: 'Sağlık', score: 82.1 },
        { sector: 'Teknoloji', score: 79.8 },
        { sector: 'Lojistik', score: 76.2 }
      ]
    },
    {
      name: 'İzmir',
      coordinates: [27.1428, 38.4237],
      topSectors: [
        { sector: 'Turizm', score: 87.3 },
        { sector: 'Tarım', score: 84.6 },
        { sector: 'Lojistik', score: 81.9 },
        { sector: 'Eğitim', score: 78.4 },
        { sector: 'Sağlık', score: 75.8 }
      ]
    },
    {
      name: 'Bursa',
      coordinates: [29.0610, 40.1885],
      topSectors: [
        { sector: 'Sanayi', score: 89.1 },
        { sector: 'Otomotiv', score: 86.7 },
        { sector: 'Lojistik', score: 83.2 },
        { sector: 'Teknoloji', score: 80.5 },
        { sector: 'Eğitim', score: 77.8 }
      ]
    },
    {
      name: 'Antalya',
      coordinates: [30.7133, 36.8969],
      topSectors: [
        { sector: 'Turizm', score: 92.4 },
        { sector: 'Tarım', score: 85.7 },
        { sector: 'Sağlık', score: 82.3 },
        { sector: 'Eğitim', score: 79.1 },
        { sector: 'Lojistik', score: 76.8 }
      ]
    }
  ];

  const handleMapClick = (event: any) => {
    const feature = event.features && event.features[0];
    if (feature) {
      const cityName = feature.properties?.name;
      const city = cities.find(c => c.name === cityName);
      
      if (city) {
        setPopupInfo({
          longitude: event.lngLat.lng,
          latitude: event.lngLat.lat,
          cityName: city.name,
          topSectors: city.topSectors
        });
        
        if (onCityClick) {
          onCityClick(city.name);
        }
      }
    }
  };

  const cityLayer = {
    id: 'cities',
    type: 'circle' as const,
    paint: {
      'circle-radius': 8,
      'circle-color': '#4ecdc4',
      'circle-stroke-color': '#fff',
      'circle-stroke-width': 2,
      'circle-opacity': 0.8
    }
  };

  return (
    <div style={{ width: '100%', height: '500px', borderRadius: '15px', overflow: 'hidden' }}>
      <Map
        {...viewState}
        onMove={(evt: { viewState: ViewState }) => setViewState(evt.viewState)}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/light-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
        onClick={handleMapClick}
        interactiveLayerIds={['cities']}
      >
        {/* Türkiye sınırları */}
        <Source
          id="turkey-boundaries"
          type="vector"
          url="mapbox://mapbox.country-boundaries-v1"
        >
          <Layer
            id="turkey-fill"
            type="fill"
            source-layer="country_boundaries"
            filter={['==', 'name_en', 'Turkey']}
            paint={{
              'fill-color': 'rgba(255, 255, 255, 0.1)',
              'fill-outline-color': '#4ecdc4'
            }}
          />
        </Source>

        {/* İl noktaları */}
        <Source
          id="cities-source"
          type="geojson"
          data={{
            type: 'FeatureCollection',
            features: cities.map(city => ({
              type: 'Feature',
              geometry: {
                type: 'Point',
                coordinates: city.coordinates
              },
              properties: {
                name: city.name,
                topSectors: city.topSectors
              }
            }))
          }}
        >
          <Layer {...cityLayer} />
        </Source>

        {/* Popup */}
        {popupInfo && (
          <Popup
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            anchor="bottom"
            onClose={() => setPopupInfo(null)}
            closeButton={true}
            closeOnClick={false}
            style={{
              background: 'rgba(255, 255, 255, 0.95)',
              borderRadius: '10px',
              padding: '0',
              border: 'none',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)'
            }}
          >
            <div style={{ padding: '15px', minWidth: '200px' }}>
              <h3 style={{ 
                margin: '0 0 10px 0', 
                color: '#4ecdc4', 
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                {popupInfo.cityName}
              </h3>
              <h4 style={{ 
                margin: '0 0 8px 0', 
                color: '#333', 
                fontSize: '14px',
                fontWeight: '600'
              }}>
                En İyi Sektörler:
              </h4>
              <ul style={{ 
                margin: '0', 
                padding: '0', 
                listStyle: 'none',
                fontSize: '12px'
              }}>
                {popupInfo.topSectors.map((sector, index) => (
                  <li key={index} style={{ 
                    margin: '4px 0',
                    padding: '4px 8px',
                    background: 'rgba(78, 205, 196, 0.1)',
                    borderRadius: '4px',
                    display: 'flex',
                    justifyContent: 'space-between'
                  }}>
                    <span>{sector.sector}</span>
                    <span style={{ fontWeight: 'bold', color: '#4ecdc4' }}>
                      {sector.score.toFixed(1)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </Popup>
        )}
      </Map>
    </div>
  );
};

export default TurkeyMap;
