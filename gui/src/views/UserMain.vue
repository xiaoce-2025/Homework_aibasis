<template>
  <YanxxDialog style="flex: 1;height:100%" />
</template>

<script>
import YanxxDialog from '../components/YanxxDialog.vue';

export default {
  name: 'App',
  components: {
    YanxxDialog
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
