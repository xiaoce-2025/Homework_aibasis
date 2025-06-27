<template>
  <div class="TextExtractContainer">
    <h1>自动化摘抄</h1>
    <!-- 加载遮罩层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loader"></div>
    </div>
    <div class="input-section">
      <textarea v-model="inputText" placeholder="粘贴或输入您的摘抄内容..." class="text-input"></textarea>
      <div class="button-section">
        <button @click="PictureOCR" class="picture-ocr-btn" title="从图片中提取文字">📷 图片OCR</button>
        <button @click="processText" class="process-btn" title="开始处理文本摘抄">🚀 摘抄，启动！</button>
        <button v-if="excerpts.length" @click="TextExport" class="export-btn" title="导出摘抄内容到文件">📤 导出摘抄内容 ({{ excerpts.length }}条)</button>
        <button v-if="excerpts.length" @click="clearContent" class="clear-btn" title="清空所有摘抄内容">
          🗑️ 清空内容
        </button>
      </div>
    </div>
    <br>
    <TextOCR v-if="StartOCR" @confirm="handleOcrConfirm" @cancel="handleOcrCancel"/>

    <div v-if="excerpts.length" class="excerpts-list">
      <div v-for="(excerpt, index) in excerpts" :key="index" class="excerpt-item">
        <div class="sentence-box">
          <span class="sentence-num">#{{ index + 1 }}</span>
          <p class="sentence-text">{{ excerpt.sentence }}</p>
        </div>
        <textarea v-model="excerpt.comment" placeholder="输入您的点评..." class="comment-input"
          @input="saveToLocalStorage"></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useConfigStore } from '../../stores/config'
import TextOCR from './TextOCR.vue';

const configStore = useConfigStore()
// 等待状态
const isLoading = ref(false);
// 开始OCR
const StartOCR = ref(false);

// 从设置中获取api参数
const apiUrl = configStore.settings.textModel.apiUrl
const apiKey = configStore.settings.textModel.apiKey
const maxToken = configStore.settings.textModel.params.maxTokens
const ModelName = configStore.settings.textModel.name
const ModelTemperature = configStore.settings.textModel.params.temperature

// 响应式数据
const inputText = ref('')
const excerpts = reactive([])

// 文本处理方法
const processText = async () => {
  if (inputText.value) {
    // 清空旧数据
    excerpts.splice(0, excerpts.length)
    // 调用大模型处理摘抄
    if (ModelName && apiUrl && ModelName) {
      try {
        isLoading.value = true;
        const response = await axios.post('http://localhost:5000/api/AITextExtracts', {
          config: {
            ModelName: ModelName,
            apiKey: apiKey,
            apiUrl: apiUrl,
            maxToken: maxToken,
            ModelTemperature: ModelTemperature,
          },
          text: inputText.value,
        });
        console.log('提交结果:', response.data);
        // 若返回了摘抄内容
        if (response.data.new_suggestions) {
          //增加摘抄内容
          excerpts.splice(0, excerpts.length, ...response.data.new_suggestions);
        }
      } catch (error) {
        console.error('提交失败:', error);
        ElMessage.error(error)
      } finally {
        isLoading.value = false;
      }
    }
    else {
      ElMessage.error('请填写完整文本大模型api信息！')
    }
    saveToLocalStorage()
  }
  else {
    ElMessage.error('请输入需要摘抄的文本！')
  }
}


// 图片OCR
const PictureOCR = async () => {
  StartOCR.value = true;
}
// 图片OCR结果返回
const handleOcrConfirm = (text) => {
  inputText.value += text;
  StartOCR.value = false;
}
const handleOcrCancel = () => {
  StartOCR.value = false;
}


