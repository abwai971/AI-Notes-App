import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../components/Button/Button";

import { getCurrentUser } from "../../api/auth";
import useAuth from "../../hooks/useAuth";
import { removeTokens } from "../../utils/token";

function Dashboard() {

    const { user, setUser } = useAuth();

    const navigate = useNavigate();

    useEffect(() => {

        async function fetchUser() {
            try {
                const response = await getCurrentUser();
                setUser(response.data);
            } catch {
                navigate("/login");
            }
        }

        fetchUser();

    }, [navigate, setUser]);

    function handleLogout() {

        removeTokens();

        setUser(null);

        navigate("/login");
    }

    if (!user) {
        return <h2 style={{ textAlign: "center", marginTop: "100px" }}>
            Loading...
        </h2>;
    }

    return (
        <div className="page">

            <div
                style={{
                    width: "500px",
                    background: "white",
                    padding: "30px",
                    borderRadius: "12px",
                }}
            >

                <h1>Welcome {user.first_name} 👋</h1>

                <br />

                <p><b>Username:</b> {user.username}</p>

                <p><b>Email:</b> {user.email}</p>

                <p><b>Role:</b> {user.role}</p>

                <br />

                <Link to="/folders">Manage folders</Link>

                <br />
                <br />

                <Button onClick={handleLogout}>
                    Logout
                </Button>

            </div>

        </div>
    );
}

export default Dashboard;
