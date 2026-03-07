import { useEffect, useState } from "react";
import AwsAcctApi from "../../api/AwsAcctApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function ViewRdsAWSaccount({ aid }) {
  const [accountData, setAccountData] = useState(null);
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
        const response = await AwsAcctApi.getawsacbyid(aid);
        setAccountData(response.data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Failed to AWS Account data.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [aid]);

  return (
    <div className="row">
      <div className="card">
        <div className="card-header">
          <h5 className="" style={{ marginBottom: "0px" }}>
            <strong>AWS Account Details</strong>
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
                <div className="col-md-3">
                  <label className="form-label">AWS Account ID</label>
                  <p>
                    <strong>{accountData?.account_number}</strong>
                  </p>
                </div>
                <div className="col-md-3">
                  <label className="form-label">Business Unit</label>
                  <p>
                    <strong>{accountData?.account_alias}</strong>
                  </p>
                </div>
                <div className="col-md-3">
                  <label className="form-label">Account Orginization</label>
                  <p>
                    <strong>{accountData?.account_org}</strong>
                  </p>
                </div>
                <div className="col-md-3">
                  <label className="form-label">Account Status</label>
                  <p>
                    <strong>
                      {accountData?.account_status ? "Active" : "Inactive"}
                    </strong>
                  </p>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
