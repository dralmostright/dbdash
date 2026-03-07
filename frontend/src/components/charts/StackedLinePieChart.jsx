import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";

export function StackedLinePieChart({ chartData }) {
  const chartRef = useRef(null);
  const chart = useRef(null);

  useEffect(() => {
    if (!chartRef.current || !chartData?.dataset || chartData.dataset.length === 0) return;

    if (!chart.current) {
      chart.current = echarts.init(chartRef.current);
    }

    const source = chartData.dataset;

    const rowCount = source.length - 1; 
    const lineSeries = Array.from({ length: rowCount }).map(() => ({
      type: "line",
      smooth: true,
      seriesLayoutBy: "row",
      emphasis: { focus: "series" }
    }));

    const getPieEncode = (dimension) => {
      const pieData = source
        .slice(1)
        .map((row) => ({
          name: row[0],
          value: row[dimension]
        }))
        .filter((item) => item.value > 0);

      return {
        data: pieData,
        label: {
          formatter: (params) =>
            params.value === 0 ? "" : `${params.name}: ${params.value} (${params.percent}%)`
        }
      };
    };

    const initialEnvName = source[0][1];


    const pieSeries = {
      type: "pie",
      id: "pie",
      radius: "30%",
      center: ["50%", "20%"], 
      emphasis: { focus: "self" },
      ...getPieEncode(1)
    };

    const option = {
      legend: {
        top: 0, 
        left: "right",
        orient: "vertical"
      },
      tooltip: { trigger: "axis", showContent: false },
      dataset: { source },
      xAxis: {
        type: "category",
        axisLabel: {
          rotate: 90,
          interval: 0
        }
      },
      yAxis: { gridIndex: 0 },
      grid: {
        top: "50%",   
        left: "5%",   
        right: "5%",
        bottom: "10%"
      },
      series: [...lineSeries, pieSeries],
      title: [
        {
          text: `BU: ${initialEnvName}`,
          left: "center",
          top: "45%", 
          textStyle: {
            fontSize: 14,
            fontWeight: "bold"
          }
        }
      ]
    };

    chart.current.setOption(option);

    chart.current.on("updateAxisPointer", (event) => {
      const xAxisInfo = event.axesInfo?.[0];
      if (xAxisInfo) {
        const dimension = xAxisInfo.value + 1;
        const envName = source[0][dimension];
        const pieUpdate = getPieEncode(dimension);
        chart.current.setOption({
          series: {
            id: "pie",
            ...pieUpdate
          },
          title: [
            {
              text: `BU: ${envName}`,
              left: "center",
              top: "45%",
              textStyle: {
                fontSize: 14,
                fontWeight: "bold"
              }
            }
          ]
        });
      }
    });

    const handleResize = () => chart.current?.resize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.current?.dispose();
      chart.current = null;
    };
  }, [chartData]);

  return <div ref={chartRef} style={{ width: "100%", height: "600px" }} />;
}
