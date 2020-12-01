<template>
  <v-app>
    <v-main class="cursorNone">
      <v-tabs v-model="tabs" centered>
        <v-tab>Main Page</v-tab>
        <v-tab>Emotion variation</v-tab>
        <v-tab>Environment variation</v-tab>
        <v-tab>setting</v-tab>
      </v-tabs>
      <v-tabs-items v-model="tabs">
        <!-- 主页 -->
        <v-tab-item>
          <v-card flat style="width: 800px; height: 480px">
            <v-row>
              <FlipClock
                style="margin-top: 50px; margin-bottom: 50px"
                class="mx-auto"
              />
            </v-row>
            <v-row>
              <v-col>
                <!-- 使用EmotionDetector.vue中的组件，监听内部发起的updateChart事件 -->
                <!-- 当updateChart事件发生时，执行updateChart函数 -->
                <!-- 使用EmotionDetector.vue中的组件，监听内部发起的workingTime事件 -->
                <!-- 当updateChart事件发生时，执行updateWorkingTime函数 -->
                <EmotionDetector
                  class="xs-6 sm-6 md-6"
                  @updateChart="updateChart"
                  @workingTime="updateWorkingTime"
                  @shouldRest="emotionRemind"
                  ref="emotion"
                />
                <!-- ↑ ref='emotion' 表示将该组件命名为emotion,以便在下方js代码中用$refs属性获取 -->
                <v-divider vertical></v-divider>
              </v-col>
              <v-col>
                <v-row>
                  <v-card elevation="3" outlined style="width: 93%">
                    <v-row>
                      <!--ref='temperature' 表示将该组件命名为temperature,以便在下方js代码中用$refs属性获取 -->
                      <Temperature style="width: 27%" ref="temperature" />
                      <v-divider vertical></v-divider>
                      <!--ref='humidity' 表示将该组件命名为humidity,以便在下方js代码中用$refs属性获取 -->
                      <Humidity style="width: 27%" ref="humidity" />
                      <v-divider vertical></v-divider>
                      <!--ref='weather' 表示将该组件命名为weather,以便在下方js代码中用$refs属性获取 -->
                      <Weather style="width: 27%" ref="weather" />
                    </v-row>
                  </v-card>
                </v-row>
                <v-row>
                  <!-- parentThreshouldTime是RelaxReminder.vue中，自定义组件的一个属性 -->
                  <!-- 此处将picker变量与该属性绑定 -->
                  <RelaxReminder
                    :parentThreshouldTime="picker"
                    style="width: 93%"
                    ref="reminder"
                  />
                  <!-- ↑ ref='reminder' 表示将该组件命名为reminder,以便在下方js代码中用$refs属性获取 -->
                </v-row>
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

        <!-- 心情变化表格页 -->
        <v-tab-item :eager="true" style="width: 800px; height: 480px">
          <v-row justify="center">
            <EmotionChart ref="chart" />
          </v-row>
        </v-tab-item>

        <!-- 环境变化表格页 -->
        <v-tab-item :eager="true" style="width: 800px; height: 480px">
          <v-row justify="center">
            <TempChart ref="tempChart" />
          </v-row>
        </v-tab-item>
        <v-tab-item style="width: 800px; height: 480px">
          <v-col>
            <div style="height: 50px"></div>
            <v-row justify="center">
              <img v-bind:src="pic" alt="" style="width:150px;height:150px;margin-top:70px"/>
              <v-time-picker
                v-model="picker"
                :landscape="$vuetify.breakpoint.smAndUp"
                format="24hr"
              ></v-time-picker>
            </v-row>
          </v-col>
        </v-tab-item>
      </v-tabs-items>
    </v-main>
  </v-app>
</template>

<script>
//从其他文件中导入组件
import FlipClock from "kuan-vue-flip-clock";
import EmotionDetector from "./components/EmotionDetector";
import Temperature from "./components/Temperature";
import Humidity from "./components/Humidity";
import EmotionChart from "./components/EmotionChart";
import TempChart from "./components/TempChart";
import RelaxReminder from "./components/RelaxReminder";
import Weather from "./components/weather";
export default {
  name: "App",
  //注册被导入的组件组件
  components: {
    FlipClock,
    EmotionDetector,
    Temperature,
    EmotionChart,
    Humidity,
    RelaxReminder,
    TempChart,
    Weather,
  },
  data: () => ({
    //用于切换tabs
    tabs: null,
    //保存温度数据
    temperature: "0.0",
    //保存湿度数据
    humidity: "0.0",
    //保存天气数据
    weather: "",
    //保存时间选择器的数据
    picker: "00:30",
    pic: "",
  }),
  methods: {
    //更新表情图表
    updateChart(x, y) {
      //调用chart组件的updateChart函数
      this.$refs.chart.updateChart(x, y);
    },
    //更新持续工作时间
    updateWorkingTime(date) {
      //调用reminder组件的formatDate函数
      this.$refs.reminder.formatDate(date);
    },
    emotionRemind() {
      this.$refs.reminder.remind();
    },
    //获取天气
    getWeather() {
      var that = this;
      //调用后端接口
      that.$axios
        .get("/surroundings/outdoor_weather")
        .then((res) => {
          if (res) {
            res = res.data;
            if (res.code == 1) {
              console.log(res);
              that.weather = res.data["weather"];
              console.log(that.weather);
              //调用weather组件的updateData函数
              that.$refs.weather.updateData(that.weather);
            }
          }
          //获取到后端数据后,设置10秒的计时器，10秒后再次执行当前函数
          setTimeout(function () {
            that.getWeather();
          }, 10000);
        })
        .catch(function (error) {
          console.log("outdoor_temp遇到错误：\t" + error);
          setTimeout(function () {
            that.getFace();
          }, 5000);
        });
    },
    //获取温度湿度
    getTemperature() {
      var that = this;
      //调用后端接口
      that.$axios
        .get("/surroundings/indoor_weather")
        .then((res) => {
          if (res) {
            res = res.data;
            if (res.code == 1) {
              console.log(res);
              that.temperature = res.data.tmp;
              that.humidity = res.data.hmd;
              //分别调用humidity和temperature组件的updateData函数
              that.$refs.humidity.updateData(that.humidity);
              that.$refs.temperature.updateData(that.temperature);

              var time = new Date().toLocaleTimeString().replace(/^\D*/, "");
              //调用tempChart组件的updateChart函数
              that.$refs.tempChart.updateChart(
                time,
                that.temperature,
                that.humidity
              );
            }
          }
          //获取到后端数据后,设置5秒的计时器，5秒后再次执行当前函数
          setTimeout(function () {
            that.getTemperature();
          }, 5000);
        })
        .catch(function (error) {
          console.log("Indoor_temp遇到错误：\t" + error);
          setTimeout(function () {
            that.getFace();
          }, 5000);
        });
    },
    getQR() {
      var that = this;
      that.$axios
        .get("/surroundings/ip_qr", {
          responseType: "arraybuffer",
        })
        .then((res) => {
          if (res) {
            let u =
              "data:image/png;base64," +
              btoa(
                new Uint8Array(res.data).reduce(
                  (data, byte) => data + String.fromCharCode(byte),
                  ""
                )
              );
            console.log(u)
            that.pic = u;
          }
        })
        .catch(function (error) {
          console.log("qr_icon遇到错误：\t" + error);
          setTimeout(function () {
            that.getFace();
          }, 5000);
        });
    },
  },
  //页面加载完毕后立刻执行的函数
  mounted() {
    this.getTemperature();
    this.getWeather();
    this.getQR();
  },
};
</script>
