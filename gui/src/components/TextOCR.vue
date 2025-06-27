<!-- components/OcrUpload.vue -->
<template>
    <div class="TextOCR">
        <div v-if="isLoading" class="loading-overlay">
            <div class="loader"></div>
        </div>
        <!-- 图片上传区域 -->
        <div class="upload-area" @click="triggerUpload" @dragover.prevent="handleDragOver" @drop.prevent="handleDrop">
            <input ref="fileInput" type="file" accept="image/*" @change="handleFileSelect" style="display: none;">
            <div v-if="!previewUrl" class="upload-placeholder">
                <el-icon :size="50">
                    <Upload />
                </el-icon>
                <div class="upload-text">点击上传图片或拖拽到此区域</div>
            </div>
            <img v-else :src="previewUrl" class="preview-image" />
        </div>

        <!-- 文本编辑区域 -->
        <div class="text-editor">
            <el-input v-model="ocrText" type="textarea" :rows="15" placeholder="识别结果将显示在此处" resize="none" />
            <div class="action-buttons">
                <el-button type="primary" @click="handleConfirm" :disabled="!ocrText">
                    确认使用
                </el-button>
                <el-button @click="handleCancel">取消</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['confirm', 'cancel'])

const fileInput = ref(null)
const previewUrl = ref('')
const ocrText = ref('')

// 等待状态
const isLoading = ref(false);

// 图片上传函数
// 点击
const triggerUpload = () => {
    fileInput.value?.click()
}
// 拖拽图片至区域
const handleDragOver = (e) => {
    e.dataTransfer.dropEffect = 'copy'
}
const handleDrop = (e) => {
    const file = e.dataTransfer.files[0]
    if (file) handleFileSelect({ target: { files: [file] } })
}

const handleFileSelect = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    // 验证文件
    if (!file.type.startsWith('image/')) {
        ElMessage.error('请选择图片文件')
        return
    }

    if (file.size > 5 * 1024 * 1024) {
        ElMessage.error('图片大小不能超过5MB')
        return
    }

    try {
        isLoading.value = true
        previewUrl.value = URL.createObjectURL(file)

        // 创建FormData
        const formData = new FormData()
        formData.append('file', file)

        // 发送请求
        const response = await fetch('http://localhost:5000/api/TextOCR', {
            method: 'POST',
            body: formData
        })

        const data = await response.json()
        if (data.status === 'success') {
            ocrText.value = data.result
        } else {
            throw new Error(data.message || '识别失败')
        }
    } catch (error) {
        ElMessage.error(`OCR错误: ${error.message}`)
        handleCancel()
    } finally {
        isLoading.value = false
    }
}

const handleConfirm = () => {
    emit('confirm', ocrText.value)
    reset()
}

const handleCancel = () => {
    emit('cancel')
    reset()
}

const reset = () => {
    previewUrl.value = ''
    ocrText.value = ''
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}
</script>

<style scoped>
.TextOCR {
    display: flex;
    gap: 20px;
    padding: 20px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
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

.upload-area {
    flex: 1;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    padding: 20px;
    min-height: 300px;
}

.upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #909399;
}

.preview-image {
    width: 100%;
    height: auto;
    max-height: 500px;
    object-fit: contain;
}

.text-editor {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.action-buttons {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}
</style>