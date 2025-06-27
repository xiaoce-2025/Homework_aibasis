<template>
    <MessageContainer />
  </template>
  
  <script>
  import MessageContainer from '../components/TextEditor.vue';
  
  export default {
    name: 'AIContinuation',
    components: {
      MessageContainer,
    }
  }
  </script>
  
  <style>
  #AIContinuation {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 0px;
  }
  </style>
  