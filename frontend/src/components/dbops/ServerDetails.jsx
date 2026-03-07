import { useState, useEffect } from "react";
import { Loading } from "../utils/Loading";
import ErrorCard from "../utils/ErrorCard";
import DbOpsApi from "../../api/DbOpsApi";

export const ServerDetails = () => {
  const [details, setDetails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchServerDetails() {
      try {
        setLoading(true);
        setError("");
        const res = await DbOpsApi.getservernmsall(); 
        setDetails(res.data);
      } catch (err) {
        setError("Failed to load server details");
      } finally {
        setLoading(false);
      }
    }

    fetchServerDetails();
  }, []);

  return (
    <div className="col-lg-6">
      <h5 className="card-title">Server Details</h5>

      {loading && <Loading />}
      {error && <ErrorCard message={error} />}

      {!loading &&
        !error &&
        details.map((item) => (


          <div
            key={item.server.msdbs_id}
            style={{ minHeight: "150px" }}
          >

        <ul className="nav nav-tabs" >
          <li className="nav-item" >
            <button
              className="nav-link active"
              type="button"
            >
              {item.server.msdbs_name}
            </button>
          </li>
        </ul>

            <table class="table table-striped">
                <thead>
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Mount Point</th>
                    <th scope="col">Usage</th>
                  </tr>
                </thead>
                <tbody>
                {item.mounts?.map((mount, index) => (
                <tr key={mount.msdbsm_id}>
                    <th scope="row">{index + 1}</th>
                    <td>{mount.msdbsm_path}</td>
                    <td>{mount.msdbsm_usage} %</td>
                </tr>
              ))}
                </tbody>
              </table>
          </div>
        ))}
    </div>
  );
};

