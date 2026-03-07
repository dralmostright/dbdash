export default function ProfileOverview({ user, activetab }) {
    return (
      <div className={`profile-overview tab-pane fade ${activetab === "overview" ? " show active" : ""}`} >
        <h5 className="card-title">Profile Details</h5>
  
        <div className="row">
          <div className="col-lg-3 col-md-4 label ">Full Name</div>
          <div className="col-lg-9 col-md-8">{user.first_name} {user.last_name}</div>
        </div>
  
        <div className="row">
          <div className="col-lg-3 col-md-4 label">Username</div>
          <div className="col-lg-9 col-md-8">{user.username}</div>
        </div>
  
        <div className="row">
          <div className="col-lg-3 col-md-4 label">Email</div>
          <div className="col-lg-9 col-md-8">{user.email}</div>
        </div>
      </div>
    );
  }
  