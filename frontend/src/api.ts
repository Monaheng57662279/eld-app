const API_URL = import.meta.env.VITE_API_URL || "https://eld-app-1.onrender.com";

// Health check
export async function checkHealth() {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) {
    throw new Error("Backend health check failed");
  }
  return res.json();
}

// Trip planning
export async function fetchTripPlan(data: any) {
  const res = await fetch(`${API_URL}/plan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to fetch trip plan");
  }
  return res.json();
}
