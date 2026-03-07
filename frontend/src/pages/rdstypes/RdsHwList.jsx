import { useEffect, useState, useCallback } from "react";
import RdsApi from "../../api/RdsApi";
import EolTable from "../../components/rdsinst/EolTable";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function RdsHwList({ viewMode, columns }) {
  const [eoldata, SetEolData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadEol = useCallback(async () => {
    try {
      setLoading(true);
      setError("");
        const res = await RdsApi.getRdsHwTypes(viewMode);
        SetEolData(res.data);
    } catch (err) {
      console.error(err);
      setError(`Failed to load instance type data for ${viewMode}`);
    } finally {
      setLoading(false);
    }
  }, [viewMode]);


  useEffect(() => {
    loadEol();
  }, [loadEol]);

  const handleRefresh = async () => {
    try {
      setLoading(true);
      await RdsApi.refreshRdsHwTypes(viewMode);
      await loadEol();
      setSuccessMessage("Successfully refreshed data from AWS.");
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      console.error(err);
      setError("Oops! Failed to refresh data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card-body" style={{ minHeight: "500px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "10px",
        }}
      >
        <h5 className="card-title">
        Amazon RDS instance types { viewMode === 'ebs' ? "EBS volumes" : ""}
        </h5>

        <button
          type="button"
          className="btn btn-dark"
          title="Get latest data from AWS"
          style={{ padding: "8px" }}
          onClick={handleRefresh}
        >
          {" "}
          <i className="bi bi-arrow-clockwise"></i>
        </button>
      </div>
      {successMessage && (
        <div className="alert alert-success" role="alert">
          {successMessage}
        </div>
      )}

      {error ? (
        <ErrorCard message={error} />
      ) : loading ? (
        <Loading />
      ) : (
        <EolTable data={eoldata} columns={columns} />
      )}
    </div>
  );
}
