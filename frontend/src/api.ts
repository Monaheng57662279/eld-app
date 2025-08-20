const API_URL = import.meta.env.VITE_BACKEND_URL;

export async function fetchTripPlan(data: any) {
  const response = await fetch(`${API_URL}/api/plan-trip/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch trip plan");
  }
  return response.json();
}
