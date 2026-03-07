import { useState, useEffect } from "react";
import ErrorCard from "../utils/ErrorCard";
import MountSelector from "./MountSelector";
import DbOpsApi from "../../api/DbOpsApi";
import { Loading } from "../utils/Loading";

export const ServerSelection = ({ serverId, setServerId, mounts, setMounts, errors, setErrors, serNmounts, setSerNMounts }) => {
    const [servers, setServers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    function sleep(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }
    //await sleep(1000);

    useEffect(() => {
        async function fetchServers() {
            try {
                setLoading(true);
                setError("");
                //await sleep(100000);
                const res = await DbOpsApi.getserversall();
                setServers(res.data);
            } catch (err) {
                setError("Failed to load servers");
            } finally {
                setLoading(false);
            }
        }
        fetchServers();
    }, []);

    return (
        <div className="col-lg-6" style={{ minHeight: "500px" }}>
            {errors.server && (
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-octagon me-1"></i>
                    {errors.server}
              </div>
            )}
            <h5 className="card-title">Server & Mount Selection</h5>

            {loading && <Loading tags="div"/>}
            {error && <ErrorCard message={error} />}
            {!loading && !error && (
                <>
                    <div className="mb-3">
                        <label>Server</label>
                        <select
                            className={`form-select ${errors.server ? "is-invalid" : ""}`}
                            value={serverId}
                            onChange={(e) => {
                                setServerId(e.target.value);
                                //setMounts({});
                                setSerNMounts({ server: e.target.options[e.target.selectedIndex].text, mounts : {} })
                                setMounts({ server: e.target.value, mounts : {} });
                                setErrors((prev) => ({ ...prev, server: "" }));
                            }}
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
                        <MountSelector
                            serverId={serverId}
                            mounts={mounts}
                            setMounts={setMounts}
                            errors={errors}
                            setErrors={setErrors}
                            serNmounts = {serNmounts} 
                            setSerNMounts={setSerNMounts}
                        />
                    )}
                </>
            )}
        </div>
    );
};
