import axios from "axios";
import { getAccessToken } from "../utils/token";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
});

api.interceptors.request.use(
    (config) => {
        const token = getAccessToken();

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
