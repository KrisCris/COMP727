<template>
  <div>
    <v-card elevation="3" outlined>
      <template slot="progress">
        <v-progress-linear
          color="blue"
          height="10"
          indeterminate
        ></v-progress-linear>
      </template>
      <v-card-title>Emotion</v-card-title>
      <v-divider class="mx-2"></v-divider>
      <v-card-text>
        <span v-text="emotion" style="margin-right: 15px"></span>
        <v-icon :color="color" x-large right>{{ icon }}</v-icon>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "EmotionDetector",
  data: () => ({
    emotion: "Detecting",
    icon: "fa-circle-notch fa-spin",
    color: "blue",
    shouldRest: false,
    loading: true,
  }),
  methods: {
    getFace() {
      var that = this;
      that.loading = true;
      that.$axios
        .get("/emotions/getEmotion")
        .then((res) => {
          res = res.data;
          if (res.code == "1") {
            var emotionCode = -1;
            that.shouldRest = res.data.shouldRest;
            if (res.data.emotion == "happy") {
              that.icon = "fa-laugh-beam";
              that.color = "green";
              emotionCode = 5;
              that.emotion = res.data.emotion;
            } else if (res.data.emotion == "neutral") {
              that.icon = "fa-meh";
              that.color = "blue";
              emotionCode = 3;
              that.emotion = res.data.emotion;
            } else if (res.data.emotion == "angry") {
              that.icon = "fa-angry";
              that.color = "red";
              emotionCode = 0;
              that.emotion = res.data.emotion;
            } else if (res.data.emotion == "sad") {
              that.icon = "fa-tired";
              that.color = "red";
              emotionCode = 2;
              that.emotion = res.data.emotion;
            } else if (res.data.emotion == "surprise") {
              that.icon = "fa-surprise";
              that.color = "yellow";
              emotionCode = 4;
              that.emotion = res.data.emotion;
            } else if (res.data.emotion == "fear") {
              that.icon = "fa-frown";
              that.color = "red";
              emotionCode = 1;
              that.emotion = res.data.emotion;
            } else {
              console.log(res);
              console.log("unexcepted emotion:\t" + res.data.emotion);
            }
            if (emotionCode >= 0 && emotionCode <= 5) {
              that.loading = false;
              var time = new Date().toLocaleTimeString().replace(/^\D*/, "");
              //发起updateChart事件，同时将time和emotionCode变量同时发送至外部
              that.$emit("updateChart", time, emotionCode);
            }
            if (that.shouldRest) {
              that.$emit("shouldRest");
            }
            //发起workingTime事件，同时将res.data.begin_time发送至外部
            that.$emit("workingTime", res.data.begin_time);
          } else if (res.code == "2") {
            //发起workingTime事件，同时将0发送至外部
            that.$emit("workingTime", 0);
          }
          //10秒后再次检测表情
          setTimeout(function () {
            that.getFace();
          }, 8000);
        })
        .catch(function (error) {
          console.log("遇到错误：\t" + error);
          setTimeout(function () {
            that.getFace();
          }, 5000);
        });
    },
  },
  mounted() {
    this.getFace();
  },
};
</script>

<style>
</style>