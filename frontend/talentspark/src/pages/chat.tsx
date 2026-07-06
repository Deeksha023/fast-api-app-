import { useState } from "react";
import { askCareerChat } from "../Services/ChatServices";
import type { ChatMessage } from "../types/chat";

function Chat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [sessionId] = useState(() => "session_" + Date.now());

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage: ChatMessage = { role: "user", content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const response = await askCareerChat(input, sessionId);
            const botMessage: ChatMessage = { role: "bot", content: response };
            setMessages(prev => [...prev, botMessage]);
        } catch (error: any) {
            console.error("Chat error:", error);
            const msg = error?.response?.data?.detail || error?.response?.data || error?.message || "Could not get response";
            const errorMessage: ChatMessage = { role: "bot", content: `Error: ${msg}` };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="chat-panel">
            <div className="chat-header-panel">
                <h2>Career Chat</h2>
                <p>Get guidance on jobs, interviews, and career growth in real time.</p>
            </div>
            <div className="chat-window">
                {messages.length === 0 && <p className="chat-empty">Ask me anything about your career!</p>}
                {messages.map((msg, i) => {
                    const prev = messages[i - 1];
                    const isUserHello = prev && prev.role === "user" && prev.content.trim().toLowerCase() === "hello";
                    const label = msg.role === "user" ? "You" : (isUserHello ? "" : "TalentSpark");
                    return (
                        <div key={i} className={msg.role === "user" ? "message-bubble user-message" : "message-bubble bot-message"}>
                            {label && <span className="message-role">{label}</span>}
                            <p>{msg.content}</p>
                        </div>
                    )
                })}
                {loading && <p className="chat-loading">Thinking...</p>}
            </div>
            <form onSubmit={handleSend} className="chat-input-row">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    disabled={loading}
                />
                <button type="submit" className="btn" disabled={loading}>Send</button>
            </form>
        </section>
    );
}

export default Chat;