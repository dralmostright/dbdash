import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

export default function DoughnutChart({ chartData }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !chartData) return;

    const chartInstance = echarts.init(chartRef.current);

    const options = {
      tooltip: {
        trigger: "item",
      },
      legend: {
        orient: "vertical",
        left: 0,        // 👈 Legend anchored left
        top: "middle",
      },
      series: [
        {
          name: "Engine Distribution",
          type: "pie",
          radius: ["40%", "70%"],
          center: ["70%", "50%"],
          avoidLabelOverlap: false,
          label: {
            show: false,
            position: "center",
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 18,
              fontWeight: "bold",
            },
          },
          labelLine: {
            show: false,
          },
          data: chartData, 
        },
      ],
    };

    chartInstance.setOption(options);

    const handleResize = () => chartInstance.resize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chartInstance.dispose();
    };
  }, [chartData]);

  return <div ref={chartRef} style={{ width: "100%", height: "375px" }} />;
}
