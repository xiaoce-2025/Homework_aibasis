<template>
  <div class="TextPolishmentContainer">
    <!-- 加载遮罩层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loader"></div>
    </div>
    
    <!-- 标题区域 -->
    <div class="header-section">
      <h2 class="header-title">文章润色工具</h2>
      <p class="header-subtitle">优化您的写作，提升文章质量</p>
    </div>
    
    <!-- 输入与设置分栏区域 - 仅在润色前显示 -->
    <div v-if="!polishedText && showInputSection && showSettingsSection" class="input-settings-container">
      <!-- 左侧文本输入区域 -->
      <div class="source-section left-column">
        <h3>原文输入</h3>
        <textarea 
          v-model="originalText" 
          placeholder="在此粘贴需要润色的文章内容..."
          class="source-input"
          :disabled="isLoading"
        ></textarea>
      </div>
      
      <!-- 右侧配置编辑区域 -->
      <div class="settings-section right-column">
        <h3>润色设置</h3>
        <div class="settings-grid vertical-layout">
          <div class="setting-item">
            <label>润色强度</label>
            <select v-model="polishStrength" :disabled="isLoading">
              <option value="light">轻度优化</option>
              <option value="medium">中度改写</option>
              <option value="aggressive">全面改写</option>
            </select>
          </div>
          <div class="setting-item">
            <label>目标风格</label>
            <select v-model="writingStyle" :disabled="isLoading">
              <option value="formal">正式书面</option>
              <option value="academic">学术论文</option>
              <option value="creative">创意写作</option>
              <option value="business">商务沟通</option>
            </select>
          </div>
          <div class="setting-item">
            <label>目标语言</label>
            <select v-model="language" :disabled="isLoading">
              <option value="zh-CN">简体中文</option>
              <option value="zh-TW">繁体中文</option>
              <option value="en-US">英文</option>
              <option value="ja-JP">日文</option>
              <option value="wyw">文言文</option>
            </select>
          </div>
          <div class="setting-item">
            <label>额外要求</label>
            <!-- 改为textarea并增加rows属性 -->
            <textarea 
              v-model="additionalRequirements" 
              placeholder="如：更简洁、更专业等，可输入多行要求"
              class="additional-textarea"
              :disabled="isLoading"
              rows="4"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="action-buttons" v-if="showActionButtons">
      <button 
        @click="polishText" 
        class="polish-btn"
        :disabled="isLoading || !originalText.trim()"
      >
        <i class="icon-pen"></i> {{ isLoading ? '润色中...' : '开始润色' }}
      </button>
      <button 
        @click="resetForm" 
        class="reset-btn"
        :disabled="isLoading"
      >
        <i class="icon-reset"></i> 重置
      </button>
    </div>
    
    <!-- 润色结果 -->
    <div class="result-section" v-if="polishedText">
      <h3>润色结果</h3>
      <div class="result-container">
        <div class="result-text">{{ polishedText }}</div>
        <div class="result-actions">
          <button @click="cancelPolish" class="cancel-btn">
            <i class="icon-cancel"></i> 取消润色
          </button>
          <button @click="copyToClipboard" class="copy-btn">
            <i class="icon-copy"></i> 复制结果
          </button>
          <button @click="acceptChanges" class="accept-btn">
            <i class="icon-accept"></i> 接受修改
          </button>
        </div>
      </div>
    </div>
    
    <!-- 对比视图 -->
    <div class="comparison-section" v-if="showComparison">
      <h3>修改对比</h3>
      <div class="comparison-container">
        <div class="comparison-original">
          <h4>原文</h4>
          <div class="original-text">{{ originalText }}</div>
        </div>
        <div class="comparison-polished">
          <h4>润色后</h4>
          <div class="polished-text">{{ polishedText }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// JS代码与原版本一致，无需修改
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { useConfigStore } from '../../stores/config'

const configStore = useConfigStore()

// 从设置中获取api参数
const apiUrl = configStore.settings.textModel.apiUrl
const apiKey = configStore.settings.textModel.apiKey
const ModelName = configStore.settings.textModel.name
const ModelTemperature = configStore.settings.textModel.params.temperature

// 状态管理
const originalText = ref('');
const polishedText = ref('');
const isLoading = ref(false);
const polishStrength = ref('medium');
const writingStyle = ref('formal');
const language = ref('zh-CN');
const additionalRequirements = ref('');
const showComparison = ref(false);
const showInputSection = ref(true);
const showSettingsSection = ref(true);
const showActionButtons = ref(true);

// 计算属性
const hasText = computed(() => originalText.value.trim().length > 0);

// 润色文章
const polishText = async () => {
  if (!hasText.value) {
    ElMessage.warning('请先输入需要润色的文章内容');
    return;
  }
  
  try {
    isLoading.value = true;
    const response = await axios.post('http://localhost:5000/api/AIPolish', {
      config: {
        ModelName: ModelName,
        apiKey: apiKey,
        apiUrl: apiUrl,
        ModelTemperature: ModelTemperature,
      },
      content: originalText.value,
      polishStrength: polishStrength.value,
      writingStyle: writingStyle.value,
      additionalRequirements: additionalRequirements.value,
      language: language.value
    });
    console.log('提交结果:', response.data);
    polishedText.value = response.data.polishedText.trim();
    if (!response.data.polishedText.trim()) {
      throw new Error('服务器返回空内容');
    }
    
    showComparison.value = true;
    showInputSection.value = false;
    showSettingsSection.value = false;
    showActionButtons.value = false;
    
    ElMessage.success('文章润色完成！');
  } catch (error) {
    console.error('润色失败:', error);
    ElMessage.error('润色过程中发生错误');
  } finally {
    isLoading.value = false;
  }
};


// 重置表单
const resetForm = () => {
  originalText.value = '';
  polishedText.value = '';
  additionalRequirements.value = '';
  showComparison.value = false;
  showInputSection.value = true;
  showSettingsSection.value = true;
  showActionButtons.value = true;
};

// 复制到剪贴板
const copyToClipboard = () => {
  if (!polishedText.value) return;
  
  navigator.clipboard.writeText(polishedText.value)
    .then(() => {
      ElMessage.success('已复制到剪贴板');
    })
    .catch(err => {
      console.error('复制失败:', err);
      ElMessage.error('复制失败，请手动选择复制');
    });
};

// 接受修改
const acceptChanges = () => {
  if (polishedText.value) {
    originalText.value = polishedText.value;
    polishedText.value = '';
    showComparison.value = false;
    showInputSection.value = true;
    showSettingsSection.value = true;
    showActionButtons.value = true;
    ElMessage.success('已接受修改');
  }
};


// 取消润色
const cancelPolish = () => {
  if (polishedText.value) {
    polishedText.value = '';
    showComparison.value = false;
    showInputSection.value = true;
    showSettingsSection.value = true;
    showActionButtons.value = true;
    ElMessage.success('已取消润色');
  }
};
</script>

<style scoped>
.TextPolishmentContainer {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  min-height: 600px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 加载动画 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #8B0012;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 头部样式 */
.header-section {
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f2f5;
}

.header-title {
  color: #8B0012;
  margin: 0;
  font-size: 24px;
}

.header-subtitle {
  color: #7a7a7a;
  margin-top: 5px;
  font-size: 14px;
}

/* 输入与设置分栏容器 - 增大间距 */
.input-settings-container {
  display: flex;
  gap: 50px; /* 原30px改为50px进一步增大间距 */
  margin-bottom: 20px;
}

/* 左右分栏样式 */
.left-column, .right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 输入区域与设置区域公共样式 */
.source-section, .settings-section, .result-section, .comparison-section {
  flex: 1;
}

h3 {
  color: #8B0012;
  font-size: 18px;
  margin-bottom: 10px;
  padding-left: 5px;
}

.source-input {
  width: 100%;
  height: 100%;
  min-height: 300px;
  padding: 15px;
  border: 2px solid #8B0012;
  border-radius: 6px;
  font-size: 16px;
  resize: vertical;
  transition: border-color 0.3s;
}

.source-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

/* 设置区域 - 重点修改部分 */
.settings-grid {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  gap: 15px; /* 垂直间距 */
  flex: 1;
}

/* 取消网格布局，设置项宽度100% */
.setting-item {
  width: 100%;
}

.setting-item label {
  margin-bottom: 6px;
  color: #5a5a5a;
  font-size: 14px;
}

.setting-item select, .additional-textarea {
  width: 100%; /* 填满父容器 */
  padding: 12px; /* 内边距 */
  border: 1px solid #dcdde1;
  border-radius: 6px; /* 圆角 */
  font-size: 14px;
  background-color: #fff;
  box-sizing: border-box;
}

.setting-item select:focus, .additional-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

/* 额外要求文本域样式 */
.additional-textarea {
  min-height: 100px; /* 固定最小高度 */
  resize: vertical; /* 允许垂直调整大小 */
  line-height: 1.5;
}

/* 响应式设计 - 增大垂直间距 */
@media (max-width: 768px) {
  .input-settings-container {
    flex-direction: column;
    gap: 30px; /* 小屏幕下垂直排列时间距增大到30px */
  }
  
  .left-column, .right-column {
    flex: none;
  }
  
  .source-input {
    min-height: 200px;
  }
}

/* 按钮区域 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin: 25px 0;
}

.polish-btn, .reset-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 25px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.polish-btn {
  background-color: #8B0012;
  color: white;
}

.polish-btn:hover {
  background-color: #a0001a;
  transform: translateY(-2px);
}

.polish-btn:disabled {
  background-color: #c4a6aa;
  cursor: not-allowed;
  transform: none;
}

.reset-btn {
  background-color: #f0f2f5;
  color: #5a5a5a;
  border: 1px solid #dcdde1;
}

.reset-btn:hover {
  background-color: #e4e6e9;
}

.reset-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 结果区域 */
.result-container {
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 15px;
  background-color: #f9fafc;
  position: relative;
}

.result-text {
  white-space: pre-wrap;
  line-height: 1.6;
  min-height: 100px;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #eaeaea;
}

.result-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.copy-btn, .accept-btn, .cancel-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 15px;
  font-size: 14px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.copy-btn {
  background-color: #3498db;
  color: white;
}

.copy-btn:hover {
  background-color: #2980b9;
}

.accept-btn {
  background-color: #27ae60;
  color: white;
}

.accept-btn:hover {
  background-color: #219653;
}

.cancel-btn {
  background-color: #ffa400;
  color: white;
}

.cancel-btn:hover {
  background-color: #fa8c35;
}

/* 对比区域 */
.comparison-container {
  display: flex;
  gap: 20px;
}

.comparison-original, .comparison-polished {
  flex: 1;
  padding: 15px;
  border-radius: 6px;
  background-color: #f9fafc;
  border: 1px solid #e1e4e8;
}

.comparison-original h4, .comparison-polished h4 {
  color: #8B0012;
  margin-top: 0;
  margin-bottom: 10px;
}

.original-text, .polished-text {
  padding: 10px;
  background-color: #fff;
  border: 1px solid #eaeaea;
  border-radius: 4px;
  min-height: 150px;
  white-space: pre-wrap;
  line-height: 1.6;
}

/* 图标样式 */
.icon-pen:before { content: "✏️"; }
.icon-reset:before { content: "🔄"; }
.icon-copy:before { content: "📋"; }
.icon-accept:before { content: "✅"; }
.icon-cancel:before { content: "❌"; }
</style>