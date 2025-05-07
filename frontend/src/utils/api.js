// src/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL; // Vite
// const API_BASE_URL = process.env.REACT_APP_API_BASE_URL; // CRA

// Helper to get the auth token from localStorage (or context)
function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Signup
export async function signup({ email, password, full_name }) {
  const res = await fetch(`${API_BASE_URL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, full_name }),
  });
  if (!res.ok) throw await res.json();
  return res.json();
}

// Login
export async function login({ email, password }) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password }),
  });
  if (!res.ok) throw await res.json();
  return res.json();
}

// Get Teams
export async function getTeams() {
  const res = await fetch(`${API_BASE_URL}/teams`, {
    headers: { ...getAuthHeaders() },
  });
  if (!res.ok) throw await res.json();
  return res.json();
}

// Create Team
export async function createTeam(team) {
  const res = await fetch(`${API_BASE_URL}/teams`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    body: JSON.stringify(team),
  });
  if (!res.ok) throw await res.json();
  return res.json();
}

// Uploading Problem File
export async function uploadProblems(file, teamId) {
  const formData = new FormData();
  formData.append('file', file);
  const url = teamId
    ? `${API_BASE_URL}/problems/upload?team_id=${teamId}`
    : `${API_BASE_URL}/problems/upload`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { ...getAuthHeaders() },
    body: formData,
  });
  if (!res.ok) throw await res.json();
  return res.json();
}