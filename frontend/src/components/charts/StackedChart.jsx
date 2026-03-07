import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

export default function StackedChart({ chartData }) {
  const chartRef = useRef(null);
  const instanceRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !chartData) return;

    if (!instanceRef.current) {
      instanceRef.current = echarts.init(chartRef.current);
    }

    const { labels, datasets } = chartData;

    const series = datasets.map(ds => ({
      name: ds.label,
      type: "bar",
      stack: "total",
      emphasis: { focus: "series" },
      label: { show: false }, // hide numbers
      data: ds.data
    }));

    instanceRef.current.setOption({
      tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
      legend: {
        orient: "vertical",
        right: 10,
        top: "middle",
        data: datasets.map(ds => ds.label)
      },
      grid: {
        left: "3%",
        right: "20%", // 🔹 leave enough space for legend
        bottom: "3%",
        containLabel: true
      },
      xAxis: {
        type: "category",
        data: labels,
        axisLabel: { rotate: 45, interval: 0 }
      },
      yAxis: { type: "value" },
      series
    });

    const resizeHandler = () => instanceRef.current.resize();
    window.addEventListener("resize", resizeHandler);

    return () => {
      window.removeEventListener("resize", resizeHandler);
      if (instanceRef.current) {
        instanceRef.current.dispose();
        instanceRef.current = null;
      }
    };
  }, [chartData]);

  return <div ref={chartRef} style={{ width: "100%", height: "400px" }} />;
}
