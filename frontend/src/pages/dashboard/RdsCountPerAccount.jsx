import { useEffect, useState } from "react";
import StackedChart from "../../components/charts/StackedChart";
import RdsApi from "../../api/RdsApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import { NoData } from "../../components/utils/NoData";

export default function RdsCountPerAccount() {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function fetchData() {
      try {
        setLoading(true);

        const response = await RdsApi.getAccountRdsCountPerDay();
        const accountsData = response.data;

        if (!isMounted) return;

        const allDatesSet = new Set();
        accountsData.forEach((acc) => {
          acc.data.forEach((d) => allDatesSet.add(d.date));
        });
        const labels = Array.from(allDatesSet).sort();

        const datasets = accountsData.map((acc) => {
          const dataMap = new Map(acc.data.map((d) => [d.date, d.rds_count]));
          const data = labels.map((date) => dataMap.get(date) ?? 0);
          return {
            label: acc.account_alias,
            data,
          };
        });

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

  //console.log(chartData)
  if (loading)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "400px" }}>
          <div className="card-body">
            <h5 className="card-title">
              RDS Instance Count <span>/Business Unit</span>
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
              RDS Instance Count <span>/Business Unit</span>
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
            RDS Instance Count <span>/Business Unit</span>
          </h5>
          {!chartData || chartData.datasets.length === 0 ? (
            <NoData />
          ) : (
            <StackedChart chartId="myChart" chartData={chartData} />
          )}
        </div>
      </div>
    </div>
  );
}
