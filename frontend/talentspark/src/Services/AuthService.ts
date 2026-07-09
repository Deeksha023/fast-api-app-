import type { LoginRequest, LoginResponse, RegisterRequest, RegisterResponse } from "../types/User";
import api from "./api";

export const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
    // Backend login accepts OAuth-style form data with username=email.
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const response = await api.post<LoginResponse>("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return response.data;
};

export const register = async (user: RegisterRequest): Promise<RegisterResponse> => {
    const response = await api.post<RegisterResponse>("/auth/register", user);
    return response.data;
};
