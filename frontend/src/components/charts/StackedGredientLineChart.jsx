import React from "react";
import ReactECharts from "echarts-for-react";

const normalizeEngineName = (engine) => {
  engine = engine.toLowerCase();

  if (engine.startsWith("sqlserver")) return "sqlserver";
  if (engine.startsWith("postgres")) return "postgres";
  if (engine.startsWith("aurora-postgresql")) return "postgres";
  if (engine.startsWith("aurora-mysql")) return "mysql";
  if (engine === "mysql") return "mysql";
  if (engine.startsWith("oracle")) return "oracle";
  if (engine.startsWith("docdb")) return "documentdb";

  return engine;
};

export default function StackedGredientLineChart({ chartData }) {
  // Normalize the data
  const normalized = (chartData || []).map(item => ({
    rds_engine: normalizeEngineName(item?.name),
    rds_count: item?.value ?? 0
  }));

  const option = {
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: normalized.map(item => item.rds_engine),
      axisLabel: {
        rotate: 30,
        fontSize: 12,
      },
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "RDS Count",
        type: "line",
        smooth: true, // Smoothed curve
        data: normalized.map(item => item.rds_count),
        lineStyle: {
          width: 3,
          color: "#4F8EF7",
        },
        itemStyle: {
          color: "#4F8EF7",
        },
        areaStyle: {
          opacity: 0.7,
          color: {
            type: "linear",
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: "rgba(79, 142, 247, 0.6)" },
              { offset: 1, color: "rgba(79, 142, 247, 0.0)" },
            ],
          },
        },
      },
    ],
  };

  return (
    <ReactECharts
      option={option}
      style={{ height: "400px", width: "100%" }}
    />
  );
}
