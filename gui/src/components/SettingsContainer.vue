<template>
    <div class="SettingsContainer">
      <!-- 头部标题 -->
      <h1 class="settings-title">全局设置</h1>
  
      <div class="setting-content">
        <div class="ai-basicsettings">
          <h1 class="settings-smallTitle">基础ai设置</h1>
          <el-form 
            ref="settingsForm"
            :model="settings"
            label-position="left"
            label-width="180px"
            class="settings-form"
          >
            <!-- 文本大模型配置 -->
            <el-card class="setting-section">
              <template #header>
                <div class="section-title">硅基流动平台信息</div>
              </template>
              
              <!-- 隐藏模型名称选项（直接删除该表单项） -->
              
              <el-form-item label="API 地址" prop="textModel.apiUrl">
                <el-input 
                  v-model="settings.textModel.apiUrl"
                  placeholder="https://api.text-model.com/v1"
                  disabled
                />
              </el-form-item>
  
              <el-form-item label="API 密钥" prop="textModel.apiKey">
                <el-input
                  v-model="settings.textModel.apiKey"
                  type="password"
                  show-password
                  placeholder="输入API密钥"
                />
              </el-form-item>
            </el-card>
            
            <!-- 删除图像大模型配置（整段删除） -->
            
          </el-form>
        </div>
        <div class="function-settings">
          <h1 class="settings-smallTitle">功能设置</h1>
          <el-form 
            ref="settingsForm"
            :model="settings"
            label-position="left"
            label-width="180px"
            class="settings-form"
          >
            <!-- 续写功能设置（无需修改） -->
            <el-card class="setting-section">
              <template #header>
                <div class="section-title">文本生成功能设置</div>
              </template>
  
              <el-form-item label="温度 (0-2)" prop="params.temperature">
                <el-slider
                  v-model="settings.textModel.params.temperature"
                  :min="0"
                  :max="2"
                  :step="0.1"
                  show-input
                />
              </el-form-item>
  
              <el-form-item label="最大Token数" prop="params.maxTokens">
                <el-input-number
                  v-model="settings.textModel.params.maxTokens"
                  :min="100"
                  :max="4000"
                  :step="100"
                />
              </el-form-item>
  
              <el-form-item label="每次续写数量 (1-5)" prop="params.generateNum">
                <el-input-number
                  v-model="settings.textModel.params.generateNum"
                  :min="1"
                  :max="5"
                />
              </el-form-item>

              <el-form-item label="单次续写字数" prop="params.generateTextNum">
                <el-input-number
                  v-model="settings.textModel.params.generateTextNum"
                  :min="1"
                  :max="500"
                />
              </el-form-item>
            </el-card>
          </el-form>
        </div>
      </div>
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button type="primary" @click="saveSettings">保存配置</el-button>
        <el-button @click="resetToDefault">恢复默认</el-button>
      </div>
  </div>
</template>
  
<script setup>
import { ElMessage } from 'element-plus'
import { useConfigStore } from '../../stores/config'
import { storeToRefs } from 'pinia'

const configStore = useConfigStore()
configStore.loadSettings()

// 直接绑定 Store 中的状态（保持响应式）
const { settings } = storeToRefs(configStore)

const saveSettings = () => {
  configStore.saveSettings();
  ElMessage.success('配置保存成功')
}

// ** 修改默认配置参数 **
const defaultSettings = {
  textModel: {
    name: "deepseek-ai/DeepSeek-V3",  // 设置默认模型名称
    apiUrl: 'https://api.siliconflow.cn/v1',  // 设置默认API地址
    apiKey: '',
    params: {
      temperature: 1.0,
      maxTokens: 150,
      generateNum: 3,
      generateTextNum: 100,
    },
  },
  // 移除 imageModel 配置
}

// 重置默认
const resetToDefault = () => {
  configStore.settings = JSON.parse(JSON.stringify(defaultSettings));
  ElMessage.info('已恢复默认配置')
}
</script>
  
  <style scoped>
  .SettingsContainer {
    max-width: 1400px;
    margin: 20px auto;
    padding: 0px;
  }
  
  .settings-title {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 0px;
  }

  .settings-smallTitle {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 24px;
  }
  
  .setting-section {
    margin-bottom: 20px;
  }

  .setting-content {
    display: flex;
    gap: 40px; 
  }

  .ai-basicsettings,
  .function-settings {
    flex: 1; /* 让两个区块均分宽度 */
    min-width: 0; /* 防止内容溢出 */
  }
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #34495e;
  }
  
  .action-buttons {
    margin-top: 30px;
    text-align: center;
  }
  
  :deep(.el-form-item__label) {
    font-weight: 500;
    color: #4a4a4a;
  }
  
  :deep(.el-card__header) {
    background-color: #f8f9fa;
  }
  </style>