<template>
  <AuthContainer />
</template>

<script>
import AuthContainer from '../components/AuthContainer.vue';

export default {
  name: 'App',
  components: {
    AuthContainer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
