import { useEffect, useState } from "react";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../utils/Loading";

const MountSelector = ({ serverId, mounts, setMounts, errors, setErrors, serNmounts, setSerNMounts }) => {
  const [availableMounts, setAvailableMounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!serverId) return;

    async function fetchMounts() {
      try {
        setLoading(true);
        setAvailableMounts([]);
        setError("");
        const res = await DbOpsApi.getserversamountll(serverId);
        setAvailableMounts(res.data?.mounts || []);
      } catch (err) {
        setError("Failed to load mounts");
      } finally {
        setLoading(false);
      }
    }

    fetchMounts();
  }, [serverId]);

  if (loading) return <Loading tags="div" />;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <>
      <div className="mb-3">
        {errors.datadir && (
          <div className="alert alert-danger alert-dismissible fade show" role="alert">
            <i className="bi bi-exclamation-octagon me-1"></i>
            {errors.datadir}
          </div>
        )}
        <label>Data Directory</label>
        <select
          className={`form-select ${errors.datadir ? "is-invalid" : ""}`}
          value={mounts.mounts?.datadir || ""}
          onChange={(e) => {
            setSerNMounts((prev) => ({
              ...prev,
              mounts: { ...prev.mounts, datadir: e.target.options[e.target.selectedIndex].text },
            }));            
            setMounts((prev) => ({
              ...prev,
              mounts: { ...prev.mounts, datadir: e.target.value },
            }));
            setErrors((prev) => ({ ...prev, datadir: "" }));
          }}
        >
          <option value="">-- Select Data Directory --</option>
          {availableMounts.map((m) => (
            <option key={`${m.msdbsm_id}-data`} value={m.msdbsm_id}>
              {m.msdbsm_path}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        {errors.log_dir && (
          <div className="alert alert-danger alert-dismissible fade show" role="alert">
            <i className="bi bi-exclamation-octagon me-1"></i>
            {errors.log_dir}
          </div>
        )}
        <label>Log Directory</label>
        <select
          className={`form-select ${errors.log_dir ? "is-invalid" : ""}`}
          value={mounts.mounts?.log_dir || ""}
          onChange={(e) => {
            setSerNMounts((prev) => ({
              ...prev,
              mounts: { ...prev.mounts, log_dir: e.target.options[e.target.selectedIndex].text },
            }));
            setMounts((prev) => ({
              ...prev,
              mounts: { ...prev.mounts, log_dir: e.target.value },
            }));
            setErrors((prev) => ({ ...prev, log_dir: "" }));
          }}
        >
          <option value="">-- Select Log Directory --</option>
          {availableMounts.map((m) => (
            <option key={`${m.msdbsm_id}-log`} value={m.msdbsm_id}>
              {m.msdbsm_path}
            </option>
          ))}
        </select>
      </div>
    </>
  );
};

export default MountSelector;



/*
import { useEffect, useState } from "react";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../utils/Loading";

const MountSelector = ({ serverId, mounts, setMounts,errors, setErrors }) => {
  const [availableMounts, setAvailableMounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchMounts() {
      try {
        setLoading(true);
        setAvailableMounts([]);
        const res = await DbOpsApi.getserversamountll(serverId);
        setAvailableMounts(res.data?.mounts || []);
      } catch (err) {
        setError("Failed to load mounts");
      } finally {
        setLoading(false);
      }
    }

    fetchMounts();
  }, [serverId]);

  if (loading) return <Loading tags="div"/>
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <>
      <div className="mb-3">
                    {errors.datadir && (
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-octagon me-1"></i>
                    {errors.datadir}
              </div>
            )}
        <label>Data Directory</label>
        <select
          className={`form-select ${errors.datadir ? "is-invalid" : ""}`}
          value={mounts?.mounts?.datadir || ""}

          onChange={(e) => {
            setMounts((prev) => ({
              server: serverId,
              mounts: {
                ...prev.mounts,
                datadir: e.target.value,
              },
            }));
            setErrors((prev) => ({ ...prev, datadir: "" }));
          }}          
        >
          <option value="">-- Select Data Directory --</option>
          {availableMounts.map((m) => (
            <option key={`${m.msdbsm_id}-data`} value={m.msdbsm_id}>
              {m.msdbsm_path}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
                    {errors.log_dir && (
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-octagon me-1"></i>
                    {errors.log_dir}
              </div>
            )}
        <label>Log Directory</label>
        <select
          className={`form-select ${errors.log_dir ? "is-invalid" : ""}`}
          value={mounts?.mounts?.log_dir || ""}
          onChange={(e) => {
            setMounts((prev) => ({
              server: serverId,
              mounts: {
                ...prev.mounts,
                log_dir: e.target.value,
              },
            }));
            setErrors((prev) => ({ ...prev, log_dir: "" }));
          }}
        >
          <option value="">-- Select Log Directory --</option>
          {availableMounts.map((m) => (
            <option key={`${m.msdbsm_id}-log`} value={m.msdbsm_id}>
              {m.msdbsm_path}
            </option>
          ))}
        </select>
      </div>
    </>
  );
};

export default MountSelector;
*/
