import { useEffect, useState, useContext } from "react";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import DbOpsApi from "../../api/DbOpsApi";
import TableRow from "../../components/table/TableRow";
import { Loading } from "../../components/utils/Loading";
import { PageTitle } from "../../components/header/PageTitle";

export function ListMSServer() {
  const [serverdata, setServerData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [deleteserver, SetDeleteServer] = useState(null);
  const [error, setError] = useState("");

  const pagetitle = {
        title: "Server Details",
        parent: "Server Details",
        current: "View Servers"
  }

  useEffect(() => {
    loadServerData();
  }, []);

  const loadServerData = () => {
    setLoading(true);

    DbOpsApi.getserversall()
      .then(async (res) => {
        setServerData(res.data);
      })
      .catch(() => {
        setMessage("Failed to load Servers info");
        setTimeout(() => setMessage(""), 1500);
        setLoading(false);
      })
      .finally(() => setLoading(false));
  };

  const handleDelete = (msdbs_id) => {
    DbOpsApi.deleteservermount(msdbs_id)
      .then(() => {
        setServerData((prev) => prev.filter((j) => j.msdbs_id !== msdbs_id));
        setMessage("Server details has been deleted Successfully.");
        setTimeout(() => setMessage(""), 1500);
      })
      .catch(() => {
        setError("Failed to delete Server details!");
        setTimeout(() => setError(""), 1500);
      })
      .finally(() => {
        setLoading(false);
        setShowModal(false);
        SetDeleteServer(null);
      });
  };

  if (loading) return <Loading />;
  return (
    <>
      <title> DbDash - List Servers</title>
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
                <p>Are you sure you want to delete this Server?</p>
                <table className="table table-hover table-sm table-bordered">
                  <tbody>
                <tr>
                    <th>Server Name</th><td>{deleteserver.msdbs_name} </td>
                </tr>
                <tr>
                    <th>Server IP/Host</th><td>{deleteserver.msdbs_host}</td>
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
                    handleDelete(deleteserver.msdbs_id);
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
                      <th scope="col">Server Name</th>
                      <th scope="col">Server Host/IP</th>
                      <th scope="col">Default Database</th>
                      <th scope="col">Default Port</th>
                      <th scope="col">Username</th>
                      <th scope="col">Status</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {serverdata.map((server, index) => (
                      <TableRow
                        key={server.msdbs_name}
                        sn={index + 1}
                        columns={[
                          server.msdbs_name,
                          server.msdbs_host,
                          server.msdbs_database,
                          server.msdbs_port,
                          server.msdbs_user,
                          server.msdbs_status,
                        ]}
                        actions={[
                          {
                            iconname: "bi-pencil-square",
                            path: `/msserver/meta/edit-ser/${server.msdbs_id}`,
                            color: "green",
                          },
                          {
                            iconname: "bi-trash3-fill",
                            color: "red",
                            onClick: () => {
                              SetDeleteServer(server);
                              setShowModal(true);
                            },
                          },
                          {
                            iconname: "bi-binoculars",
                            color: "blue",
                            path: `/msserver/meta/view-ser/${server.msdbs_id}`
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