// 导出摘抄
const TextExport = async () => {
  if (excerpts.length === 0) {
    ElMessage.warning('没有摘抄内容可导出！')
    return
  }

  try {
    const { value: exportFormat } = await ElMessageBox.prompt(
      '请选择导出格式：\n1. TXT文本文件\n2. Markdown文件\n3. Word文档（HTML格式）',
      '选择导出格式',
      {
        confirmButtonText: '导出',
        cancelButtonText: '取消',
        inputPattern: /^[1-3]$/,
        inputErrorMessage: '请输入1-3之间的数字',
        inputValue: '1',
        inputPlaceholder: '请输入1-3'
      }
    )

    // 显示导出进度
    const loadingMessage = ElMessage({
      message: '正在生成导出文件...',
      type: 'info',
      duration: 0
    })

    try {
      switch (exportFormat) {
        case '1':
          await exportAsTxt()
          break
        case '2':
          await exportAsMarkdown()
          break
        case '3':
          await exportAsWord()
          break
        default:
          ElMessage.error('无效的导出格式')
      }
    } finally {
      loadingMessage.close()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('导出失败:', error)
      ElMessage.error('导出失败：' + (error.message || '未知错误'))
    }
  }
}

// 导出为TXT格式
const exportAsTxt = async () => {
  try {
    const content = generateTxtContent()
    await downloadFile(content, `摘抄内容_${getTimestamp()}.txt`, 'text/plain;charset=utf-8')
    ElMessage.success('TXT文件导出成功！')
  } catch (error) {
    throw new Error('TXT文件导出失败：' + error.message)
  }
}

// 导出为Markdown格式
const exportAsMarkdown = async () => {
  try {
    const content = generateMarkdownContent()
    await downloadFile(content, `摘抄内容_${getTimestamp()}.md`, 'text/markdown;charset=utf-8')
    ElMessage.success('Markdown文件导出成功！')
  } catch (error) {
    throw new Error('Markdown文件导出失败：' + error.message)
  }
}

// 导出为Word格式
const exportAsWord = async () => {
  try {
    const content = generateWordContent()
    await downloadFile(content, `摘抄内容_${getTimestamp()}.html`, 'text/html;charset=utf-8')
    ElMessage.success('Word文档导出成功！')
  } catch (error) {
    throw new Error('Word文档导出失败：' + error.message)
  }
}

// 获取时间戳
const getTimestamp = () => {
  const now = new Date()
  return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`
}

// 生成TXT内容
const generateTxtContent = () => {
  const timestamp = new Date().toLocaleString('zh-CN')
  const totalExcerpts = excerpts.length
  const totalComments = excerpts.filter(excerpt => excerpt.comment && excerpt.comment.trim()).length
  
  let content = `摘抄内容\n`
  content += `导出时间：${timestamp}\n`
  content += `总计：${totalExcerpts}条摘抄\n`
  content += `有点评：${totalComments}条\n`
  content += `${'='.repeat(50)}\n\n`

  excerpts.forEach((excerpt, index) => {
    content += `${index + 1}. ${excerpt.sentence}\n`
    if (excerpt.comment && excerpt.comment.trim()) {
      content += `   点评：${excerpt.comment}\n`
    }
    content += '\n'
  })

  return content
}

// 生成Markdown内容
const generateMarkdownContent = () => {
  const timestamp = new Date().toLocaleString('zh-CN')
  const totalExcerpts = excerpts.length
  const totalComments = excerpts.filter(excerpt => excerpt.comment && excerpt.comment.trim()).length
  
  let content = `# 摘抄内容\n\n`
  content += `**导出时间：** ${timestamp}\n\n`
  content += `**统计信息：**\n`
  content += `- 总计：${totalExcerpts}条摘抄\n`
  content += `- 有点评：${totalComments}条\n`
  content += `- 无点评：${totalExcerpts - totalComments}条\n\n`
  content += `---\n\n`

  excerpts.forEach((excerpt, index) => {
    content += `## ${index + 1}. ${excerpt.sentence}\n\n`
    if (excerpt.comment && excerpt.comment.trim()) {
      content += `**点评：** ${excerpt.comment}\n\n`
    }
    content += `---\n\n`
  })

  return content
}

