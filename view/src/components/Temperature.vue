<template>
  <div style="margin-left:14px;margin-top:14px">
    <v-icon large left style="margin-left: 6px; margin-right: 5px">
      {{ temp_icon }}
    </v-icon>
    <span style="font-size: 22px" v-text="temperature + '℃'"></span>
  </div>
</template>

<script>
export default {
  name: "Temperature",
  data: () => ({
    temp_iconSets: [
      "fa-thermometer-empty",
      "fa-thermometer-quarter",
      "fa-thermometer-half",
      "fa-thermometer-three-quarters",
    ],
    temp_icon: "fa-thermometer-empty",
    temperature: "0.0",
  }),
  methods: {
    updateData(dt) {
      this.temperature = dt;
    },
  },
};
</script>

<style>
</style>