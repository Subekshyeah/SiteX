import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { LatLngExpression } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './Map.module.css';

const BHAKTAPUR_CENTER: LatLngExpression = [27.671, 85.435];

const Map: React.FC = () => {
  return (
    <MapContainer
      center={BHAKTAPUR_CENTER}
      zoom={13}
      style={{ height: 'calc(100vh - 56px)', width: '100%' }}
      scrollWheelZoom
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />

      <Marker position={BHAKTAPUR_CENTER}>
        <Popup>
          A simple marker in Bhaktapur!
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default Map;