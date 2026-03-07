import {
  useState,
  useEffect,
  useCallback
} from "react";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../utils/Loading";
import ErrorCard from "../utils/ErrorCard";

export function StepRetriveJira({ jiratdata, setJiraTData, jiramdata }) {

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadJiraTicketDetails = useCallback(() => {
    setLoading(true);
    DbOpsApi.getjiraticketdetail(jiramdata.jira_id, jiramdata.jira_ticket)
      .then((res) => setJiraTData(res.data))
      .catch((err) => {
        setMessage(`Failed to fetch Jira Ticket Details for Ticket : "${jiramdata.jira_ticket}". Verify if the Jira Ticket is valid or check with App Administrator.`);
        setError(true);
      })
      .finally(() => setLoading(false));
  }, [jiramdata.jira_id, jiramdata.jira_ticket, setJiraTData]);

  useEffect(() => {
    if (jiramdata?.jira_id && jiramdata?.jira_ticket) {
      loadJiraTicketDetails();
    }
  }, [jiramdata?.jira_id, jiramdata?.jira_ticket, loadJiraTicketDetails]);
  /*
  useEffect(() => {
    if (jiramdata && jiramdata.jira_id && jiramdata.jira_ticket) {
      loadJiraTicketDetails();
    }
  }, [jiramdata?.jira_id, jiramdata?.jira_ticket]);

  const loadJiraTicketDetails = () => {
    setLoading(true);
    DbOpsApi.getjiraticketdetail(jiramdata.jira_id, jiramdata.jira_ticket)
      .then(async (res) => {
        setJiraTData(res.data);
      })
      .catch(() => {
        setMessage("Failed to Jira Ticket Details");
        setTimeout(() => setMessage(""), 1500);
        setError(true)
        setLoading(false);
      })
      .finally(() => setLoading(false));
  };  
*/
  //console.log(jiramdata)
  //console.log(jiratdata)

  return (
    <div className="card col-lg-12" style={{ minHeight: "500px" }}>
      <div className="col-lg-6">
        <div className="row g-0" style={{ marginTop: "10px" }}>
          <h5>Jira Details</h5>
          {error ? (
            <ErrorCard message={message} />
          ) : loading ? (
            <Loading />
          ) : (
            <>
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
          )}
        </div>
      </div>
      <div className="col-lg-6">
      </div>
    </div>
  );
};
