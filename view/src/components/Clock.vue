  
<template>
  <div class="clock"></div>
</template>
<script>
export default {
  name: "Clock",
  data: () => ({}),
  mounted: () => {
    var clk = document.getElementsByClassName("clock");
    clk.FlipClock({
      clockFace: "TwelveHourClock",
    });
  },
};
</script>
