import { NavLink, useLocation } from "react-router";
import SidebarSubmenu from "./SidebarSubmenu";

export function SidebarItem({ item, openMenu, toggleMenu }) {
  const location = useLocation();

  // Check if this item or any child submenu is active
  const isActivePath = (path) => location.pathname.startsWith(path);

  const isParentActive =
    item.submenu?.some((s) => isActivePath(s.routepath)) || false;

  const isOpen = openMenu === item.menuname || isParentActive;

  return (
    <li className="nav-item">
      {/* Parent: If has submenu → button, else → NavLink */}
      {!item.submenu ? (
        <NavLink
          to={item.routepath}
          className={({ isActive }) =>
            `nav-link ${isActive ? "active" : "collapsed"}`
          }
        >
          <i className={item.icon}></i>
          <span>{item.menuname}</span>
        </NavLink>
      ) : (
        <>
          <button
            className={`nav-link ${isOpen ? "active" : "collapsed"}`}
            onClick={() => toggleMenu(item.menuname)}
          >
            <i className={item.icon}></i>
            <span>{item.menuname}</span>
            <i className="bi bi-chevron-down ms-auto"></i>
          </button>

          {isOpen && <SidebarSubmenu submenu={item.submenu} />}
        </>
      )}
    </li>
  );
}
