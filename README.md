# ELD Trip Planner (Django + React)

A minimal full‑stack demo that takes trip details and outputs:
- A map with route and stop information (OpenStreetMap + OSRM)
- Generated Hours-of-Service daily log sheets (SVG)

## Tech
- **Backend:** Django, simple JSON API, external services: Nominatim (geocoding), OSRM (routing)
- **Frontend:** React + Vite + Tailwind, react‑leaflet for maps

> Assumptions implemented: property-carrying 70hr/8days, 11h driving/day, 14h on-duty window, 30‑min break before 8h driving, 10h off‑duty between shifts, 1h pickup & drop-off, fueling every 1000 miles (30min on-duty).

---

## Local Dev

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm i
npm run dev
```

- Adjust `VITE_BACKEND_URL` in `frontend/.env` (or set env var) to point to your backend (default `http://localhost:8000`).

---

## Deployment

### Option A: Frontend on **Vercel**, Backend on **Render** (or Railway/Fly)
1. **Backend**
   - Push `/backend` to a new GitHub repo or folder.
   - Create a new **Render** Web Service from that repo.
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `cd backend && gunicorn planner.wsgi:application -c gunicorn.conf.py`
   - Environment:
     - `DJANGO_SECRET_KEY` = (random)
     - `DJANGO_DEBUG` = `0`
     - `ALLOWED_HOSTS` = `*`
     - Optional: `CORS_ALLOWED_ORIGINS` = `https://<your-vercel-domain>`
   - Note the backend URL, e.g. `https://your-backend.onrender.com`

2. **Frontend**
   - In Vercel, import the `/frontend` folder (or separate repo).
   - Add env var `VITE_BACKEND_URL` set to your backend URL.
   - Deploy. After completion, open the site and test.

> You can also deploy the backend using the included `Dockerfile.backend` on any container platform.

### Health Check
- `GET /api/health` should return `{ "ok": true }`

### Plan API
`POST /api/plan`

```json
{
  "currentLocation": "Amarillo, TX",
  "pickup": "Oklahoma City, OK",
  "dropoff": "Atlanta, GA",
  "currentCycleUsedHours": 5
}
```

Response includes `route.path` (lat/lon points) and `schedule` segments.

---

## Notes / Limits

- Uses public Nominatim + OSRM endpoints; rate‑limited and not guaranteed for production. For a production key, consider **OpenRouteService** or hosting OSRM yourself.
- ELD logs are **approximations** driven by route duration and HOS rules; they’re for demo use, not legal compliance.
- CORS is permissive by default for demo; lock it down in production.
- Timezone handling is UTC internally; the UI renders in the user’s local time.

---

## Project Structure

```
truck-planner/
├── backend/ (Django API)
└── frontend/ (React app)
```

Happy trucking!
