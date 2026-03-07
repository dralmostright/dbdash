import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function ViewRdsParameters({ riid }) {
  const [rdsinstparams, SetRdsInstParams] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const headerCluster = (
    <div className="flex flex-wrap align-items-center justify-content-between gap-2">
      <span className="text-xl text-900 font-bold">Cluster RDS Parameters</span>
    </div>
  );

  const headerInstance = (
    <div className="flex flex-wrap align-items-center justify-content-between gap-2">
      <span className="text-xl text-900 font-bold">Instance RDS Parameters</span>
    </div>
  );

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
        const response = await RdsApi.getRdsInstParams(riid);
        SetRdsInstParams(response.data);
        //console.log(secrulesdata)
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

  //console.log()

  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 className="" style={{ marginBottom: "0px" }}>
            <strong>RDS Non-default database parameters</strong>
          </h5>
        </div>
        <div
          className="card-body"
          style={{ marginTop: "20px", paddingBottom: "0px", minHeight: "80px", marginBottom: "20px" }}
        >
          <div className="row">
            {error ? (
              <ErrorCard message={error} />
            ) : loading ? (
              <Loading />
            ) : (
              <>
                {" "}
                {rdsinstparams == null ? (
                  <div
                    className="d-flex justify-content-center center-absolute"
                    style={{ top: "65%" }}
                  >
                    <h4 className="text-warning">
                      <i class="bi bi-exclamation-triangle-fill"></i> No Data
                      found for RDS DB parameters
                    </h4>
                  </div>
                ) : (
                  <>
                    <div className="col-lg-6">
                      {rdsinstparams.filter(
                        (params) => params.param_type === "Cluster"
                      ) == null ? (
                        <div>No data</div>
                      ) : (
                        <DataTable
                          value={rdsinstparams.filter(
                            (params) => params.param_type === "Cluster"
                          )}
                          header={headerCluster}
                          paginator
                          stripedRows
                          size="small"
                          rows={10}
                          rowsPerPageOptions={[10, 20]}
                          showGridlines
                        >
                          <Column
                            header="S.N."
                            body={(_, options) => options.rowIndex + 1}
                            style={{ width: "70px" }}
                          />
                          <Column
                            field="param_name"
                            header="Parameter Name"
                            sortable
                          ></Column>
                          <Column
                            field="param_value"
                            header="Parameter Value"
                          ></Column>
                        </DataTable>
                      )}
                    </div>
                    <div className="col-lg-6">
                      {rdsinstparams.filter(
                        (params) => params.param_type === "Instance"
                      ) == null ? (
                        <div>No data</div>
                      ) : (
                        <DataTable
                          value={rdsinstparams.filter(
                            (params) => params.param_type === "Instance"
                          )}
                          header={headerInstance}
                          paginator
                          stripedRows
                          size="small"
                          rows={10}
                          rowsPerPageOptions={[10, 20]}
                          showGridlines
                        >
                          <Column
                            header="S.N."
                            body={(_, options) => options.rowIndex + 1}
                            style={{ width: "70px" }}
                          />
                          <Column
                            field="param_name"
                            header="Parameter Name"
                            sortable
                          ></Column>
                          <Column
                            field="param_value"
                            header="Parameter Value"
                          ></Column>
                        </DataTable>
                      )}
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