// 生成Word内容（HTML格式，可转换为Word）
const generateWordContent = () => {
  const timestamp = new Date().toLocaleString('zh-CN')
  const totalExcerpts = excerpts.length
  const totalComments = excerpts.filter(excerpt => excerpt.comment && excerpt.comment.trim()).length
  
  let content = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>摘抄内容</title>
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #333; border-bottom: 2px solid #2196F3; padding-bottom: 10px; }
        h2 { color: #2196F3; margin-top: 30px; }
        .excerpt { margin: 20px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #2196F3; }
        .comment { margin-top: 10px; padding: 10px; background: #e3f2fd; border-radius: 4px; }
        .timestamp { color: #666; font-size: 14px; }
        .stats { background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 20px 0; }
        .stats ul { margin: 5px 0; padding-left: 20px; }
    </style>
</head>
<body>
    <h1>摘抄内容</h1>
    <p class="timestamp">导出时间：${timestamp}</p>
    
    <div class="stats">
        <h3>统计信息</h3>
        <ul>
            <li>总计：${totalExcerpts}条摘抄</li>
            <li>有点评：${totalComments}条</li>
            <li>无点评：${totalExcerpts - totalComments}条</li>
        </ul>
    </div>
    
    <hr>
`

  excerpts.forEach((excerpt, index) => {
    content += `
    <div class="excerpt">
        <h2>${index + 1}. ${excerpt.sentence}</h2>
`
    if (excerpt.comment && excerpt.comment.trim()) {
      content += `
        <div class="comment">
            <strong>点评：</strong>${excerpt.comment}
        </div>
`
    }
    content += `    </div>`
  })

  content += `
</body>
</html>`

  return content
}

// 下载文件
const downloadFile = (content, filename, mimeType) => {
  return new Promise((resolve, reject) => {
    try {
      const blob = new Blob([content], { type: mimeType })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      link.style.display = 'none'
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      // 延迟释放URL对象
      setTimeout(() => {
        URL.revokeObjectURL(url)
      }, 100)
      
      resolve()
    } catch (error) {
      reject(new Error('文件下载失败：' + error.message))
    }
  })
}

// 本地存储功能
const saveToLocalStorage = () => {
  localStorage.setItem('excerptsData', JSON.stringify(excerpts))
}

// 初始化时加载本地数据
onMounted(() => {
  const savedData = localStorage.getItem('excerptsData')
  if (savedData) {
    const parsedData = JSON.parse(savedData)
    excerpts.push(...parsedData)
  }
})

// 清空内容
const clearContent = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有摘抄内容吗？此操作不可恢复！',
      '确认清空',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    // 用户确认后执行清空操作
    inputText.value = ''
    excerpts.splice(0, excerpts.length)
    saveToLocalStorage()
    ElMessage.success('内容已清空！')
  } catch (error) {
    // 用户取消操作，不做任何处理
    if (error !== 'cancel') {
      ElMessage.error('清空操作失败：' + error.message)
    }
  }
}
</script>

<style>
.TextExtractContainer {
  max-width: 800px;
  margin: 2rem auto;
  padding: 20px;
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

.text-input {
  width: 100%;
  height: 150px;
  padding: 15px;
  margin: 10px 0;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  resize: vertical;
}

.button-section {
  gap: 10px;
  display: flex;
  justify-content: center;
}

.process-btn {
  background: #4CAF50;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.process-btn:hover {
  background: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}

.process-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
}

.picture-ocr-btn {
  background: #e54110;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.picture-ocr-btn:hover {
  background: #d43707;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(229, 65, 16, 0.3);
}

.picture-ocr-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(229, 65, 16, 0.3);
}

.export-btn {
  background: #3844ef;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.export-btn:hover {
  background: #0614db;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(56, 68, 239, 0.3);
}

.export-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(56, 68, 239, 0.3);
}

.clear-btn {
  background: #f44336;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.clear-btn:hover {
  background: #d32f2f;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3);
}

.clear-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(244, 67, 54, 0.3);
}

.excerpts-list {
  margin-top: 30px;
}

.excerpt-item {
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sentence-box {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.sentence-num {
  background: #2196F3;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  margin-right: 10px;
}

.comment-input {
  align-items: center;
  width: 95%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  min-height: 80px;
  resize: vertical;
}
</style>