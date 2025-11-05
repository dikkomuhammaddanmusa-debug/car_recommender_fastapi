import axios from "axios";
export const API_URL = "http://192.168.1.135:8000";
export const api = axios.create({
  baseURL: API_URL,
  timeout: 20000,
  headers: { "Content-Type": "application/json" },
});
export const getHealth = () => api.get("/api/v1/health");
export const searchCars = (params) => api.get("/api/v1/cars/search", { params });
export const recommendCars = (body) => api.post("/api/v1/cars/recommend", body);
export const getStats = () => api.get("/api/v1/stats");
