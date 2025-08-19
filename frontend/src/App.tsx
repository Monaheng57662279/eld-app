import React, { useState } from "react"
import MapView from "./components/MapView"
import ELDLog from "./components/ELDLog"

type PlanResponse = {
  ok: boolean
  locations: any
  route: { distance_m: number; duration_s: number; path: {lat:number,lon:number}[] }
  schedule: any[]
}

export default function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<PlanResponse | null>(null)
  const [form, setForm] = useState({
    currentLocation: "",
    pickup: "",
    dropoff: "",
    currentCycleUsedHours: 0,
  })

  const backend = (import.meta as any).env.VITE_BACKEND_URL || "http://localhost:8000"

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setError(null); setLoading(true)
    try {
      const res = await fetch(`${backend}/api/plan`, {
        method: "POST",
        headers: { "Content-Type":"application/json" },
        body: JSON.stringify(form)
      })
      const json = await res.json()
      if (!res.ok) throw new Error(json.error || "Failed to plan")
      setData(json)
    } catch (err:any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <header className="p-4 border-b bg-white">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="h1">ELD Trip Planner</div>
          <div className="badge">Property-carrying • 70hr/8d</div>
        </div>
      </header>

      <main className="flex-1">
        <div className="max-w-6xl mx-auto p-4 grid gap-4 lg:grid-cols-3">
          <section className="card lg:col-span-1">
            <div className="h2 mb-3">Trip Details</div>
            <form className="space-y-3" onSubmit={submit}>
              <div>
                <div className="label">Current location</div>
                <input className="input" placeholder="e.g., Amarillo, TX" value={form.currentLocation}
                       onChange={e=>setForm({...form, currentLocation:e.target.value})}/>
              </div>
              <div>
                <div className="label">Pickup</div>
                <input className="input" placeholder="e.g., Oklahoma City, OK" value={form.pickup}
                       onChange={e=>setForm({...form, pickup:e.target.value})}/>
              </div>
              <div>
                <div className="label">Dropoff</div>
                <input className="input" placeholder="e.g., Atlanta, GA" value={form.dropoff}
                       onChange={e=>setForm({...form, dropoff:e.target.value})}/>
              </div>
              <div>
                <div className="label">Current cycle used (hrs)</div>
                <input className="input" type="number" min={0} max={70} step={0.5}
                       value={form.currentCycleUsedHours}
                       onChange={e=>setForm({...form, currentCycleUsedHours: Number(e.target.value)})}/>
              </div>
              <button className="btn" disabled={loading}>
                {loading ? "Planning..." : "Plan Route"}
              </button>
              {error && <div className="text-red-600 text-sm">{error}</div>}
            </form>
          </section>

          <section className="lg:col-span-2 grid gap-4">
            <div className="card" style={{height: 400}}>
              <div className="h2 mb-2">Route</div>
              <MapView path={data?.route?.path || []} schedule={data?.schedule || []} />
            </div>
            <div className="card">
              <div className="h2 mb-2">Daily Log Sheets</div>
              <ELDLog schedule={data?.schedule || []} />
            </div>
          </section>
        </div>
      </main>

      <footer className="p-4 text-center text-xs text-slate-500">
        Built with OpenStreetMap + OSRM • Demo use only
      </footer>
    </div>
  )
}
