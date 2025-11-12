import React, { FC } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { LatLngExpression } from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Approximate coordinates for Bhaktapur (Latitude, Longitude)
const BHAKTAPUR_CENTER: LatLngExpression = [27.671, 85.435];
const INITIAL_ZOOM: number = 13;

interface MapComponentProps {
  // You can pass props here for dynamic data, like locations or styles
}

const MapComponent: FC<MapComponentProps> = () => {
  return (
    // 1. MapContainer is the main component that creates the Leaflet map instance
    <MapContainer 
      center={BHAKTAPUR_CENTER} 
      zoom={INITIAL_ZOOM} 
      // Ensure the container has a defined height, otherwise the map won't display
      style={{ height: '89vh', width: '100%' }} 
      scrollWheelZoom={true} 
    >
      
      {/* 2. TileLayer adds the visual map tiles (the background) */}
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />

      {/* 3. Add a Marker for a Point of Interest (like a hotel) */}
      <Marker position={BHAKTAPUR_CENTER}>
        <Popup>
          A simple marker in **Bhaktapur**!
          <br />
          This can hold more information.
        </Popup>
      </Marker>
      
      {/* To replicate the look of your image, you would add more Marker components
          or use other Leaflet features like Circle, Polygon, or GeoJSON layers 
          to display the various points like 'Restaurants', 'Hotels', etc. */}

    </MapContainer>
  );
};

export default MapComponent;