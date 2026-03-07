export function StepReview({ serverdata, jiratdata }) {
  return (
    <>
      <div className="card">
        <div className="row gx-3" style={{ padding: "5px" }}>
          <h5 className="card-title">Review and Submit</h5>
          <div className="col-lg-6" style={{ minHeight: "425px" }}>
            <>
              <h5 className="card-title">Jira Ticket Details</h5>
              <table className="table table-hover table-bordered activity table-sm">
                <thead>
                  <tr>
                    <th scope="col">Jira Fileds</th>
                    <th scope="col">Jira Values</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th>Jira Summary</th>
                    <td>{jiratdata.jirat_summary}</td>
                  </tr>
                  <tr>
                    <th>Jira Ticket</th>
                    <td>{jiratdata.jirat_ticket}</td>
                  </tr>
                  <tr>
                    <th>Company Name</th>
                    <td>{jiratdata.jirat_company_name}</td>
                  </tr>
                  <tr>
                    <th>Address</th>
                    <td>{jiratdata.jirat_company_address}</td>
                  </tr>
                  <tr>
                    <th>Application Type (Source Database)</th>
                    <td>{jiratdata.jirat_src_app_type}</td>
                  </tr>
                  <tr>
                    <th>Database Name</th>
                    <td>{jiratdata.jirat_db_name}</td>
                  </tr>
                  <tr>
                    <th>Number of Sites</th>
                    <td>{jiratdata.jirat_num_sites}</td>
                  </tr>
                  <tr>
                    <th>Number of Desktop Licenses</th>
                    <td>{jiratdata.jirat_desktop_licenses}</td>
                  </tr>
                  <tr>
                    <th>Number of Mobile Licenses</th>
                    <td>{jiratdata.jirat_mobile_licenses}</td>
                  </tr>
                  <tr>
                    <th>Reporter</th>
                    <td>{jiratdata.jirat_reporter}</td>
                  </tr>
                  <tr>
                    <th>Assignee</th>
                    <td>{jiratdata.jirat_assignee}</td>
                  </tr>
                  <tr>
                    <th>Jira Created Date</th>
                    <td>{jiratdata.jirat_created}</td>
                  </tr>

                </tbody>
              </table>
            </>

          </div>
          <div className="col-lg-6">
            <h5 className="card-title">Database being provisioned on</h5>
            <ul className="nav nav-tabs" >
              <li className="nav-item" >
                <button
                  className="nav-link active"
                  type="button"
                >
                  {serverdata.server}
                </button>
              </li>
            </ul>

            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Directory Type</th>
                  <th scope="col">Directory Path</th>
                </tr>
              </thead>
              <tbody>
                {
                  Object.entries(serverdata.mounts).map(([key, value], index) => (
                    <tr key={key}>
                      <td>{index + 1}</td>
                      <td>{key}</td>
                      <td>{value}</td>
                    </tr>
                  ))
                }
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}