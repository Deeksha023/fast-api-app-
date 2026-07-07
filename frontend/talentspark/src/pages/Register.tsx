import {useState} from "react";
import {register} from "../Services/AuthService";

type Props = {
    onSwitchToLogin: () => void;
}

function Register({onSwitchToLogin}: Props){
    const [name,setName] = useState("");
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");
    const [role,setRole] = useState("admin");

    const handleSubmit = async (e:React.FormEvent) => {
        e.preventDefault();
        try {
            await register({name,email,password,role});
            alert("Registration successful! Please login.");
            onSwitchToLogin();
        } catch (error: any) {
            console.error("Error during registration:", error);
            const msg = error?.response?.data?.detail || error?.response?.data || error.message || "Registration failed";
            alert(`Registration failed: ${msg}`);
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
                    <h2>Create account</h2>
                    <p>Register to manage companies and jobs.</p>
                </div>
                <form onSubmit={handleSubmit} className="auth-form">
                    <label htmlFor="name">Name</label>
                    <div className="input-group">
                        <span className="input-icon">N</span>
                        <input id="name" type="text" value={name} onChange={(e)=>setName(e.target.value)} placeholder="Enter your name" required />
                    </div>

                    <label htmlFor="email">Email address</label>
                    <div className="input-group">
                        <span className="input-icon">@</span>
                        <input id="email" type="email" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Enter your email" required />
                    </div>

                    <label htmlFor="password">Password</label>
                    <div className="input-group">
                        <span className="input-icon">#</span>
                        <input id="password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Create a password" required />
                    </div>

                    <label htmlFor="role">Role</label>
                    <select id="role" value={role} onChange={(e)=>setRole(e.target.value)} required>
                        <option value="admin">Admin</option>
                        <option value="candidate">Candidate</option>
                    </select>

                    <button type="submit" className="btn auth-submit">Register</button>
                </form>
                <div className="auth-divider"><span>or</span></div>
                <div className="auth-footer">
                    <span>Already have an account?</span>
                    <button type="button" className="btn secondary" onClick={onSwitchToLogin}>Login</button>
                </div>
            </div>
        </div>
    )
}

export default Register;
