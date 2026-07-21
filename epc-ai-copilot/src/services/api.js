import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const login = async (credentials) => {
  const response = await api.post("/login", credentials);
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get("/api/health");
  return response.data;
};

export const getDashboard = async () => {
  const response = await api.get("/dashboard");
  return response.data;
};

export const uploadCompliance = async (formData) => {
  const payload = formData instanceof FormData ? formData : new FormData();
  if (!(formData instanceof FormData)) {
    payload.append("specification", formData.specificationFile);
    payload.append("vendor", formData.vendorFile);
  }

  const response = await api.post("/compliance/upload", payload, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getCompliance = async () => {
  const response = await api.get("/compliance");
  return response.data;
};

export const getRisks = async () => {
  const response = await api.get("/risk");
  return response.data;
};

export const getSupply = async () => {
  const response = await api.get("/supply");
  return response.data;
};

export const getCommissioning = async () => {
  const response = await api.get("/commissioning");
  return response.data;
};

export const chat = async (message) => {
  const payload = typeof message === "string" ? { message } : message;
  const response = await api.post("/chat", payload);
  return response.data;
};

export const getExecutiveBrief = async () => {
  const response = await api.get("/executive-brief");
  return response.data;
};

export const uploadScheduleRisk = async (file) => {
  const payload = new FormData();
  payload.append("file", file);
  const response = await api.post("/schedule-risk", payload, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

export default api;

