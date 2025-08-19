import React, { useMemo } from "react"
import dayjs from "dayjs"

type Seg = { start:string; end:string; status:string; label:string }

const ROWS = ["OFF_DUTY", "SLEEPER", "DRIVING", "ON_DUTY"] as const

function xFor(dt: dayjs.Dayjs, dayStart: dayjs.Dayjs, width: number){
  const minutes = dt.diff(dayStart, "minute")
  return Math.max(0, Math.min(width, (minutes/ (24*60)) * width))
}

export default function ELDLog({ schedule }:{ schedule: Seg[] }){
  // Group segments by day (local time of viewer)
  const byDay = useMemo(()=>{
    const map = new Map<string, Seg[]>()
    for (const s of schedule){
      const d = dayjs(s.start).format("YYYY-MM-DD")
      if (!map.has(d)) map.set(d, [])
      map.get(d)!.push(s)
    }
    return Array.from(map.entries()).sort(([a],[b])=> a<b ? -1 : 1)
  }, [schedule])

  return (
    <div className="space-y-6">
      {byDay.map(([day, segs])=> (
        <DayLog key={day} day={day} segs={segs} />
      ))}
      {!byDay.length && <div className="text-sm text-slate-500">Plan a trip to see logs.</div>}
    </div>
  )
}

function DayLog({ day, segs }:{ day:string; segs: Seg[] }){
  const width = 900, height = 200, rowH = height / ROWS.length
  const dayStart = dayjs(day + "T00:00:00")
  const dayEnd = dayStart.add(1, "day")

  // Expand segments clipped to this day
  const segments = useMemo(()=>{
    return segs.map(s=>{
      const s0 = dayjs(s.start); const s1 = dayjs(s.end)
      const start = s0.isBefore(dayStart) ? dayStart : s0
      const end = s1.isAfter(dayEnd) ? dayEnd : s1
      return {...s, start: start.toISOString(), end: end.toISOString()}
    }).filter(s=> dayjs(s.start).isBefore(dayEnd) && dayjs(s.end).isAfter(dayStart))
  }, [segs, day])

  function yFor(status:string){
    const idx = status === "OFF_DUTY" ? 0 : status === "SLEEPER" ? 1 : status === "DRIVING" ? 2 : 3
    return (idx + 0.5) * rowH
  }

  return (
    <div className="space-y-2">
      <div className="font-medium">{dayjs(day).format("MMMM D, YYYY")}</div>
      <svg width={width} height={height} className="w-full">
        {/* grid */}
        {ROWS.map((_, i)=> (
          <line key={i} x1={0} x2={width} y1={(i+1)*rowH} y2={(i+1)*rowH} stroke="#e2e8f0" />
        ))}
        {Array.from({length:25}).map((_,i)=> (
          <line key={i} x1={(i/24)*width} x2={(i/24)*width} y1={0} y2={height} stroke="#f1f5f9" />
        ))}
        {/* labels left */}
        {ROWS.map((r,i)=> (
          <text key={i} x={4} y={(i+0.8)*rowH} fontSize={12} fill="#334155">{r.replace("_"," ")}</text>
        ))}
        {/* hour labels */}
        {Array.from({length:25}).map((_,i)=> (
          <text key={i} x={(i/24)*width+2} y={12} fontSize={10} fill="#64748b">{i}</text>
        ))}
        {/* segments */}
        {segments.map((s,i)=> {
          const sx = xFor(dayjs(s.start), dayStart, width)
          const ex = xFor(dayjs(s.end), dayStart, width)
          const y = yFor(s.status)
          return (
            <g key={i}>
              <line x1={sx} x2={ex} y1={y} y2={y} stroke="#0f172a" strokeWidth={3}/>
              <circle cx={sx} cy={y} r={3} fill="#0f172a" />
              <circle cx={ex} cy={y} r={3} fill="#0f172a" />
              <text x={(sx+ex)/2} y={y-6} textAnchor="middle" fontSize={10} fill="#334155">{s.label}</text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
