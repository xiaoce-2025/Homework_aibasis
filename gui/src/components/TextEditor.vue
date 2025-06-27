<template>
  <div class="MessageContainer">
    <!-- 加载遮罩层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loader"></div>
    </div>
    <!-- 左侧输入区域 -->
    <div class="left-panel">
      <div class="title-section">
        <textarea v-model="title" placeholder="在此输入标题..." class="title-input" :disabled="isLoading"></textarea>
      </div>
      <div class="input-section">
        <textarea v-model="content" placeholder="在此输入内容..." class="text-input"
          :disabled="isLoading || isChoosing"></textarea>
      </div>
    </div>

    <!-- 右侧候选下文 -->
    <div class="right-panel">
      <h3 v-show="!isChoosing">写作要求</h3>
      <div class="content-request-section" v-show="!isChoosing">
        <textarea v-model="ContentRequest" placeholder="在此输入你的写作要求，如作文题目、背景设定等..." class="content-request-input"
          :disabled="isLoading"></textarea>
      </div>
      
      <!-- 风格/情感标签选择 -->
      <div class="style-section" v-show="!isChoosing">
        <h4>风格/情感标签</h4>
        <div class="style-tags">
          <label v-for="tag in styleTags" :key="tag.value" class="style-tag">
            <input type="checkbox" v-model="selectedStyles" :value="tag.value" :disabled="isLoading">
            <span>{{ tag.label }}</span>
          </label>
        </div>
      </div>

      <!-- 文章构思输入 -->
      <div class="plot-section" v-show="!isChoosing">
        <h4>文章构思</h4>
        <textarea v-model="plotOutline" placeholder="在此输入你对文章情节发展的构思，如：主角接下来会遇到什么挑战？故事会如何发展？..." class="plot-input"
          :disabled="isLoading"></textarea>
      </div>

      <h3 v-show="isChoosing">候选下文</h3>
      <div v-for="suggestion in suggestions" :key="suggestion.id" class="suggestion-item"
        @click="insertSuggestion(suggestion.text)">
        {{ suggestion.text }}
      </div>
      <div class="confirm-cancel" v-show="isChoosing">
        <button @click="ChooseCancel" class="CancelButton" v-show="isChoosing">
          取消
        </button>
        <button @click="ChooseConfirm" class="ConfirmButton" v-show="isChoosing">
          确认
        </button>
      </div>
      <button @click="handleSubmit" class="submit-btn" :disabled="isLoading">
        {{ isChoosing ? '让小希重写一份' : '让小希来帮你写吧~' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useConfigStore } from '../../stores/config'

const configStore = useConfigStore()

// 从设置中获取api参数
const apiUrl = configStore.settings.textModel.apiUrl
const apiKey = configStore.settings.textModel.apiKey
const maxToken = configStore.settings.textModel.params.maxTokens
const ModelName = configStore.settings.textModel.name
const ModelTemperature = configStore.settings.textModel.params.temperature
const generateNum = configStore.settings.textModel.params.generateNum
const generateTextNum = configStore.settings.textModel.params.generateTextNum


// 输入文本内容
const title = ref('');
const content = ref('');
const ContentRequest = ref('');
const plotOutline = ref(''); // 文章构思

// 风格/情感标签
const styleTags = ref([
  { value: 'romantic', label: '浪漫' },
  { value: 'mysterious', label: '神秘' },
  { value: 'humorous', label: '幽默' },
  { value: 'melancholy', label: '忧郁' },
  { value: 'exciting', label: '激动' },
  { value: 'peaceful', label: '平静' },
  { value: 'nostalgic', label: '怀旧' },
  { value: 'optimistic', label: '乐观' },
  { value: 'pessimistic', label: '悲观' },
  { value: 'dramatic', label: '戏剧性' },
  { value: 'realistic', label: '现实' },
  { value: 'fantasy', label: '奇幻' },
  { value: 'suspense', label: '悬疑' },
  { value: 'warm', label: '温暖' },
  { value: 'cold', label: '冷酷' }
]);

const selectedStyles = ref([]); // 选中的风格标签

// 选择文本状态 
const content_BeforeChoosing = ref('');
const isChoosing = ref(false);
// 等待状态
const isLoading = ref(false);
// 候选下文列表
const suggestions = ref([]);

// 候选下文请求列表
const fetchSuggestions = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('http://localhost:5000/api/ConnectTest');
    ElMessage({
      message: response.data,
      type: 'success',
      duration: 1000
    })
  } catch (error) {
    console.error('服务端检测：', error);
    ElMessage({
      message: '服务端检测：连接异常',
      type: 'error',
      duration: 3000
    })
  } finally {
    isLoading.value = false;
  }
};

// 插入建议文本
const insertSuggestion = (text) => {
  content.value = content_BeforeChoosing.value + text;
};

//确认按钮
const ChooseConfirm = () => {
  isChoosing.value = false;
  content_BeforeChoosing.value = content.value;
  suggestions.value = [];
}

//取消按钮
const ChooseCancel = () => {
  isChoosing.value = false;
  content.value = content_BeforeChoosing.value;
  suggestions.value = [];
}

