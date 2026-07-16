import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";

import { loginUser } from "../../api/auth";
import { saveTokens } from "../../utils/token";

import "./Login.css";

function Login() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    function handleChange(e) {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();

        setLoading(true);
        setError("");

        try {
            const response = await loginUser(formData);

            saveTokens(
                response.data.access_token,
                response.data.refresh_token
            )

            navigate("/dashboard");

        } catch (err) {
            if (err.response) {
                setError(err.response.data.detail);
            } else {
                setError("Something went wrong.");
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="page">
            <Card>

                <h1 className="title">
                    AI Notes
                </h1>

                <p className="subtitle">
                    Welcome Back
                </p>

                <form onSubmit={handleSubmit}>

                    <Input
                        label="Email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                    />

                    <Input
                        label="Password"
                        name="password"
                        type="password"
                        value={formData.password}
                        onChange={handleChange}
                    />

                    {error && (
                        <p className="error">
                            {error}
                        </p>
                    )}

                    <Button
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? "Signing In..." : "Login"}
                    </Button>

                </form>

                <p className="footer-text">
                    Don't have an account?{" "}
                    <Link to="/register">
                        Register
                    </Link>
                </p>

            </Card>
        </div>
    );
}

export default Login;