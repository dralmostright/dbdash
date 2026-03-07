import { useContext, useState } from "react";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { PageTitle } from "../../components/header/PageTitle";
import { AuthContext } from "../../context/AuthContext";

// Import new components
import ProfileChangePassword from "./ProfileChangePassword";
import ProfileEdit from "./ProfileEdit";
import ProfileOverview from "./ProfileOverview";
import './UserProfile.css'

export function UserProfile() {
  const { user } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState("overview");

  const pagetitle = {
    title: "Users",
    parent: "Users",
    current: "Profile",
  };

  return (
    <>
      <title>DbDash - Profile</title>
      <Header />
      <Sidebar />

      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section profile">
          <div className="row">
            {/* LEFT CARD */}
            <div className="col-xl-4">
              <div className="card">
                <div className="card-body profile-card pt-4 d-flex flex-column align-items-center">
                  <img src={user.display_pic} alt="Profile" className="rounded-circle" />
                  <h2>{user.first_name} {user.last_name}</h2>
                  <span className="userprofile"></span>
                </div>
              </div>
            </div>

            {/* RIGHT SIDE TABS */}
            <div className="col-xl-8">
              <div className="card">
                <div className="card-body pt-3">

                  {/* TAB BUTTONS */}
                  <ul className="nav nav-tabs nav-tabs-bordered">
                    <li className="nav-item">
                      <button
                        className={`nav-link ${activeTab === "overview" ? " active" : ""}`}
                        onClick={() => setActiveTab("overview")}
                      >
                        Overview
                      </button>
                    </li>

                    <li className="nav-item">
                      <button
                        className={`nav-link ${activeTab === "edit" ? " active" : ""}`}
                        onClick={() => setActiveTab("edit")}
                      >
                        Edit Profile
                      </button>
                    </li>

                    <li className="nav-item">
                      <button
                        className={`nav-link ${activeTab === "password" ? " active" : ""}`}
                        onClick={() => setActiveTab("password")}
                      >
                        Change Password
                      </button>
                    </li>
                  </ul>

                  {/* TAB CONTENT */}
                  <div className="tab-content pt-2">
                    {activeTab === "overview" && <ProfileOverview user={user} activetab={activeTab}/>}
                    {activeTab === "edit" && <ProfileEdit user={user} activetab={activeTab}/>}
                    {activeTab === "password" && <ProfileChangePassword user={user} activetab={activeTab}/>}
                  </div>

                </div>
              </div>
            </div>
          </div>
        </section>

      </main>
    </>
  );
}
