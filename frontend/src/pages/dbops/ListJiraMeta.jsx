import { useEffect, useState, useContext } from "react";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import DbOpsApi from "../../api/DbOpsApi";
import TableRow from "../../components/table/TableRow";
import { Loading } from "../../components/utils/Loading";
import { PageTitle } from "../../components/header/PageTitle";
import { AuthContext } from "../../context/AuthContext";

export function ListJiraMeta() {
  const [jirameta, setJiraMeta] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [deletejmeta, SetDeleteJmeta] = useState(null);
  const [error, setError] = useState("");
  const { user } = useContext(AuthContext);

  const pagetitle = {
    title: "Jira Meta",
    parent: "Jira Meta",
    current: "List Jira Meta info",
  };

  // Fetch users
  useEffect(() => {
    loadJiraMeta();
  }, []);

  const loadJiraMeta = () => {
    setLoading(true);

    DbOpsApi.listmetadata(user.uid)
      .then(async (res) => {
        setJiraMeta(res.data);
      })
      .catch(() => {
        setMessage("Failed to load Jira Meta info");
        setTimeout(() => setMessage(""), 1500);
        setLoading(false);
      })
      .finally(() => setLoading(false));
  };

  const handleDelete = (jira_id) => {
    DbOpsApi.deletemetadata(jira_id)
      .then(() => {
        setJiraMeta((prev) => prev.filter((j) => j.jira_id !== jira_id));
        setMessage("Jira Metadata has been deleted Successfully.");
        setTimeout(() => setMessage(""), 1500);
      })
      .catch(() => {
        setError("Failed to delete Jira Metadata!");
        setTimeout(() => setError(""), 1500);
      })
      .finally(() => {
        setLoading(false);
        setShowModal(false);
        SetDeleteJmeta(null);
      });
  };
  //const handleView = (user) => alert("View: " + user.username);
  //{ iconname: "bi-eye-fill", path: "/", onClick: () => handleView(user) },
  //const handleEdit = (user) => alert("Edit: " + user.username);
  if (loading) return <Loading />;
  return (
    <>
      <title> DbDash - List Jira Meta</title>
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
                  <tbody>
                <tr>
                    <th>Jira Meta Name</th><td>{deletejmeta.jira_meta_name} </td>
                </tr>
                <tr>
                    <th>Jira Meta User</th><td>{deletejmeta.jira_user}</td>
                </tr>
                </tbody>
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
                    handleDelete(deletejmeta.jira_id);
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
                  </div>
                )}
                {error && (
                  <div
                    className="alert alert-danger alert-dismissible show"
                    role="alert"
                  >
                    <i className="bi bi-exclamation-octagon me-1"></i>
                    {error}
                  </div>
                )}

                <table className="table table-hover table-sm table-bordered">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Jira Meta Name</th>
                      <th scope="col">Jira Cloud API Endpoint</th>
                      <th scope="col">Jira User Email</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {jirameta.map((jmeta, index) => (
                      <TableRow
                        key={jmeta.jira_id}
                        sn={index + 1}
                        columns={[
                          jmeta.jira_meta_name,
                          jmeta.jira_api_url,
                          jmeta.jira_user,
                        ]}
                        actions={[
                          {
                            iconname: "bi-pencil-square",
                            path: `/jira/meta/edit-m/${jmeta.jira_id}`,
                            color: "green",
                          },
                          {
                            iconname: "bi-trash3-fill",
                            color: "red",
                            onClick: () => {
                                SetDeleteJmeta(jmeta);
                              setShowModal(true);
                            },
                          },
                        ]}
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
