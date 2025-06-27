<template>
  <div class="AuthContainer" v-if="isLogin">
    <el-card class="auth-card">
      <h1 class="auth-title">登录</h1>

      <el-form v-if="isLogin" ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名/邮箱" prefix-icon="User" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>

        <div class="auth-options">
          <!--el-checkbox v-model="rememberMe">记住用户名（未实现）</el-checkbox-->
          <el-link type="primary" @click="isLogin = false">没有账号？去注册</el-link>
        </div>

        <el-button type="primary" native-type="submit" class="auth-button">
          立即登录
        </el-button>
      </el-form>
    </el-card>
  </div>

  <!-- 注册页面 -->
  <div class="AuthContainer" v-else>
    <el-card class="auth-card">
      <h1 class="auth-title">注册</h1>

      <el-form :v-else="!isLogin" ref="registerFormRef" :model="registerForm" :rules="registerRules"
        @submit.prevent="handleRegister">

        <el-form-item prop="username">
          <el-input v-model="registerForm.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" prefix-icon="Lock"
            show-password />
        </el-form-item>

        <div class="auth-options">
          <el-link type="primary" @click="isLogin = true">已有账号？立即登录</el-link>
        </div>

        <el-button type="primary" native-type="submit" class="auth-button">
          立即注册
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios';
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const router = useRouter()

// 登录/注册切换
const isLogin = ref(true)

// 添加表单引用
const loginFormRef = ref(null)
const registerFormRef = ref(null)

// 监视登录状态变化
watch(isLogin, (newVal) => {
  nextTick(() => {
    if (newVal) {
      loginFormRef.value?.clearValidate()
    } else {
      registerFormRef.value?.clearValidate()
    }
  })
})

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

// 自定义验证函数
const validatePassword = (rule, value, callback) => {
  if (value.length < 6) {
    callback(new Error('密码不能少于6位'))
  } else {
    callback()
  }
}

const validateConfirm = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 登录验证规则
const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 1, max: 100, message: '长度在3到16个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ]
})

// 注册验证规则
const registerRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在3到16个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' }
  ]
})


// 登录处理函数
const handleLogin = async () => {
  const connected = ref(false)
  try {
    // 先进行表单验证
    await loginFormRef.value.validate();
    // 登录处理函数
    connected.value = true
    const response = await axios.post('http://localhost:5000/api/UserLogin', loginForm)
    if (response.data == 'True') {
      // 更新用户状态
      userStore.loginSuccess({
        username: loginForm.username,
        token: loginForm.token
      })
      ElMessage.success('登录成功')
      // 跳转逻辑
      router.push('/')
    }
    else {
      ElMessage.error('登陆失败：用户名或密码错误')
    }
  } catch (error) {
    if (error.response) {
      ElMessage.error(error)
    }
    else if (connected.value == true) {
      ElMessage.error("登录失败")
    }
  }
}

// 注册处理函数
const handleRegister = async () => {
  const connected = ref(false)
  try {
    // 先进行表单验证
    await registerFormRef.value.validate();
    // 登录处理函数
    connected.value = true
    const response = await axios.post('http://localhost:5000/api/UserSignUp', registerForm)
    if (response.data == 'True') {
      //注册成功跳转
      ElMessage.success('注册成功，请登录')
      isLogin.value = true
    }
    else {
      ElMessage.error('注册失败：用户名已被注册')
    }
  } catch (error) {
    if (error.response) {
      ElMessage.error(error)
    }
    else if (connected.value == true) {
      ElMessage.error("登录失败")
    }
  }
}
</script>

<style scoped>
.AuthContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f7fa;
}

.auth-card {
  width: 400px;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.auth-title {
  text-align: center;
  color: #303133;
  margin-bottom: 30px;
}

.auth-options {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.auth-button {
  width: 100%;
  height: 40px;
  margin-top: 10px;
}

.third-party-auth {
  margin-top: 30px;
}

.divider {
  color: #909399;
  font-size: 12px;
  text-align: center;
  position: relative;
  margin: 20px 0;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid #dcdfe6;
  position: absolute;
  top: 50%;
  width: 40%;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 15px;
}

.icon-wechat {
  color: #67C23A;
}

.icon-github {
  color: #303133;
}
</style>