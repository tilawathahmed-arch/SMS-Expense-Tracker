import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getTransactions = () => api.get("/dashboard/transactions");
export const getCategorySummary = () => api.get("/dashboard/summary/category");
export const getMonthlySummary = () => api.get("/dashboard/summary/monthly");
export const getTotals = () => api.get("/dashboard/summary/totals");