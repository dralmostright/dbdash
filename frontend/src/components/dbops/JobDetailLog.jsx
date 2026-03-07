import { useEffect, useRef, useState } from "react";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import "./jobstatus.css";

export function JobDetailLog({ job_id }) {
  const [jobdata, setJobData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const sincetimeRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    // reset when job_id changes
    setJobData([]);
    setLoading(true);
    setError(null);
    sincetimeRef.current = null;

    async function fetchData() {
      try {
        const response = await DbOpsApi.getjoblogsbyid(
          job_id,
          sincetimeRef.current
        );

        const logs = response.data || [];

        if (logs.length > 0) {
          setJobData(prev => {
            const existing = new Set(prev.map(l => l.exec_datetime));
            const newLogs = logs.filter(
              l => !existing.has(l.exec_datetime)
            );
            return [...newLogs, ...prev];
          });

          const latestTime = logs.reduce((latest, log) => {
            return !latest || new Date(log.exec_datetime) > new Date(latest)
              ? log.exec_datetime
              : latest;
          }, sincetimeRef.current);

          sincetimeRef.current = latestTime;

          const finalStatus = logs.at(-1)?.job_status;
          if (finalStatus === "COMPLETED" || finalStatus === "FAILED") {
            clearInterval(intervalRef.current);
          }
        }

        setError(null);
      } catch (err) {
        console.error(err);
        setError("Failed to load job data.");
        clearInterval(intervalRef.current);
      } finally {
        setLoading(false);
      }
    }

    fetchData();

    intervalRef.current = setInterval(fetchData, 30000);

    return () => clearInterval(intervalRef.current);
  }, [job_id]);

  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 style={{ marginBottom: "0px" }}>
            <strong>Job Log</strong>
          </h5>
        </div>

        <div
          className="card-body"
          style={{ marginTop: "20px", paddingBottom: "0px", minHeight: "80px" }}
        >
          {error ? (
            <ErrorCard message={error} />
          ) : loading ? (
            <Loading />
          ) : (
            <table className="table table-striped table-sm table-bordered">
              <thead>
                <tr>
                  <th>Event Time</th>
                  <th>Status</th>
                  <th>Event Details</th>
                </tr>
              </thead>
              <tbody>
                {jobdata.map((log, index) => (
                  <tr key={`${log.exec_datetime}-${index}`}>
                    <td className="event-time-col">
                      {new Date(log.exec_datetime).toLocaleString()}
                    </td>
                    <td>{log.exec_status}</td>
                    <td>
                    {log.exec_detail?.includes("Directory:") ? (
                        <pre className="log-pre">
                        {log.exec_detail}
                        </pre>
                    ) : (
                        log.exec_detail
                    )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
