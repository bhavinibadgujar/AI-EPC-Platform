import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Authentication
export const login = async (credentials) => {
  const response = await api.post("/login", credentials);
  return response.data;
};

// Dashboard
export const getDashboard = async () => {
  const response = await api.get("/dashboard");
  return response.data;
};

// Compliance
export const uploadCompliance = async (formData) => {
  const response = await api.post("/compliance/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

// Risk
export const getRisks = async () => {
  const response = await api.get("/risk");
  return response.data;
};

// Supply Chain
export const getSupply = async () => {
  const response = await api.get("/supply");
  return response.data;
};

// Commissioning
export const getCommissioning = async () => {
  const response = await api.get("/commissioning");
  return response.data;
};

// AI Chat
export const chat = async (message) => {
  const response = await api.post("/chat", {
    message,
  });

  return response.data;
};

export default api;
