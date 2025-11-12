import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './Map.module.css';

const Map: React.FC = () => {
  return (
    <MapContainer center={[27.7,85.3]} zoom={12} style={{height:'calc(100vh - 56px)', width:'100%'}}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
    </MapContainer>
  );
};

export default Map;