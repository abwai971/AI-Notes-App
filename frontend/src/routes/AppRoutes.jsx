import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Register from "../pages/Register/Register";
import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";

import ProtectedRoute from "../components/ProtectedRoute/ProtectedRoute";

function AppRoutes() {
    return (
        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Navigate to="/login" />}
                />

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}

export default AppRoutes;