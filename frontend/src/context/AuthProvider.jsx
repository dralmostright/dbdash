import { useState, useEffect } from 'react';
import AuthApi from '../api/AuthApi';
import { AuthContext } from './AuthContext';

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      const token = localStorage.getItem("access_token");
      if (token) {
          AuthApi.getProfile()
          .then((res) => { setUser(res.data); })
          .catch(async () => {
            try {
              const refreshRes = await AuthApi.refresh();
              localStorage.setItem(
                "access_token",
                refreshRes.data.access_token
              );
              const profileRes = await AuthApi.getProfile();
              setUser(profileRes.data);
            } catch {
              localStorage.clear();
              setUser(null);
            }
          })
          .finally(() => setLoading(false));
      } else {
        setLoading(false);
      }
    }, []);
  
    const login = async (credentials) => {
      const res = await AuthApi.login(credentials);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      console.log(res.data.access_token)
      console.log(res.data.refresh_token)
      setUser(res.data.user);
    };
  
    const register = async (data) => {
      await AuthApi.register(data);
    };
  
    const logout = () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setUser(null);
    };

    return (
      <AuthContext.Provider value={{ user, login, register, logout, loading }}>
        {children}
      </AuthContext.Provider>
    );
  };
