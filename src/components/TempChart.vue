<template>
  <div id="tempCharts" style="width: 700px; height: 400px"></div>
</template>

<script>
export default {
  name: "TempChart",
  data: () => ({
    chart: null,
  }),
  mounted() {
    this.drawLine();
  },
  methods: {
    updateChart(x, y1, y2) {
      if (this.chart == null) {
        this.drawLine();
      }
      var opt = this.chart.getOption();
      var data1 = opt.series[0].data;
      var data2 = opt.series[1].data;
      if (opt.xAxis[0].data.length > 80000) {
        opt.xAxis[0].data.shift();
      }
      opt.xAxis[0].data.push(x);
      if (data1.length > 80000) {
        data1.shift();
      }
      if (data2.length > 80000) {
        data2.shift();
      }
      data1.push(y1);
      data2.push(y2);
      this.chart.setOption(opt);
    },
    drawLine() {
      if (this.chart != null) return;
      var that = this;
      this.chart = this.$echarts.init(document.getElementById("tempCharts"));
      // 绘制图表
      this.chart.setOption({
        grid: {
          x: 80,
        },
        legend: {
          borderColor: "white",
        },
        xAxis: {
          type: "category",
          color: "white",
          axisLabel: {
            show: true,
            color: "white",
            fontSize: 15,
          },
          axisLine: {
            lineStyle: {
              color: "white",
            },
          },
          data: [],
        },
        yAxis: [
          {
            type: "value",
            name: "Temperature(℃)",
            splitLine: {
              show: false,
            },
            axisLine: {
              lineStyle: {
                color: "#B5B5B5",
              },
            },
            nameTextStyle: {
              color: "white",
            },
            color: "white",
            axisLabel: {
              show: true,
              color: "#F78539",
              fontSize: 15,
            },
          },
          {
            type: "value",
            max: 100,
            min: 0,
            splitLine: {
              show: false,
            },
            axisLine: {
              lineStyle: {
                color: "#B5B5B5",
              },
            },
            nameTextStyle: {
              color: "white",
            },
            name: "Humidity(%)",
            axisLabel: {
              show: true,
              color: "#0090FF",
              fontSize: 15,
            },
          },
        ],
        series: [
          {
            data: [],
            type: "line",
            lineStyle: {
              color: "#F78539",
            },
            yAxisIndex: 0,
            symbol: "none",
            smooth: true,
          },
          {
            data: [],
            type: "line",
            lineStyle: {
              color: "#0090FF",
            },
            yAxisIndex: 1,
            symbol: "none",
            smooth: true,
          },
        ],
      });
    },
  },
};
</script>

<style>
</style>