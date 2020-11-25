<template>
  <div style="margin-left:14px;margin-top:14px">
    <v-icon large left style="margin-left: 6px; margin-right: 5px">
      {{ humid_icon }}
    </v-icon>
    <span style="font-size: 22px" v-text="humidity + '%'"></span>
  </div>
</template>

<script>
export default {
  name: "Humidity",
  data: () => ({
    humid_icon: "fa-tint",
    humidity: "0.0",
  }),
  mounted() {},
  methods: {
    updateData(dt) {
      this.humidity = dt;
    },
  },
};
</script>

<style>
</style>