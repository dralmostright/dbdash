import { useState, useRef, useEffect,useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import { NavLink, useNavigate } from "react-router-dom";

import './Profile.css'

export function Profile() {

    const [profileTab, setProfileTab] = useState(false);
    const dropdownRef = useRef(null);
    const { user } = useContext(AuthContext);
    const { logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const toggleProfile = () => {
        setProfileTab(prev => !prev);
    }

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setProfileTab(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    const handleLogout = () => {
        logout();                
        navigate("/auth/login"); 
      };

    if (!user) return null;

    return (
        <li className="nav-item dropdown pe-3" ref={dropdownRef}>
            <div 
                onClick={toggleProfile} 
                className={`nav-link nav-profile d-flex align-items-center pe-0 ${profileTab ? 'show' : ''}`} 
                style={{ cursor: "pointer" }}
            >
                <img src={user.display_pic} alt="Profile" className="rounded-circle" />
                <span className="d-none d-md-block dropdown-toggle ps-2">{user.first_name} {user.last_name}</span>
            </div>

            <ul className={`dropdown-menu dropdown-menu-end dropdown-menu-arrow profileheader ${profileTab ? 'showprofile show' : ''} profile`}>
                <li className="dropdown-header">
                    <h6>{user.first_name} {user.last_name}</h6>
                    <span></span>
                </li>
                <li><hr className="dropdown-divider" /></li>

                <li>
                    <NavLink className="dropdown-item d-flex align-items-center " to="/account/profile">
                        <i className="bi bi-person"></i>
                        <span>My Profile</span>
                    </NavLink>
                </li>

                <li><hr className="dropdown-divider" /></li>

                <li>
                    <button onClick={handleLogout} className="dropdown-item d-flex align-items-center">
                        <i className="bi bi-box-arrow-right"></i>
                        <span>Sign Out</span>
                    </button>
                </li>
            </ul>
        </li>
    )
}
