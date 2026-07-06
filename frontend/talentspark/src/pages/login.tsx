import {useState} from "react";
import {login} from "../Services/AuthService";

type Props = {
    onLogin: (token: string) => void;
    onSwitchToRegister: () => void;
}

function Login({onLogin, onSwitchToRegister}: Props){
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");

    const handleSubmit = async (e:React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await login({email,password});
            onLogin(response.access_token);
        } catch (error) {
            console.error("Error during login:", error);
            alert("Login failed");
        }
    }   
    return(
        <div className="auth-container auth-background">
            <div className="auth-card auth-card--login">
                <div className="auth-brand">
                    <div className="brand-text">
                        <span className="brand-name">Talent</span>
                        <span className="brand-accent">Spark</span>
                    </div>
                </div>
                <div className="auth-header">
                    <h2>Welcome back</h2>
                    <p>Sign in to continue to TalentSpark.</p>
                </div>
                <form onSubmit={handleSubmit} className="auth-form">
                    <label htmlFor="email">Email address</label>
                    <div className="input-group">
                        <span className="input-icon">✉</span>
                        <input id="email" type="email" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Enter your email" required />
                    </div>

                    <label htmlFor="password">Password</label>
                    <div className="input-group">
                        <span className="input-icon">🔒</span>
                        <input id="password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Enter your password" required />
                    </div>

                    <button type="submit" className="btn auth-submit">Login</button>
                </form>
                <div className="auth-divider"><span>or</span></div>
                <div className="auth-footer">
                    <span>Don't have an account?</span>
                    <button type="button" className="btn secondary" onClick={onSwitchToRegister}>Register</button>
                </div>
            </div>
        </div>
    )
}

export default Login;
