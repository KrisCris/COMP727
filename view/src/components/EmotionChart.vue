<template>
  <div id="charts" style="width: 700px; height: 400px"></div>
</template>

<script>
export default {
  name: "EmotionChart",
  data: () => ({
    chart: null,
    emotionTable: ["angry","fear", "sad","neutral","surprise","happy"],
  }),
  mounted() {
    this.drawLine();
  },
  methods: {
    updateChart(x, y) {
      if (this.chart == null) {
        this.drawLine();
      }
      var opt = this.chart.getOption();
      var data = opt.series[0].data;
      if (opt.xAxis[0].data.length > 1440) {
        opt.xAxis[0].data.shift();
      }
      opt.xAxis[0].data.push(x);
      if (data.length > 1440) {
        data.shift();
      }
      data.push(y);
      this.chart.setOption(opt);
    },
    drawLine() {
      if (this.chart != null) return;
      var that = this;
      this.chart = this.$echarts.init(document.getElementById("charts"));
      // 绘制图表
      this.chart.setOption({
        grid: {
          x: 80,
        },
        xAxis: {
          type: "category",
          data: [
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
            // "00:00",
          ],
          axisLabel: {
            show: true,
            color: "white",
          },
        },
        yAxis: {
          type: "value",
          max: 5,
          min: 0,
          offset: 0,
          axisLabel: {
            show: true,
            interval: "auto", // {number}
            color: "white",
            align: "right",
            fontSize: 15,
            formatter: function (value, index) {
              return that.emotionTable[value];
            }, // Template formatter!
          },
        },
        series: [
          {
            data: [
              // 3,
              // 3, 
              // 3, 
              // 3, 
              // 3, 
              // 3, 
              // 3, 
              // 3, 
              // 3, 
              // 3
              ],
            type: "line",
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