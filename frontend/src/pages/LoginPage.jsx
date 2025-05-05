import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { login, signup } from "../utils/api";

export default function LoginPage({ onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login: setAuthToken } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (isLogin) {
        const data = await login({ email, password });
        setAuthToken( data.access_token);
        navigate("/");
      } else {
        await signup({ email, password, full_name: fullName });
        setIsLogin(true);
        setError("Signup successful! Please log in.");
      }
    } catch (err) {
      setError(err.detail || "Authentication failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold mb-6 text-center">
          {isLogin ? "Login" : "Sign Up"}
        </h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          {!isLogin && (
            <input
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-400"
              value={fullName}
              onChange={e => setFullName(e.target.value)}
              placeholder="Full Name"
              required
            />
          )}
          <input
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-400"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="Email"
            type="email"
            required
          />
          <input
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-400"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Password"
            type="password"
            required
          />
          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>
        <div className="mt-4 text-center">
          <button
            className="text-blue-600 hover:underline"
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin
              ? "Don't have an account? Sign Up"
              : "Already have an account? Login"}
          </button>
        </div>
        {error && (
          <div className="mt-4 text-center text-red-600">{error}</div>
        )}
      </div>
    </div>
  );
}