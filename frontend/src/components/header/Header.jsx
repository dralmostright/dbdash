import { NavLink } from "react-router"
import { Profile } from "./Profile"
import { AnimatedHeader } from "../utils/AnimateHeader";
export function Header() {
  const toggleSidebar = () => {
    document.body.classList.toggle("toggle-sidebar");
  };
  return (
    <header id="header" className="header fixed-top d-flex align-items-center">
    
    <div className="d-flex align-items-center justify-content-between">
      <NavLink to="/" className="logo d-flex align-items-center">
        <img src="/img/logo.png" alt="" />
        <span className="d-none d-lg-block">DbDash</span>
      </NavLink>
      <i className="bi bi-list toggle-sidebar-btn" onClick={toggleSidebar}></i>
    </div>

    <div className="search-bar">
    The backbone of uptime is unseen vigilance !
    </div>

    <nav className="header-nav ms-auto">
      <ul className="d-flex align-items-center">
        <Profile />
      </ul>
    </nav>

  </header>
  )
}
