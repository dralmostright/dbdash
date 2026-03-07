import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

export default function StackedLineChart({ chartData }) {
  const chartRef = useRef(null);
  const instanceRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !chartData) return;

    // Init chart once
    if (!instanceRef.current) {
      instanceRef.current = echarts.init(chartRef.current);
    }

    const { labels, datasets } = chartData;


const azSeries = datasets.map(ds => ({
  name: ds.label,
  type: "line",
  smooth: true,
  data: ds.data,
  stack: undefined, 
  lineStyle: { width: 2 }, 
  symbol: "circle",
  symbolSize: 4,
}));

const totalSeries = {
  name: "Total",
  type: "line",
  smooth: true,
  data: labels.map((_, idx) =>
    datasets.reduce((sum, ds) => sum + (ds.data[idx] ?? 0), 0)
  ),
  stack: undefined, 
  lineStyle: { width: 3 }, 
  symbol: "circle",
  symbolSize: 6,
  z: 10, 
};

const series = [...azSeries, totalSeries];

    instanceRef.current.setOption({
      tooltip: { trigger: "axis" },
      legend: {
        top: "5%",
        left: "right", 
      },
      grid: {
        left: "3%",
        right: "8%", 
        bottom: "3%",
        containLabel: true,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: labels,
        axisLabel: {
          rotate: 90, 
        },
      },
      yAxis: { type: "value" },
      series,
    });

    const handleResize = () => instanceRef.current.resize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      instanceRef.current.dispose();
      instanceRef.current = null;
    };
  }, [chartData]);

  return <div ref={chartRef} style={{ width: "100%", height: "400px" }} />;
}
