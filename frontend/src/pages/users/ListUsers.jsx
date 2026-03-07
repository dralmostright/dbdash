import { useEffect, useState } from "react";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import { NavLink } from "react-router";
import UsersApi from "../../api/UsersApi";
import TableRow from "../../components/table/TableRow";
import { Loading } from "../../components/utils/Loading";
import { PageTitle } from "../../components/header/PageTitle";

export function ListUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [deleteUser, SetDeleteUser] = useState(null);
  const [error, setError] = useState("");

  const pagetitle = {
    title: "Users",
    parent: "Users",
    current: "All Users",
  };

  // Fetch users
  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = () => {
    setLoading(true);

    UsersApi.listall()
      .then(async (res) => {
        setUsers(res.data);
      })
      .catch(() => {
        setMessage("Failed to load users");
        setLoading(false);
      })
      .finally(() => setLoading(false));
  };

  const handleDelete = (uid) => {
    UsersApi.remove(uid)
      .then(() => {
        setUsers((prev) => prev.filter((u) => u.uid !== uid));
        setMessage("User has been deleted Successfully.");
      })
      .catch(() => {
        setError("Failed to delete User!");
      })
      .finally(() => {
        setLoading(false);
        setShowModal(false);
        SetDeleteUser(null);
      });
  };
  //const handleView = (user) => alert("View: " + user.username);
  //{ iconname: "bi-eye-fill", path: "/", onClick: () => handleView(user) },
  //const handleEdit = (user) => alert("Edit: " + user.username);
  if (loading) return <Loading />;
  return (
    <>
      <title> DbDash - List Users</title>
      <Header />
      <Sidebar />

      {showModal && (
        <div className="modal fade show" style={{ display: "block" }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content" style={{ zIndex: 5000 }}>
              <div className="modal-header">
                <h5 className="modal-title">Confirm Delete</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowModal(false)}
                ></button>
              </div>

              <div className="modal-body">
                <p>Are you sure you want to delete this User?</p>
                <table className="table table-hover table-sm table-bordered">
                <tr>
                    <th>Full Name</th><td>{deleteUser.first_name} {deleteUser.last_name}</td>
                </tr>
                <tr>
                    <th>Email</th><td>{deleteUser.email}</td>
                </tr>
                </table>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>

                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={() => {
                    handleDelete(deleteUser.uid);
                    setShowModal(false);
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show"></div>
        </div>
      )}

      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section">
          <div className="row">
            <div className="card">
              <div className="card-body" style={{ marginTop: "20px" }}>
                {message && (
                  <div
                    className="alert alert-success alert-dismissible show"
                    role="alert"
                  >
                    <i className="bi bi-check-circle me-1"></i>
                    {message}
                    <button
                      type="button"
                      className="btn-close"
                      data-bs-dismiss="alert"
                      aria-label="Close"
                    ></button>
                  </div>
                )}
                {error && (
                  <div
                    className="alert alert-danger alert-dismissible show"
                    role="alert"
                  >
                    <i className="bi bi-exclamation-octagon me-1"></i>
                    {error}
                    <button
                      type="button"
                      className="btn-close"
                      data-bs-dismiss="alert"
                      aria-label="Close"
                    ></button>
                  </div>
                )}

                <table className="table table-hover table-sm table-bordered">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Full Name</th>
                      <th scope="col">Email</th>
                      <th scope="col">Role</th>
                      <th scope="col">Status</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user, index) => (
                      <TableRow
                        key={user.uid}
                        sn={index + 1}
                        columns={[
                          user.first_name+" "+user.last_name,
                          user.email,
                          user.role,
                        ]}
                        actions={[
                          {
                            iconname: "bi-pencil-square",
                            path: `/account/edit-user/${user.uid}`,
                            color: "green",
                          },
                          {
                            iconname: "bi-trash3-fill",
                            color: "red",
                            onClick: () => {
                                SetDeleteUser(user);
                              setShowModal(true);
                            },
                          },
                        ]}
                        status={[user.is_verified]}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
