import { useEffect, useState } from "react";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import './jobstatus.css'

export function JobStatus({ job_id }) {
  const [jobdata, setJobData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let intervalId;

    async function fetchData() {
        try {
        const response = await DbOpsApi.getjobbyid(job_id);
        setJobData(response.data);
        setError(null);

        // Stop polling when job is done
        if (
            response.data.job_status === "COMPLETED" ||
            response.data.job_status === "FAILED"
        ) {
            clearInterval(intervalId);
        }
        } catch (err) {
        console.error(err);
        setError("Failed to load job data.");
        clearInterval(intervalId); // stop polling on error
        } finally {
        setLoading(false);
        }
    }

    // Initial fetch
    fetchData();

    // Poll every 3 seconds
    intervalId = setInterval(fetchData, 30000);

    // Cleanup on unmount
    return () => clearInterval(intervalId);
    }, [job_id]);


  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 className="" style={{ marginBottom: "0px" }}>
            <strong>Job Progress</strong>
          </h5>
        </div>
        <div
          className="card-body"
          style={{ marginTop: "20px", paddingBottom: "0px", minHeight: "80px" }}
        >
          <div className="row">
            {error ? (
              <ErrorCard message={error} />
            ) : loading ? (
              <Loading />
            ) : (
              <>
                {" "}
                <div className="col-md-3">
                  <label className="form-label">Jira Ticket</label>
                  <p>
                    <strong>{jobdata?.jirat_ticket}</strong>
                  </p>
                </div>
                <div className="col-md-3">
                  <label className="form-label">Job Last Updated</label>
                  <p>
                    <strong>{jobdata?.job_updated_at}</strong>
                  </p>
                </div>
                <div className="col-md-3">
                  <label className="form-label">Job Initiated By</label>
                  <p>
                    <strong>{jobdata?.jira_user}</strong>
                  </p>
                </div>
                <div className="col-md-3">
                <label className="form-label">Job Status</label>

                {jobdata?.job_status === "COMPLETED" && (
                    <div className="d-flex align-items-center gap-2">
                    <div className="status-circle success">
                        <i className="bi bi-check-lg"></i>
                    </div>
                    <span className="status-text success-text">{jobdata?.job_status}</span>
                    </div>
                )}

                {jobdata?.job_status === "FAILED" && (
                    <div className="d-flex align-items-center gap-2">
                    <div className="status-circle failed">
                        <i className="bi bi-x-lg"></i>
                    </div>
                    <span className="status-text failed-text">{jobdata?.job_status}</span>
                    </div>
                )}

                {jobdata?.job_status !== "COMPLETED" &&
                    jobdata?.job_status !== "FAILED" && (
                    <div className="d-flex align-items-center gap-2">
                        <div className="spinner-border text-primary custom-spinner" role="status"></div>
                        <strong className="status-text">{jobdata?.job_status}..</strong>
                    </div>
                    )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

