import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../components/Button/Button";
import { getCurrentUser } from "../../api/auth";
import useAuth from "../../hooks/useAuth";
import { removeTokens } from "../../utils/token";
import "./Dashboard.css";

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
        return <main className="dashboard-loading">Loading your workspace…</main>;
    }

    return (
        <main className="dashboard-page">
            <header className="dashboard-topbar">
                <Link className="dashboard-brand" to="/dashboard">AI Notes</Link>
                <div className="dashboard-topbar-actions">
                    <Link to="/notes">Notes</Link>
                    <button type="button" onClick={handleLogout}>Log out</button>
                </div>
            </header>

            <section className="dashboard-shell">
                <div className="dashboard-welcome">
                    <p className="dashboard-kicker">Your workspace</p>
                    <h1>Welcome back, {user.first_name}.</h1>
                    <p>Capture an idea, return to a draft, or keep your folders organized.</p>
                </div>

                <section className="dashboard-actions" aria-label="Workspace shortcuts">
                    <Link className="dashboard-action-card notes-action" to="/notes">
                        <span className="dashboard-action-icon">✦</span>
                        <span>
                            <strong>Open notes</strong>
                            <small>Write, organize, and revisit your ideas.</small>
                        </span>
                        <b>→</b>
                    </Link>
                    <Link className="dashboard-action-card folders-action" to="/folders">
                        <span className="dashboard-action-icon">▦</span>
                        <span>
                            <strong>Manage folders</strong>
                            <small>Create spaces for every project and topic.</small>
                        </span>
                        <b>→</b>
                    </Link>
                </section>

                <section className="account-card">
                    <div>
                        <p className="dashboard-kicker">Account</p>
                        <h2>{user.first_name} {user.last_name}</h2>
                    </div>
                    <div className="account-details">
                        <p><span>Username</span>{user.username}</p>
                        <p><span>Email</span>{user.email}</p>
                        <p><span>Role</span>{user.role}</p>
                    </div>
                    <Button onClick={handleLogout}>Log out</Button>
                </section>
            </section>
        </main>
    );
}

export default Dashboard;
