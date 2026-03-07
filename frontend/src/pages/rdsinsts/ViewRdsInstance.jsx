import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import "./ViewRdsInstance.css";

export function ViewRdsInstance({ riid }) {
  const [rdsData, setRdsData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await RdsApi.getRdsInstanceDetail(riid);
        setRdsData(response.data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Failed to AWS Account data.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [riid]);

  const tags = parseTagList(rdsData?.rds_taglist);

  function parseTagList(tagString) {
    if (!tagString || tagString.trim() === "" || tagString.trim() === "[]") {
      return [];
    }

    try {
      const parsed = JSON.parse(tagString);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }

  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 className="" style={{ marginBottom: "0px" }}>
            <strong>RDS Details</strong>
          </h5>
        </div>
        <div
          className="card-body"
          style={{
            marginTop: "20px",
            paddingBottom: "0px",
            minHeight: "150px",
          }}
        >
          <div className="row">
            {error ? (
              <ErrorCard message={error} />
            ) : loading ? (
              <Loading />
            ) : (
              <>
                <div className="row">
                  {" "}
                  <div className="col-md-3 info-row">
                    <label className="form-label">Instance Identifier</label>
                    <p>
                      <strong>{rdsData?.rds_identifier}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Instance Endpoint</label>
                    <p>
                      <strong>{rdsData?.rds_endpoint}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Instance AZ</label>
                    <p>
                      <strong>{rdsData?.rds_az}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Instance Status</label>
                    <p>
                      <strong>{rdsData?.rds_inststatus}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Instance Class</label>
                    <p>
                      <strong>{rdsData?.rds_instanceclass}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">RDS Engine</label>
                    <p>
                      <strong>{rdsData?.rds_engine}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Parameter group</label>
                    <p>
                      <strong>{rdsData?.rds_paramgroup}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">RDS AZ</label>
                    <p>
                      <strong>{rdsData?.rds_az}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Engine Version</label>
                    <p>
                      <strong>{rdsData?.rds_enginever}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Lisence Model</label>
                    <p>
                      <strong>{rdsData?.rds_lisencemodel}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Storage Type</label>
                    <p>
                      <strong>{rdsData?.rds_storagetype}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Copy Tags to Snapshot</label>
                    <p>
                      <strong>{rdsData?.rds_copytagsnapshot}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Storage Encrypted</label>
                    <p>
                      <strong>{rdsData?.rds_storageencrypted}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Lisence Model</label>
                    <p>
                      <strong>{rdsData?.rds_lisencemodel}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Delete Protection</label>
                    <p>
                      <strong>{rdsData?.rds_deleteprotection}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Endpoint</label>
                    <p>
                      <strong>{rdsData?.rds_endpoint}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Port</label>
                    <p>
                      <strong>{rdsData?.rds_port}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">VPC</label>
                    <p>
                      <strong>{rdsData?.rds_vpc}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Subnet Group</label>
                    <p>
                      <strong>{rdsData?.rds_subnetgrp}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Subnets</label>
                    <p>
                      <strong>
                      {rdsData?.rds_subnets.split(",").map((subnet, index) => (
        <div key={index}>{subnet}</div>
      ))}
                        </strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Backup Retention</label>
                    <p>
                      <strong>{rdsData?.rds_backupretention} Days</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Instance Role</label>
                    <p>
                      <strong>{rdsData?.rds_dbinstrole}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Cluster Identifier</label>
                    <p>
                      <strong>{rdsData?.rds_clusteridentifier}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Cluster Endpoint</label>
                    <p>
                      <strong>{rdsData?.rds_clusterendpoint}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Master User</label>
                    <p>
                      <strong>{rdsData?.rds_masteruser}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Multi AZ</label>
                    <p>
                      <strong>{rdsData?.rds_multiaz}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Created Date</label>
                    <p>
                      <strong>{rdsData?.rds_instcreatetime}</strong>
                    </p>
                  </div>
                  <div className="col-md-3 info-row">
                    <label className="form-label">Last Collected Date</label>
                    <p>
                      <strong>{rdsData?.created_at}</strong>
                    </p>
                  </div>                                  
                </div>
                <div className="row">
                  <div className="card-header" style={{ paddingLeft: "5px" }}>
                    Tags
                  </div>
                  <div
                    className="card-body"
                    style={{
                      marginRight: "0px",
                      marginTop: "20px",
                      paddingLeft: "0px",
                    }}
                  >
                    {tags.length === 0 ? (
                      <p style={{ paddingLeft: "5px" }} className="text-dark">
                        <i className="bi bi-exclamation-triangle me-1"></i>No
                        tags available
                      </p>
                    ) : (
                      <>
                        {tags.map((tag) => (
                          <div
                            key={tag.Key}
                            className="badge border-secondary border-1 text-primary"
                          >
                            <span className="btn-key">{tag.Key}</span>
                            <span className="btn-value">{tag.Value}</span>
                          </div>
                        ))}
                      </>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
