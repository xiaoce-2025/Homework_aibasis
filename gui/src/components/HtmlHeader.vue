<template>
  <header class="HtmlHeader">
    <!-- Logo 区域 -->
    <div class="logo">
      <img src="@/assets/logo.png" alt="网站Logo" class="logo-image">
      <span class="site-name">严小希的工作间</span>
    </div>

    <!-- 登陆后才显示此导航菜单 -->
    <!-- 导航菜单（桌面端） -->
    <div v-if="userStore.userInfo" @command="handleCommand" class="right-group">
      <nav class="nav-desktop">
        <ul class="nav-list">
          <li v-for="(item, index) in navItems" :key="index" class="nav-item">
            <router-link :to="item.path" class="nav-link" active-class="active-link" @click="handleNavClick(item)">
              {{ item.title }}
            </router-link>
          </li>
        </ul>
      </nav>
    </div>

    <!-- 用户操作区 -->
    <div class="user-area">
      <el-dropdown v-if="userStore.userInfo" @command="handleCommand">
        <span class="user-name">
          {{ userStore.userInfo.username }}
          <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">关于小希</el-dropdown-item>
            <el-dropdown-item command="settings">设置中心</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <div v-else class="user-log">
        <router-link to="/UserLogin" class="auth-button" custom v-slot="{ isActive, navigate }">
          <button :class="['auth-button', { active: isActive }]" @click="navigate">
            登录 / 注册
          </button>
        </router-link>
      </div>
    </div>

    <!-- 移动端菜单切换按钮 -->
    <button class="menu-toggle" @click="toggleMobileMenu" aria-label="切换导航菜单">
      <span class="hamburger"></span>
    </button>

    <!-- 移动端导航菜单 -->
    <Transition name="slide-down">
      <nav v-show="isMobileMenuOpen" class="nav-mobile">
        <ul class="nav-list-mobile">
          <li v-for="(item, index) in navItems" :key="index" class="nav-item-mobile">
            <router-link :to="item.path" class="nav-link-mobile" @click="toggleMobileMenu">
              {{ item.title }}
            </router-link>
          </li>
        </ul>
      </nav>
    </Transition>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../../stores/user'
import { ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 导航菜单配置
const navItems = ref([
  { title: '首页', path: '/', exact: true },
  { title: '续写', path: '/AIContinuation' },
  { title: '润色', path: '/AIPolishment' },
  { title: '功能中心', path: '/FunctionCenter' }
])

// 移动端菜单状态
const isMobileMenuOpen = ref(false)

// 切换移动端菜单
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// 处理导航点击
const handleNavClick = (item) => {
  router.push(item.path) // 使用router进行跳转
  isMobileMenuOpen.value = false // 移动端点击后关闭菜单
}


//检测是否在登录状态
const handleCommand = (command) => {
  switch (command) {
    case 'logout':
      userStore.logout()
      window.location.reload() // 刷新页面清除状态
      break
    case 'profile':
      router.push('/UserCenter')
      break
    case 'settings':
      router.push('/AllSettings')
      break
  }
}

</script>

<style scoped>
.HtmlHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.logo-image {
  height: 40px;
  width: auto;
}

.site-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.nav-desktop {
  display: none;
}

.right-group {
  display: flex;
  align-items: center;
  margin-left: auto;
  /* 关键属性：推至最右侧 */
  gap: 2rem;
  /* 导航与按钮间距 */
}

.nav-list {
  display: flex;
  gap: 2rem;
  list-style: none;
  margin-left: auto;
  /* 导航内部右对齐 */
  margin-right: 30px;
}

.nav-link {
  color: #34495e;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #3498db;
}

.user-log {
  display: none;
  gap: 1rem;

}

.auth-button {
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  border: 2px solid #3498db;
  background: transparent;
  color: #3498db;
  cursor: pointer;
  transition: all 0.3s;
}

.auth-button:hover {
  background: #3498db;
  color: white;
}

.register {
  background: #3498db;
  color: white;
}

.register:hover {
  opacity: 0.9;
}

.menu-toggle {
  display: block;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
}

.hamburger {
  display: block;
  width: 24px;
  height: 2px;
  background: #2c3e50;
  position: relative;
}

.hamburger::before,
.hamburger::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: inherit;
  transition: transform 0.3s;
}

.hamburger::before {
  transform: translateY(-6px);
}

.hamburger::after {
  transform: translateY(6px);
}

.nav-mobile {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-list-mobile {
  list-style: none;
  padding: 1rem;
}

.nav-item-mobile {
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.nav-link-mobile {
  color: #34495e;
  text-decoration: none;
  display: block;
}

/* 过渡动画 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (min-width: 768px) {
  .nav-desktop {
    display: block;
  }

  .user-log {
    display: flex;
  }

  .menu-toggle {
    display: none;
  }

  .nav-mobile {
    display: none;
  }
}
</style>