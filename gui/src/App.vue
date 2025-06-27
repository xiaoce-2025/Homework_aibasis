<!-- 原 App.vue 中的 YanxxDialog 组件 -->
<template>
  <div>
    <HtmlHeader />
    <div v-if="userStore.userInfo" class="dialog-container">
      <router-view></router-view>
    </div>
    <div v-else>
      <AuthContainer />
    </div>
  </div>
</template>

<script>
import HtmlHeader from './components/HtmlHeader.vue';
import AuthContainer from './components/AuthContainer.vue';
import { useUserStore } from '../stores/user'

export default {
  name: 'App',
  components: {
    HtmlHeader,
    AuthContainer,
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
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
  height: 100%;
}

/* 新增对话框容器样式 */
.dialog-container {
  height: calc(100vh - 87px); /* 减去头部高度，具体数值根据实际头部高度调整 */
  width: 100%;
}
</style>