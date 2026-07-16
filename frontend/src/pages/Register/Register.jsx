import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Card from "../../components/Card/Card";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";

import { registerUser } from "../../api/auth";

import "./Register.css";

function Register() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        username: "",
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
            await registerUser(formData);

            alert("Registration Successful!");

            navigate("/login");
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
                    Create your account
                </p>

                <form onSubmit={handleSubmit}>

                    <Input
                        label="First Name"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                    />

                    <Input
                        label="Last Name"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                    />

                    <Input
                        label="Username"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                    />

                    <Input
                        label="Email"
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />

                    <Input
                        label="Password"
                        type="password"
                        name="password"
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
                        {loading ? "Creating..." : "Register"}
                    </Button>

                </form>

                <p className="footer-text">
                    Already have an account?{" "}
                    <Link to="/login">
                        Login
                    </Link>
                </p>

            </Card>
        </div>
    );
}

export default Register;