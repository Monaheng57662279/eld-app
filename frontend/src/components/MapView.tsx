import React, { useMemo } from "react"
import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet"
import L from "leaflet"

type Pt = {lat:number, lon:number}

export default function MapView({ path, schedule }:{ path: Pt[], schedule:any[] }){
  const center = useMemo(()=> path.length ? [path[0].lat, path[0].lon] : [39.5,-98.35], [path])
  const polyline = useMemo(()=> path.map(p=>[p.lat, p.lon]) as [number,number][], [path])

  const drivingStops = schedule.filter((s:any)=> s.label === "Driving" && s.lat && s.lon)

  return (
    <MapContainer center={center as any} zoom={5} scrollWheelZoom className="rounded-xl overflow-hidden" style={{height:"100%"}}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {polyline.length > 1 && <Polyline positions={polyline as any} />}
      {drivingStops.map((s:any, i:number)=> (
        <Marker key={i} position={[s.lat, s.lon] as any} icon={L.icon({iconUrl:'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png', iconSize:[25,41], iconAnchor:[12,41]})}>
          <Popup>
            <div className="text-sm">
              <div className="font-medium">{s.label}</div>
              <div>Ends: {new Date(s.end).toLocaleString()}</div>
              <div>Status: {s.status}</div>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
