import { useEffect, useState } from "react";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import DbOpsApi from "../../api/DbOpsApi";
import TableRow from "../../components/table/TableRow";
import { Loading } from "../../components/utils/Loading";
import { PageTitle } from "../../components/header/PageTitle";

export function ListJobs() {
  const [jobData, setJobData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const pagetitle = {
        title: "DB Provision Jobs",
        parent: "DB Provision Jobs",
        current: "List Jobs"
  }

  useEffect(() => {
    loadServerData();
  }, []);

  const loadServerData = () => {
    setLoading(true);

    DbOpsApi.getalljobs()
      .then(async (res) => {
        setJobData(res.data);
      })
      .catch(() => {
        setError("Failed to load Servers info");
        setTimeout(() => setError(""), 1500);
        setLoading(false);
      })
      .finally(() => setLoading(false));
  };

  /*
  function parseDbJson(value) {
  if (!value) return null;

  try {
    let parsed = value;

    while (typeof parsed === "string") {
      parsed = JSON.parse(parsed);
    }

    return parsed;
  } catch (e) {
    console.error("Failed to parse DB JSON", e, value);
    return null;
  }
}
*/
//console.log(jobData)

  if (loading) return <Loading />;
  return (
    <>
      <title> DbDash - List Provision Jobs</title>
      <Header />
      <Sidebar />
      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section">
          <div className="row">
            <div className="card">
              <div className="card-body" style={{ marginTop: "20px" }}>
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
                      <th scope="col">Jira Ticket</th>
                      <th scope="col">Job Initiated By</th>
                      <th scope="col">Job Mode</th>
                      <th scope="col">Job Status</th>
                      <th scope="col">Job Last Updated</th>
                      <th scope="col">Job Current Step</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {jobData.map((job, index) => (
                      <TableRow
                        key={job.job_id}
                        sn={index + 1}
                            columns={[
                              job.jirat_ticket,
                              job.jira_user,
                              job.job_mode,
                              job.job_status,
                              job.job_updated_at,
                              job.job_current_step,
                            ]}
                            actions={[
                              {
                                iconname: "bi-binoculars",
                                color: "blue",
                                path: `/provision/database/view-job/${job.job_id}`,
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
