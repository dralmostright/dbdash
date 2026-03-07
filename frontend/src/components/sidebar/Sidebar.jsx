import { useState } from "react";
import { SidebarItem } from "./SidebarItem";
import { menuList } from "./menuData";
import "./sidebar.css";


export function Sidebar() {
  const [openMenu, setOpenMenu] = useState(null);

  const toggleMenu = (name) => {
    setOpenMenu((prev) => (prev === name ? null : name));
  };

  return (
    <aside id="sidebar" className="sidebar">
      <ul className="sidebar-nav">
        {menuList.map((item, index) => (
          <SidebarItem
            key={index}
            item={item}
            openMenu={openMenu}
            toggleMenu={toggleMenu}
          />
        ))}
      </ul>
    </aside>
  );
}