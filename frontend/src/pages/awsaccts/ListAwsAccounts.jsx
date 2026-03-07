import { useState, useEffect } from "react";
import { NavLink } from "react-router";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import TableRow from "../../components/table/TableRow";
import { Loading } from "../../components/utils/Loading";
import { PageTitle } from "../../components/header/PageTitle";
import AwsAcctApi from "../../api/AwsAcctApi";
import { CommaParser } from "../../components/utils/CommaParser";

export function ListAwsAccounts() {
  const [awsaccounts, setAwsAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [deleteId, setDeleteId] = useState(null);
  const [error, setError] = useState("");

  const pagetitle = {
    title: "Aws Accounts",
    parent: "Aws Accounts",
    current: "All Accounts",
  };
  // Fetch users
  useEffect(() => {
    loadAwsOrgs();
  }, []);

  const loadAwsOrgs = () => {
    setLoading(true);

    AwsAcctApi.listall()
      .then(async (res) => {
        setAwsAccounts(res.data);
      })
      .catch(() => {
        setError("Failed to load Accounts");
        setLoading(false);
      })
      .finally(() => setLoading(false));
  };

  // Delete user
  const handleDelete = (aid) => {
    AwsAcctApi.deleteac(aid)
      .then(() => {
        setAwsAccounts((prev) => prev.filter((u) => u.aid !== aid)); // update UI
        setMessage("Account Has been deleted Successfully.");
      })
      .catch(() => {
        setError("Failed to delete Account!")
      })
      .finally(() => {
        setLoading(false);
        setShowModal(false);
        setDeleteId(null);
      });
  };
  //{ iconname: "bi-eye-fill", path: "/", onClick: () => handleView(awsaccount) },
  //const handleView = (user) => alert("View: " + user.username);
  //const handleEdit = (user) => alert("Edit: " + user.username);
  if (loading) return <Loading />;
  return (
    <>
      <title> DbDash - Running Instances</title>
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
                <p>Are you sure you want to delete this AWS Account?</p>
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
                    handleDelete(deleteId);
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
            
              {message && <div className="alert alert-success alert-dismissible show" role="alert">
                <i className="bi bi-check-circle me-1"></i>
                {message}
                <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div> }
              {error &&
              <div className="alert alert-danger alert-dismissible show" role="alert">
                <i className="bi bi-exclamation-octagon me-1"></i>
                {error}
                <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
                }
                <table className="table table-hover activity table-sm">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Account Alias</th>
                      <th scope="col">Account Number</th>
                      <th scope="col">Account Org</th>
                      <th scope="col">Account Az</th>
                      <th scope="col">Account Status</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {awsaccounts.map((awsaccount, index) => (
                      <TableRow
                        key={awsaccount.aid}
                        sn={index + 1}
                        columns={[
                          awsaccount.account_alias,
                          awsaccount.account_number,
                          awsaccount.account_org,
                        ]}
                        actions={[
                          {
                            iconname: "bi-pencil-square",
                            path: `/aws/edit-account/${awsaccount.aid}`,
                            color: "green",
                          },
                          {
                            iconname: "bi-trash3-fill",
                            path: "/aws/accounts",
                            color: "red",
                            onClick: () => {
                              setDeleteId(awsaccount.aid);
                              setShowModal(true);
                            },
                          },
                        ]}
                        extras={CommaParser(awsaccount.account_az)}
                        status={[awsaccount.account_status]}
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
