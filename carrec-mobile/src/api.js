import axios from "axios";
export const API_URL = "https://carrec-api-dikko.onrender.com";
export const api = axios.create({
  baseURL: API_URL,
  timeout: 20000,
  headers: { "Content-Type": "application/json" },
});
export const getHealth = () => api.get("/api/v1/health");
export const searchCars = (params) => api.get("/api/v1/cars/search", { params });
export const recommendCars = (params) => api.get("/api/v1/recommend", { params });