// 提交内容
const handleSubmit = async () => {
  if (ModelName && apiUrl && ModelName) {
    try {
      isLoading.value = true;
      const response = await axios.post('http://localhost:5000/api/submit', {
        config: {
          ModelName: ModelName,
          apiKey: apiKey,
          apiUrl: apiUrl,
          maxToken: maxToken,
          ModelTemperature: ModelTemperature,
          generateNum: generateNum,
          generateTextNum: generateTextNum,
        },
        title: title.value,
        content: content.value,
        ContentRequest: ContentRequest.value,
        selectedStyles: selectedStyles.value, // 添加选中的风格标签
        plotOutline: plotOutline.value // 添加文章构思
      });
      console.log('提交结果:', response.data);
      // 如果需要更新候选建议
      if (response.data.new_suggestions) {
        //添加候选状态
        suggestions.value = response.data.new_suggestions;
        // 进入选择状态
        if (!(suggestions.value.length === 0)) {
          isChoosing.value = true;
          content_BeforeChoosing.value = content.value;
        }
        else {
          ElMessage({
            message: '获取候选列表失败：api调用异常',
            type: 'error',
            duration: 3000
          })
        }
      }
    } catch (error) {
      console.error('提交失败:', error);
      ElMessage({
        message: error,
        type: 'error',
        duration: 3000
      })
    } finally {
      isLoading.value = false;
    }
  }
  else {
    ElMessage({
      message: '请填写完整文本大模型api信息！',
      type: 'error',
      duration: 3000
    })
  }
};

onMounted(() => {
  fetchSuggestions();
});

</script>

<style scoped>
/* 总样式 */
.MessageContainer {
  position: relative;
  display: flex;
  padding: 20px;
  gap: 20px;
  min-height: 740px;
}

/* 加载器样式 */
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
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* 左侧样式 */
.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  /* 垂直排列 */
  gap: 15px;
  /* 元素间距 */
}

/* 标题样式 */
.title-section {
  height: 42px;
}

.title-input {
  width: 95%;
  height: 48%;
  padding: 15px;
  border: 2px solid #8B0012;
  border-radius: 6px;
  font-size: 18px;
  resize: none;
}

/* 输入样式 */
.input-section {
  flex: 1;
}

.text-input {
  width: 95%;
  height: 95%;
  padding: 15px;
  border: 2px solid #8B0012;
  border-radius: 6px;
  font-size: 16px;
  resize: none;
}

/* 右侧总样式 */
.right-panel {
  width: 350px;
  padding: 15px;
  background-color: #f5f6fa;
  border-radius: 8px;
  text-align: center;
  max-height: 740px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 10px;
  margin: 8px 0;
  background-color: white;
  border: 1px solid #dcdde1;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.suggestion-item:hover {
  background-color: #3498db;
  color: white;
  transform: translateX(5px);
}

h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

h4 {
  margin: 10px 0 8px 0;
  color: #34495e;
  font-size: 14px;
  text-align: left;
}

/* 风格标签样式 */
.style-section {
  margin: 15px 0;
  text-align: left;
}

.style-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.style-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.style-tag:hover {
  background-color: #e3f2fd;
  border-color: #2196f3;
}

.style-tag input[type="checkbox"] {
  margin: 0;
  cursor: pointer;
}

.style-tag input[type="checkbox"]:checked + span {
  color: #2196f3;
  font-weight: bold;
}

/* 文章构思样式 */
.plot-section {
  margin: 15px 0;
  text-align: left;
}

.plot-input {
  width: 100%;
  height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  resize: none;
  box-sizing: border-box;
}

/* 续写提交按钮样式 */
.submit-btn {
  width: 100%;
  background: royalblue;
  flex: 1;
  /* 等分剩余空间 */
  font-family: inherit;
  font-size: 20px;
  color: white;
  padding: 0.7em 1em;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  min-width: 80px;
  /* 设置合理的最小宽度 */
  text-align: center;
  /* 文字居中 */
  margin-top: 15px;
}

/* 禁用状态样式 */
textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 选择确认/取消按钮样式 */
.confirm-cancel {
  width: 100%;
  /* 占据整行宽度 */
  height: 65px;
  display: flex;
  justify-content: space-between;
  /* 左右两端对齐 */
  gap: 15px;
}

/* 统一按钮样式 */
.ConfirmButton,
.CancelButton {
  height: 80%;
  flex: 1;
  /* 等分剩余空间 */
  font-family: inherit;
  font-size: 20px;
  color: white;
  padding: 0.7em 1em;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  min-width: 80px;
  /* 设置合理的最小宽度 */
  text-align: center;
  /* 文字居中 */
}

.ConfirmButton {
  background: rgb(85, 239, 85);
}

.CancelButton {
  background: rgb(211, 49, 49);
}

/* 写作要求输入样式 */
.content-request-section {
  margin-bottom: 15px;
}

.content-request-input {
  width: 100%;
  height: 120px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  resize: none;
  box-sizing: border-box;
}
</style>