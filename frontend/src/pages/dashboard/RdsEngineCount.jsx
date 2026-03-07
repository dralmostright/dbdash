import React, { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import DoughnutChart from "../../components/charts/DoughnutChart";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import { NoData } from "../../components/utils/NoData";

export default function RdsEngineCount() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchChartData() {
      try {
        setLoading(true);
        const response = await RdsApi.getRdsEngineCount();
        const transformed = response.data.map((item) => ({
          name: item.rds_engine,
          value: item.rds_count,
        }));

        setData(transformed);
      } catch (err) {
        console.error(err);
        setError("Failed to load Engine Distribution Data");
      } finally {
        setLoading(false);
      }
    }

    fetchChartData();
  }, []);

  if (loading)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "350px" }}>
          <div className="card-body">
            <h5 className="card-title">
              RDS Distribution <span>/Engine</span>
            </h5>
            <Loading />
          </div>
        </div>
      </div>
    );
  if (error)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "350px" }}>
          <div className="card-body">
            <h5 className="card-title">
              RDS Distribution <span>/Engine</span>
            </h5>
            <ErrorCard message={error} />
          </div>
        </div>
      </div>
    );
  return (
    <div className="col-12">
      <div className="card" style={{ minHeight: "350px" }}>
        <div className="card-body">
          <h5 className="card-title">
            RDS Distribution <span>/Engine</span>
          </h5>
          {!data || data.length === 0 ? (
            <NoData />
          ) : (
            <DoughnutChart chartData={data} />
          )}
        </div>
      </div>
    </div>
  );
}
