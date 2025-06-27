import { createRouter, createWebHashHistory } from 'vue-router'

// 路由级代码分割（懒加载）
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/UserMain.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/AIContinuation',
    name: 'AIContinuation',
    component: () => import('@/views/AIContinuation.vue'),
    meta: { title: 'AI续写' }
  },
  {
    path: '/AIPolishment',
    name: 'AIPolishment',
    component: () => import('@/views/AIPolishment.vue'),
    meta: { title: 'AI润色' }
  },
  {
    path: '/AllSettings',
    name: 'AllSettings',
    component: () => import('@/views/AllSettings.vue'),
    meta: { title: '设置' }
  },
  // 添加登录注册路由
  {
    path: '/UserLogin',
    name: 'UserLogin',
    component: () => import('@/views/UserLogin.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/FunctionCenter',
    name: 'FunctionCenter',
    component: () => import('@/views/FunctionCenter.vue'),
    meta: { title: '功能中心' }
  },
  {
    path: '/UserCenter',
    name: 'UserCenter',
    component: () => import('@/views/UserCenter.vue'),
    meta: { title: '用户中心' }
  },
  {
    path: '/AITextExtracts',
    name: 'AITextExtracts',
    component: () => import('@/views/AITextExtracts.vue'),
    meta: { title: '摘抄' }
  }
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

export default router