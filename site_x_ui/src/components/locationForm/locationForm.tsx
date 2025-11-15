"use client";

import { useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { MapPin } from "lucide-react";
import * as L from "leaflet";

// Fix Leaflet default icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function MapPicker({
  lat,
  lng,
  setLat,
  setLng,
}: {
  lat: number;
  lng: number;
  setLat: (v: number) => void;
  setLng: (v: number) => void;
}) {
  function MapEvents() {
    useMapEvents({
      click(e) {
        setLat(Number(e.latlng.lat.toFixed(6)));
        setLng(Number(e.latlng.lng.toFixed(6)));
      },
    });
    return null;
  }

  return (
    <>
      <MapEvents />
      {lat && lng && <Marker position={[lat, lng]} />}
    </>
  );
}

export default function LocationForm() {
  const [lat, setLat] = useState<number>(27.7172); // Kathmandu
  const [lng, setLng] = useState<number>(85.3240);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({ name, email, address, lat, lng });
    alert(`Submitted!\nLat: ${lat}\nLng: ${lng}`);
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-gray-50">
      {/* ---------- LEFT SIDE – FORM (full height) ---------- */}
      <div className="w-full md:w-96 bg-white shadow-lg overflow-y-auto p-8 md:p-10 flex-shrink-0 border-r">
        <Card className="border-0 shadow-none">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-3 text-2xl font-semibold">
              <MapPin className="w-6 h-6" />
              Location Analysis
            </CardTitle>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <Label htmlFor="name">Cafe Name</Label>
                <Input
                  id="name"
                  placeholder="Napang Chussa Tonewa"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="mt-1"
                />
              </div>

              {/* <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="john@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="mt-1"
                />
              </div> */}

        

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="lat">Latitude</Label>
                  <Input
                    id="lat"
                    value={lat.toFixed(6)}
                    readOnly
                    className="mt-1 bg-muted font-mono text-sm"
                  />
                </div>
                <div>
                  <Label htmlFor="lng">Longitude</Label>
                  <Input
                    id="lng"
                    value={lng.toFixed(6)}
                    readOnly
                    className="mt-1 bg-muted font-mono text-sm"
                  />
                </div>
              </div>

              <Button type="submit" className="w-full py-3">
                Submit Location
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* ---------- RIGHT SIDE – FULL-SCREEN MAP ---------- */}
      <div className="flex-1 relative min-h-[480px]">
        <MapContainer
          center={[lat, lng]}
          zoom={13}
          className="h-full w-full"
          scrollWheelZoom
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          />
          <MapPicker lat={lat} lng={lng} setLat={setLat} setLng={setLng} />
        </MapContainer>

        {/* Optional overlay info */}
        <div className="absolute top-4 left-4 z-10 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-md shadow text-sm font-medium">
          Click map to set coordinates
        </div>
      </div>
    </div>
  );
}