import { useEffect, useState } from "react";
import StackedLineChart from "../../components/charts/StackedLineChart";
import RdsApi from "../../api/RdsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import { NoData } from "../../components/utils/NoData";

export default function RdsAzCountPerAccount() {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function fetchData() {
      try {
        setLoading(true);

        const response = await RdsApi.getRdsAzAccountCount();
        const azData = response.data;

        if (!isMounted) return;
        const azSet = new Set();
        azData.forEach((acc) =>
          acc.data.forEach((row) => azSet.add(row.rds_az))
        );
        const azList = Array.from(azSet).sort(); 

        const datasets = azList.map((az) => ({
          label: az,
          data: azData.map((acc) => {
            const found = acc.data.find((d) => d.rds_az === az);
            return found ? found.rds_count : 0;
          }),
        }));

        const labels = azData.map((acc) => acc.account_alias);

        setChartData({ labels, datasets });
        setError(null);
      } catch (err) {
        console.error(err);
        if (isMounted) setError("Failed to load chart data.");
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchData();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
          <div className="card-body">
            <h5 className="card-title">
              RDS Instance Count <span>/AZ - Business Unit</span>
            </h5>
            <Loading />
          </div>
        </div>
      </div>
    );
  if (error)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
          <div className="card-body">
            <h5 className="card-title">
              RDS Instance Count <span>/AZ - Business Unit</span>
            </h5>
            <ErrorCard message={error} />
          </div>
        </div>
      </div>
    );
  if (!chartData) return null;

  return (
    <div className="col-12">
      <div className="card" style={{ minHeight: "400px" }}>
        <div className="card-body">
          <h5 className="card-title">
            RDS Instance Count <span>/AZ - Business Unit</span>
          </h5>
          {!chartData || chartData.datasets.length === 0 ? (
            <NoData />
          ) : (
            <StackedLineChart chartId="myChart" chartData={chartData} />
          )}
        </div>
      </div>
    </div>
  );
}
