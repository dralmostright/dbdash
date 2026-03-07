import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function ViewRdsHwConfig({ riid }) {
  const [rdshwdata, SetRdsHWData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        /*
        function sleep(ms) {
          return new Promise((resolve) => setTimeout(resolve, ms));
        }
        //await sleep(1000);
        */
        const response = await RdsApi.getRdsHwDetail(riid);
        SetRdsHWData(response.data.rds_hw_details);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Failed to Instance class configuration.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [riid]);

  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 className="" style={{ marginBottom: "0px" }}>
            <strong>Instance/EBS-optimized Class Details</strong>
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
                {rdshwdata == null ? (
                  <div className="d-flex justify-content-center center-absolute" style={{top: "65%"}}>
                    <h4 className="text-warning">
                      <i className="bi bi-exclamation-triangle-fill"></i> No Data found for Instance Class
                    </h4>
                  </div>
                ) : (
                  <>
                  <div className="col-md-3">
                      <label className="form-label">Instance Family</label>
                      <p>
                        <strong>{rdshwdata?.ec2_hw_type}</strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Instance Class</label>
                      <p>
                        <strong>{rdshwdata?.rds_hw_model}</strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Memory (GiB)</label>
                      <p>
                        <strong>{rdshwdata?.rds_hw_mem}</strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Instance vCPU</label>
                      <p>
                        <strong>{rdshwdata?.rds_hw_vcpu}</strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Instance Storage</label>
                      <p>
                        <strong>
                          {rdshwdata?.rds_hw_storage }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Network Performance (Gbps)</label>
                      <p>
                        <strong>
                          {rdshwdata?.rds_hw_net_gbps }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Baseline bandwidth (Mbps)</label>
                      <p>
                        <strong>
                          {rdshwdata?.ec2_hw_basebandwm }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Maximum bandwidth (Mbps)</label>
                      <p>
                        <strong>
                          {rdshwdata?.ec2_hw_maxbandwm == null ? "N/A" : rdshwdata?.ec2_hw_maxbandwm }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Baseline throughput (MB/s, 128 KiB I/O)</label>
                      <p>
                        <strong>
                          {rdshwdata?.ec2_hw_basethroputm }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Maximum throughput (MB/s, 128 KiB I/O)</label>
                      <p>
                        <strong>
                        {rdshwdata?.ec2_hw_maxthroputm == null ? "N/A" : rdshwdata?.ec2_hw_maxthroputm }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Baseline IOPS (16 KiB I/O)</label>
                      <p>
                        <strong>
                          {rdshwdata?.ec2_hw_baseiopsm }
                        </strong>
                      </p>
                    </div>
                    <div className="col-md-3">
                      <label className="form-label">Maximum IOPS (16 KiB I/O)</label>
                      <p>
                        <strong>
                        {rdshwdata?.ec2_hw_maxiopswm == null ? "N/A" : rdshwdata?.ec2_hw_maxiopswm }
                        </strong>
                      </p>
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
