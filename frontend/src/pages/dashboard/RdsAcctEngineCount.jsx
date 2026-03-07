import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { StackedLinePieChart } from "../../components/charts/StackedLinePieChart";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import { NoData } from "../../components/utils/NoData";

export function RdsAcctEngineCount() {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadRdsUpCount = async () => {
        try {
            const res = await RdsApi.getRdsAccountEngineCount();
            setChartData(res.data);
        } catch (error) {
            console.log(error)
            setError("Failed to load chart data")
        } finally {
            setLoading(false)
        }
    };

    loadRdsUpCount();
}, []);


if (loading) return (
    <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
        <div className="card-body">
            <h5 className="card-title">RDS Instance <span>/Business Unit</span></h5>
            <Loading />
        </div>
        </div>
    </div>
);
if (error) return (
    <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
        <div className="card-body">
            <h5 className="card-title">RDS Instance <span>/Business Unit</span></h5>
            <ErrorCard message={ error }/>
        </div>
        </div>
    </div>
);
if (chartData.dataset === null) return null;

return (
    <div className="col-12">
        <div className="card">
            <div className="card-body" style={{ minHeight: "400px" }}>
                <h5 className="card-title">RDS Instance <span>/Business Unit</span></h5>
                { !chartData?.dataset || chartData.dataset.length === 0 ? <NoData /> : <StackedLinePieChart chartId="myChart" chartData={chartData} /> }
            </div>
        </div>
    </div>
);
}