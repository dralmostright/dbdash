import { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { getRelativeTime } from "../../components/utils/dateTImeUtils";
import RdsApi from "../../api/RdsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import { NoData } from "../../components/utils/NoData";
//getRdsRecentActivity

dayjs.extend(relativeTime);

export function RecentActivity() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetRecentActivity() {
      try {
        setLoading(true);
        const response = await RdsApi.getRdsRecentActivity();
        setData(response.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load Engine Distribution Data");
      } finally {
        setLoading(false);
      }
    }

    fetRecentActivity();
  }, []);

  if (loading)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "350px" }}>
          <div className="card-body">
            <h5 className="card-title">RDS Activity </h5>
            <Loading />
          </div>
        </div>
      </div>
    );
  if (error)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "350px" }}>
          <div className="card-body">
            <h5 className="card-title">RDS Activity </h5>
            <ErrorCard message={error} />
          </div>
        </div>
      </div>
    );

  return (
    <div className="card">
      <div className="card-body" style={{ minHeight: "400px" }}>
        <h5 className="card-title">Recent Activity</h5>
        {!data || data.length === 0 ? (
          <NoData />
        ) : (
          <div className="activity">
            {data.map((item, index) => (
              <div className="activity-item d-flex" key={index}>
                <div className="activite-label" style={{ minWidth: "100px" }}>
                  {getRelativeTime(item.event_time)}
                </div>

                <i
                  className={`bi bi-circle-fill activity-badge align-self-start ${
                    item.event_type === "create"
                      ? "text-success"
                      : "text-danger"
                  }`}
                />
                <div className="activity-content">
                  <span className="fw-bold">{item.rds_identifier}</span>
                  <br />
                  <small className="text-muted">
                    BU : <strong>{item.account_alias}</strong>
                  </small>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
