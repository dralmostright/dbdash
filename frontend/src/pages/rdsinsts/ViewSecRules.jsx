import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function ViewSecRules({ riid }) {
  const [secrulesdata, SetSecRulesData] = useState(null);
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
        const response = await RdsApi.getRdsSecRules(riid);
        SetSecRulesData(response.data);
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

  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 className="" style={{ marginBottom: "0px" }}>
            <strong>Security Rules for the RDS</strong>
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
                {secrulesdata == null ? (
                  <div className="d-flex justify-content-center center-absolute" style={{ top: "65%" }}>
                    <h4 className="text-warning">
                      <i class="bi bi-exclamation-triangle-fill"></i> No Data found for Security Rules
                    </h4>
                  </div>
                ) : (
                  <>
                    <DataTable value={secrulesdata}
                      paginator
                      stripedRows
                      size="small"
                      rows={10}
                      rowsPerPageOptions={[10, 20]}
                      showGridlines >
                      <Column
                        header="S.N."
                        body={(_, options) => options.rowIndex + 1}
                        style={{ width: "70px" }}
                      />
                      <Column field="sec_group_name" header="Security Group"></Column>
                      <Column field="sec_gpid" header="Gropup Id"></Column>
                      <Column field="sec_rule_type" header="Rule Type"></Column>
                      <Column field="sec_port_range" header="Port Range"></Column>
                      <Column field="sec_ip_ranges" header="CIDR Range"></Column>
                    </DataTable>
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
