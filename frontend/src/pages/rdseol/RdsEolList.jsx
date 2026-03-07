import { useEffect, useState, useCallback } from "react";
import RdsApi from "../../api/RdsApi";
import EolTable from "../../components/rdsinst/EolTable";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import BannerMessage from "../../components/rdsinst/BannerMessage";

export function RdsEolList({ engine, version, columns }) {
  const [eoldata, SetEolData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadEol = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      if (version === "major") {
        const res = await RdsApi.getRdsEolMajorDetail(engine);
        SetEolData(res.data);
      } else {
        const res = await RdsApi.getRdsEolMinorDetail(engine);
        SetEolData(res.data);
      }
    } catch (err) {
      console.error(err);
      setError(`Failed to load EOL data for ${version} ${engine}`);
    } finally {
      setLoading(false);
    }
  }, [engine, version]);

  //console.log(eoldata)

  useEffect(() => {
    loadEol();
  }, [loadEol]);

  const handleRefresh = async () => {
    try {
      setLoading(true);
      await RdsApi.refreshRdsEolData(engine, version);
      await loadEol();
      setSuccessMessage("Successfully refreshed EOL data from AWS.");
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      console.error(err);
      setError("Failed to refresh EOL data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card-body" style={{ minHeight: "500px" }}>
            <BannerMessage />
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "10px",
        }}
      >

        <h5 className="card-title">
          EOL details : {version} {engine}
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
