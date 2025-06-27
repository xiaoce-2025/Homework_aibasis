// stores/user.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(null)
  
  // 初始化时从本地存储加载
  const loadFromStorage = () => {
    const stored = localStorage.getItem('userInfo')
    if (stored) userInfo.value = JSON.parse(stored)
  }

  // 登录成功处理
  const loginSuccess = (data) => {
    userInfo.value = data
    localStorage.setItem('userInfo', JSON.stringify(data))
  }

  // 退出登录
  const logout = () => {
    userInfo.value = null
    localStorage.removeItem('userInfo')
  }

  return { 
    userInfo,
    loadFromStorage,
    loginSuccess,
    logout
  }
})