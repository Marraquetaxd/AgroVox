"use client";

import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Icono para Nodos
const crearIconoNodo = (estado: string) => L.divIcon({
  className: 'custom-leaflet-icon',
  html: `<div class="relative flex h-5 w-5 items-center justify-center">
           ${estado === 'alerta' ? '<span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75"></span>' : ''}
           <span class="relative inline-flex h-3 w-3 rounded-full ${estado === 'alerta' ? 'bg-red-500' : 'bg-agrogreen-500'} shadow-lg border border-white z-10"></span>
         </div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10],
});

// Icono para el Gateway (Antena Central)
const iconoGateway = L.divIcon({
  className: 'custom-leaflet-icon',
  html: `<div class="relative flex h-8 w-8 items-center justify-center">
           <span class="relative inline-flex h-4 w-4 rounded-full bg-blue-500 shadow-lg border-2 border-white z-10"></span>
         </div>`,
  iconSize: [32, 32],
  iconAnchor: [16, 16],
});

// Coordenadas simuladas del polígono de riego (Sector 1)
const coordenadasSector: [number, number][] = [
  [-34.170, -70.740],
  [-34.170, -70.735],
  [-34.175, -70.735],
  [-34.175, -70.740],
];

export default function MapaTopografico() {
  const centro: [number, number] = [-34.1725, -70.7375];

  return (
    <MapContainer center={centro} zoom={16} className="w-full h-full z-0">
      {/* Capa Satelital de Esri */}
      <TileLayer
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        attribution='&copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
      />
      
      {/* Polígono del Sector de Riego */}
      <Polygon 
        positions={coordenadasSector} 
        pathOptions={{ color: '#22c55e', fillColor: '#22c55e', fillOpacity: 0.2, weight: 2 }} 
      />

      {/* Gateway Principal */}
      <Marker position={[-34.172, -70.738]} icon={iconoGateway}>
        <Popup className="rounded-lg"><span className="font-bold text-blue-600">Gateway LoRa Central</span><br/>Caseta de Riego</Popup>
      </Marker>

      {/* Nodos IoT */}
      <Marker position={[-34.171, -70.739]} icon={crearIconoNodo('ok')}>
        <Popup className="rounded-lg"><span className="font-bold">AGV-010</span><br/>Batería: 98%</Popup>
      </Marker>
      <Marker position={[-34.174, -70.736]} icon={crearIconoNodo('alerta')}>
        <Popup className="rounded-lg"><span className="font-bold text-red-600">AGV-011 (Alerta)</span><br/>Cavitación Detectada</Popup>
      </Marker>
    </MapContainer>
  );
}