import axios from "axios";

const AxiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api/v1",
});

AxiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default AxiosClient;
