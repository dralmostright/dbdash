import {
  useState,
  useEffect,
  forwardRef,
  useImperativeHandle,
} from "react";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../utils/Loading";
import ErrorCard from "../utils/ErrorCard";

export const StepMounts = forwardRef(
  ({ mounts, setMounts }, ref) => {
    const [servers, setServers] = useState([]);
    const [inputValid, setInputValid] = useState("");
    const [serverId, setServerId] = useState("");
    const [availableMounts, setAvailableMounts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useImperativeHandle(ref, () => ({
      validate() {
        if (!serverId) {
          setInputValid("Please select the Server");
          setTimeout(() => setInputValid(""), 1500);
          return false;
        }
        if (!mounts?.mounts?.datadir || !mounts?.mounts?.log_dir) {
          setInputValid("Please select both mounts");
          setTimeout(() => setInputValid(""), 2000);
          return false;
        }
        return true;
      },
    }));

    useEffect(() => {
      async function fetchData() {
        try {
          setLoading(true);
          const response = await DbOpsApi.getserversall();
          setServers(response.data);
          setError(false);
        } catch (err) {
          console.error(err);
          setError("Failed to load servers.");
        } finally {
          setLoading(false);
        }
      }

      fetchData();
    }, []);

    useEffect(() => {
      if (!serverId) return;

      setLoading(true);
      setAvailableMounts([]);
      setMounts({});

      DbOpsApi.getserversamountll(serverId)
        .then((res) => setAvailableMounts(res.data?.mounts || []))
        .catch((err) =>
          setError(err?.message || "Failed to load mounts")
        )
        .finally(() => setLoading(false));
    }, [serverId, setMounts]);

    return (
      <div className="card col-lg-12" style={{ minHeight: "500px" }}>
        <div className="col-lg-6">
          <div className="row g-0" style={{ marginTop: "10px" }}>
            <h5>Server & Mount Selection</h5>

            {error && <ErrorCard message={error} />}
            {inputValid &&
              <>
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                  <i class="bi bi-exclamation-octagon me-1"></i>
                  {inputValid}
                </div>
              </>}
            {loading && <Loading />}

            {!loading && (
              <>
                <div className="mb-3">
                  <label>Server</label>
                  <select
                    className="form-select"
                    value={serverId}
                    onChange={(e) => setServerId(e.target.value)}
                  >
                    <option value="">-- Select Server --</option>
                    {servers.map((srv) => (
                      <option key={srv.msdbs_id} value={srv.msdbs_id}>
                        {srv.msdbs_name}
                      </option>
                    ))}
                  </select>
                </div>

                {serverId && (
                  <>
                    <div className="mb-3">
                      <label>Data Directory</label>
                      <select
                        className="form-select"
                        value={mounts?.mounts?.datadir || ""}
                        onChange={(e) =>
                          setMounts((prev) => ({
                            server: serverId,
                            mounts: {
                              ...prev.mounts,
                              datadir: e.target.value,
                            },
                          }))
                        }
                      >
                        <option value="" key="mnt1">-- Select Data Directory --</option>
                        {availableMounts.map((m) => (
                          <option key={`${m.msdbsm_id}-mnt1`} value={m.msdbsm_id}>
                            {m.msdbsm_path}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="mb-3">
                      <label>Log Directory</label>
                      <select
                        className="form-select"
                        value={mounts?.mounts?.log_dir || ""}
                        onChange={(e) =>
                          setMounts((prev) => ({
                            server: serverId,
                            mounts: {
                              ...prev.mounts,
                              log_dir: e.target.value,
                            },
                          }))
                        }
                      >
                        <option key="mnt2" value="">-- Select Log Directory --</option>
                        {availableMounts.map((m) => (
                          <option key={`${m.msdbsm_id}-mnt2`} value={m.msdbsm_id}>
                            {m.msdbsm_path}
                          </option>
                        ))}
                      </select>
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        </div>
        <div className="col-lg-6"></div>
      </div>
    );
  }
);
