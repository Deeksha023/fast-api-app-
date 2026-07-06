interface ChatMessage {
    role: "user" | "bot";
    content: string;
}

interface ChatRequest {
    message: string;
    session_id: string;
}

interface ChatResponse {
    response: string;
}

interface LoginRequest {
    email: string;
    password: string;
}

interface LoginResponse {
    access_token: string;
    token_type?: string;
}

interface RegisterRequest {
    name: string;
    email: string;
    password: string;
    role: string;
}

interface RegisterResponse {
    id?: number;
    name: string;
    email: string;
    role: string;
}

export type {
    ChatMessage,
    ChatRequest,
    ChatResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse
}
