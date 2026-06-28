const API_BASE = "http://localhost:8000";

// Helper to get headers with mock auth token
function getHeaders() {
  const token = localStorage.getItem("allergyguard_token");
  const headers = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

export async function fetchAllergens() {
  const res = await fetch(`${API_BASE}/api/allergens`);
  if (!res.ok) throw new Error("Failed to fetch allergens");
  return res.json();
}

export async function fetchSymptoms() {
  const res = await fetch(`${API_BASE}/api/symptoms`);
  if (!res.ok) throw new Error("Failed to fetch symptoms");
  return res.json();
}

export async function fetchFoods() {
  const res = await fetch(`${API_BASE}/api/foods`);
  if (!res.ok) throw new Error("Failed to fetch foods");
  return res.json();
}

export async function registerUser(email, password) {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Registration failed");
  }
  const data = await res.json();
  localStorage.setItem("allergyguard_token", data.token);
  localStorage.setItem("allergyguard_email", data.email);
  return data;
}

export async function loginUser(email, password) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }
  const data = await res.json();
  localStorage.setItem("allergyguard_token", data.token);
  localStorage.setItem("allergyguard_email", data.email);
  return data;
}

export function logoutUser() {
  localStorage.removeItem("allergyguard_token");
  localStorage.removeItem("allergyguard_email");
}

export async function fetchUserLogs() {
  const res = await fetch(`${API_BASE}/api/logs`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error("Failed to fetch history");
  return res.json();
}

export async function assessKnownAllergies(allergenIds) {
  const res = await fetch(`${API_BASE}/api/assess/known`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders()
    },
    body: JSON.stringify({ allergens: allergenIds })
  });
  if (!res.ok) throw new Error("Failed to run known allergy assessment");
  return res.json();
}

export async function assessUnknownAllergy(formData) {
  const headers = getHeaders();
  const res = await fetch(`${API_BASE}/api/assess/unknown`, {
    method: "POST",
    headers: headers, // Fetch handles Content-Type for FormData automatically
    body: formData
  });
  if (!res.ok) throw new Error("Failed to run risk assessment");
  return res.json();
}

export function getImageUrl(path) {
  if (!path) return "/placeholder-image.jpg";
  return `${API_BASE}${path}`;
}
