import { NavLink, useLocation } from "react-router";

export default function SidebarSubmenu({ submenu }) {
  const location = useLocation(); // current path

  return (
    <ul className="nav-content">
      {submenu.map((sub, index) => {
        const isDisabled = 
        sub.routepath.includes("edit-")||
        sub.routepath.includes("list-rds")||
        sub.routepath.includes("view-ser")||
        sub.routepath.includes("view-job")||        
        sub.routepath.includes("view-rds");
        const isActive = location.pathname === sub.routepath;

        return (
          <li key={index}>
            {!sub.submenu ? (
              <NavLink
                to={sub.routepath}
                onClick={(e) => {
                  if (isDisabled) e.preventDefault(); 
                }}
                className={`nav-link ${isActive ? "active" : ""}`}
              >
                <i className="bi bi-circle"></i>
                <span>{sub.menuname}</span>
              </NavLink>
            ) : (
              <SidebarItem item={sub} />
            )}
          </li>
        );
      })}
    </ul>
  );
}
