<template>
  <AIToolsList />
</template>

<script>
import AIToolsList from '../components/FunctionList.vue'

export default {
  name: 'App',
  components: {
    AIToolsList,
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