// src/components/ProtectedRoute.jsx
import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { Loading } from "../components/utils/Loading"

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);
  if (loading) return (
      <Loading />
  );
  if (!user) return <Navigate to="/auth/login" replace />;
  return children;
};

export default ProtectedRoute;