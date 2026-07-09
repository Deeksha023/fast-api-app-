import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
});

export function getAxiosErrorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
        if (error.response) {
            const detail = error.response.data?.detail || error.response.data?.message || error.response.data;
            if (Array.isArray(detail)) {
                return detail.map((item) => item.msg || JSON.stringify(item)).join(", ");
            }
            if (typeof detail === "string") {
                return detail;
            }
            if (detail) {
                return JSON.stringify(detail);
            }
            return `Server error (${error.response.status})`;
        }

        if (error.request) {
            return `Network error: Could not reach the backend at ${API_BASE_URL}. Make sure FastAPI is running on port 8000.`;
        }

        return error.message;
    }

    return error instanceof Error ? error.message : "Something went wrong";
}

// Automatically attach the Bearer token to every request
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem("token");
            window.location.reload();
        }
        return Promise.reject(error);
    }
);

export default api;
export { API_BASE_URL };
