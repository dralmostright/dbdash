import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import { NoData } from "../../components/utils/NoData";

export default function RdsEngineAcountCount() {
    const [tableData, setTableData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function fetchData() {
            try {
                setLoading(true);
                const response = await RdsApi.getRdsEngineAccountCount();
                const accountsData = response.data;
                setTableData(accountsData);
                setError(null);
            } catch (err) {
                console.error(err);
                setError("Failed to load engine version for account data.");
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, []);

    if (loading) return (
                <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
            <div className="card-body">
                <h5 className="card-title">RDS Version <span>/Account</span></h5>
                <Loading />
            </div>
        </div>
        </div>
    );
    if (error) return (
        <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
            <div className="card-body">
                <h5 className="card-title">RDS Version <span>/Account</span></h5>
                <ErrorCard message={error} />
            </div>
        </div>
        </div>
    );
    if (!tableData) return null;

    return (
            <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
            <div className="card-body">
                <h5 className="card-title">
                    RDS Version <span>/ Account</span>
                </h5>
                {!tableData || tableData.length === 0 ? (
            <NoData />
          ) : (
                <table className="table activity table-sm table-hover table-bordered">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Engine Type</th>
                            <th scope="col">Engine Version</th>
                            <th scope="col">Engine Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            tableData.map((tr, key) => (
                                <tr key={key}>
                                    <td> {key + 1}</td>
                                    <td>{tr.rds_engine}</td>
                                    <td>{tr.rds_enginever}</td>
                                    <td>{tr.rds_count}</td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table>
          )}
            </div>
        </div>
        </div>
    )
}
