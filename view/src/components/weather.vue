<template>
  <div style="margin-left: 14px; margin-top: 14px; margin-bottom: 12px">
    <v-icon large left style="margin-left: 6px; margin-right: 5px">
      {{ weather_icon }}
    </v-icon>
    <span v-text="weather"></span>
  </div>
</template>

<script>
export default {
  name: "Weather",
  data: () => ({
    weather_icon: "fa-sun",
    weather_icon_set: {
      rainy: "fa-cloud-rain",
      sunny: "fa-sun",
      cloudy: "fa-cloud",
      snowy: "fa-snowflake",
      smogy: "fa-smog",
      thunder:"fa-bolt"
    },
    weather: "",
  }),
  mounted() {},
  methods: {
    updateData(dt) {
      this.weather = dt;
      this.weather_icon = this.weather_icon_set[this.weather];
    },
  },
};
</script>

<style>
</style>