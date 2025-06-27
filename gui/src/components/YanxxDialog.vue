<template>
    <div class="chat-layout">
        <!-- 历史记录面板 -->
        <HistoryPanel 
            :messages="messages"
            :current-session-id="currentSessionId"
            @session-selected="loadSession"
            @session-created="createSession"
            @session-deleted="handleSessionDeleted"
            @history-cleared="handleHistoryCleared"
            @toggle-collapse="handleHistoryToggle"
        />
        
        <!-- 对话容器 -->
        <div class="chat-container" :style="{ width: containerWidth, height: containerHeight }">
            <div ref="messagesContainer" class="messages">
                <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender]">
                    <div v-if="msg.sender === 'user'" class="message-content">
                        <span class="username">我</span> {{ msg.content }}
                        <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
                    </div>
                    <div v-else class="message-content">
                        <!-- 新增语音播放按钮 -->
                        <button v-if="!msg.loading" @click="playVoice(msg)" class="voice-play-btn">
                            <i class="fas fa-volume-up"></i>
                        </button>
                        
                        <span class="username">严小希</span>
                        <span v-if="msg.loading" class="loading-dots">思考中</span>
                        <span v-else>{{ msg.content }}</span>
                        <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
                        
                        <!-- AI续写跳转条 -->
                        <div v-if="!msg.loading && msg.showContinuation" class="continuation-bar">
                            <div class="divider"></div>
                            <button @click="gotoContinuation" class="continuation-btn">点击此处让小希来帮你续写 -></button>
                        </div>

                        <!-- AI润色跳转条 -->
                        <div v-if="!msg.loading && msg.showPolishment" class="continuation-bar">
                            <div class="divider"></div>
                            <button @click="gotoPolishment" class="continuation-btn">点击此处让小希来帮你润色 -></button>
                        </div>

                        <!-- AI摘抄跳转条 -->
                        <div v-if="!msg.loading && msg.showExtraction" class="continuation-bar">
                            <div class="divider"></div>
                            <button @click="gotoExtraction" class="continuation-btn">点击此处让小希来帮你摘抄 -></button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 图片预览区域 - 在输入框上方 -->    
            <div v-if="selectedImage" class="image-preview-area">
                <div class="image-preview-header">
                    <span class="image-preview-title">已选择图片</span>
                    <button @click="removeImage" class="remove-image-btn" title="移除图片">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="image-preview-content">
                    <div @click="showImagePreview" class="image-thumbnail-container">
                        <img :src="`data:${selectedImage.type};base64,${selectedImage.data}`" 
                             :alt="selectedImage.name" 
                             class="image-thumbnail">
                        <div class="image-overlay">
                            <i class="fas fa-eye"></i>
                            <span class="image-filename">{{ selectedImage.name }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 图片全屏预览遮罩 -->
            <div v-if="showPreview" @click="hideImagePreview" class="image-preview-overlay">
                <div class="image-preview-modal" @click.stop>
                    <div class="image-preview-modal-header">
                        <span class="image-preview-modal-title">{{ selectedImage?.name }}</span>
                        <button @click="hideImagePreview" class="close-preview-btn">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="image-preview-modal-content">
                        <img v-if="selectedImage" 
                             :src="`data:${selectedImage.type};base64,${selectedImage.data}`" 
                             :alt="selectedImage.name" 
                             class="image-preview-full">
                    </div>
                </div>
            </div>  

            <div class="input-area" :style="{ width: inputAreaWidth }">
                <textarea v-model="userInput" placeholder="输入你的问题..." @keydown.enter.exact.prevent="sendMessage"
                    :disabled="isLoading" rows="2"></textarea>
                <div class="input-buttons">
                    <!-- 图片输入按钮 -->
                    <button @click="triggerImageUpload" :disabled="isLoading" class="image-upload-btn" title="上传图片进行OCR识别">
                        <i class="fas fa-image"></i>
                    </button>
                    <input ref="imageInput" type="file" accept="image/*" @change="handleImageUpload" style="display: none;">
                    <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
                        {{ isLoading ? '发送中...' : '发送' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, watch, nextTick, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useConfigStore } from '../../stores/config';
import HistoryPanel from './HistoryPanel.vue';

export default {
    components: {
        HistoryPanel
    },
    props: {
        width: {
            type: String,
            default: '100%'
        },
        height: {
            type: String,
            default: '100%'
        }
    },
    setup(props) {
        const router = useRouter();
        const configStore = useConfigStore();
        const config = ref({
            ModelName: configStore.settings.textModel.name,
            apiKey: configStore.settings.textModel.apiKey,
            apiUrl: configStore.settings.textModel.apiUrl,
            ModelTemperature: configStore.settings.textModel.params.temperature
        });

        const messages = reactive([]);
        const userInput = ref('');
        const isLoading = ref(false);
        const messagesContainer = ref(null);
        const currentAIResponse = ref(null); // 跟踪当前AI响应
        const containerWidth = ref(props.width);
        const containerHeight = ref(props.height);
        const showPreview = ref(false); // 控制图片全屏预览显示
        const selectedImage = ref(null); // 存储选中的图片数据
        const imageInput = ref(null);
        
        // 历史记录相关
        const currentSessionId = ref(null);
        const isHistoryCollapsed = ref(false); // 跟踪历史面板折叠状态

        watch([() => props.width, () => props.height], () => {
            containerWidth.value = props.width;
            containerHeight.value = props.height;
        });

        const scrollToBottom = () => {
            nextTick(() => {
                if (messagesContainer.value) {
                    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
                }
            });
        };

        // 历史记录相关函数
        const createSession = (session) => {
            currentSessionId.value = session.id;
            messages.length = 0; // 清空当前消息
            scrollToBottom();
        };

        const loadSession = (session) => {
            currentSessionId.value = session.id;
            messages.length = 0; // 清空当前消息
            // 加载会话消息
            if (session.messages && session.messages.length > 0) {
                messages.push(...session.messages);
            }
            scrollToBottom();
        };

        const handleSessionDeleted = (sessionId) => {
            if (currentSessionId.value === sessionId) {
                // 如果删除的是当前会话，清空消息并创建新会话
                messages.length = 0;
                currentSessionId.value = null;
                createNewSession();
            }
        };

        const handleHistoryCleared = () => {
            messages.length = 0;
            currentSessionId.value = null;
            createNewSession();
        };

        const createNewSession = () => {
            const newSession = {
                id: Date.now().toString(),
                title: '新对话',
                preview: '开始新的对话...',
                messages: [],
                lastTime: new Date().toISOString(),
                createdAt: new Date().toISOString()
            };
            currentSessionId.value = newSession.id;
        };

        // 路由跳转函数
        const gotoContinuation = () => {
            router.push('/AIContinuation');
        };

        const gotoPolishment = () => {
            router.push('/AIPolishment');
        };

        const gotoExtraction = () => {
            router.push('/AITextExtracts');
        };

        // 格式化时间戳
        const formatTime = (timestamp) => {
            const date = new Date(timestamp);
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        };

        // 流式处理函数 - 异步生成器
        const processStream = async function*(response) {
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `请求失败: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                
                if (done) {
                    break;
                }

                // 解码并追加数据
                buffer += decoder.decode(value, { stream: true });
                
                // 按行分割处理
                const lines = buffer.split('\n');
                buffer = lines.pop() || ''; // 保留不完整的行
                
                for (const line of lines) {
                    const trimmedLine = line.trim();
                    if (!trimmedLine.startsWith('data:')) continue;
                    
                    const content = trimmedLine.substring(5).trim();
                    
                    // 处理特殊标记
                    if (content === '[DONE]') {
                        yield { type: 'done' };
                        continue;
                    }
                    
                    // 处理错误
                    if (content.includes('error')) {
                        try {
                            const error = JSON.parse(content);
                            throw new Error(error.error || '未知错误');
                        } catch {
                            throw new Error(content);
                        }
                    }
                    
                    // 解析内容并返回
                    yield { type: 'content', data: content };
                }
            }
        };
        
        // 新增：API Key校验函数
        const validateAPIKey = () => {
            const apiKey = config.value.apiKey;
            
            // 检查是否存在API Key
            if (!apiKey) {
                return {
                    valid: false,
                    message: 'API Key未设置，请先配置API密钥'
                };
            }
            
            // 检查是否为有效字符串
            if (typeof apiKey !== 'string' || apiKey.trim() === '') {
                return {
                    valid: false,
                    message: 'API Key格式不正确，请检查输入'
                };
            }
            
            // 示例：根据常见API Key格式进行长度检查（可根据实际API要求调整）
            if (apiKey.length < 10) {
                return {
                    valid: false,
                    message: 'API Key长度过短，可能无效'
                };
            }
            
            return { valid: true };
        };

        const sendMessage = async () => {
            if (!userInput.value.trim() || isLoading.value) return;

            // 如果没有当前会话，创建一个新会话
            if (!currentSessionId.value) {
                createNewSession();
            }

            const userMessage = userInput.value.trim();
            userInput.value = '';

            // 添加用户消息
            messages.push({
                sender: 'user',
                content: userMessage,
                timestamp: new Date()
            });

            // 添加AI消息占位符
            const aiMessageRef = {
                sender: 'ai',
                content: '',
                loading: true,
                timestamp: new Date(),
                showContinuation: false,
                showPolishment: false,
                showExtraction: false,
            };
            messages.push(aiMessageRef);
            currentAIResponse.value = aiMessageRef;

            scrollToBottom();
            isLoading.value = true;
            
            // api配置校验
            const validationResult = validateAPIKey();
            if (!validationResult.valid) {
                // 校验失败处理
                isLoading.value = false;
                currentAIResponse.value.content = validationResult.message;
                currentAIResponse.value.loading = false;
                return;
            }

            const historyMessages = messages.slice(0, -2);
            
            // 1. 先调用分类接口
            try {
                aiMessageRef.loading = false;
                // 构建分类请求体
                let classifyRequestBody;
                
                if (selectedImage.value) {
                    // 有图片时包含图片数据
                    classifyRequestBody = {
                        config: config.value,
                        content: historyMessages,
                        ContentRequest: userMessage,
                        image: selectedImage.value
                    };
                } else {
                    // 没有图片时不包含image字段
                    classifyRequestBody = {
                        config: config.value,
                        content: historyMessages,
                        ContentRequest: userMessage
                    };
                }
                
                // 调用分类接口
                const classifyResponse = await fetch('http://localhost:5000/api/dialog/classify', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(classifyRequestBody)
                });
                
                if (!classifyResponse.ok) {
                    throw new Error(`分类接口请求失败: ${classifyResponse.status}`);
                }
                
                // 解析分类结果
                const classifyResult = await classifyResponse.json();
                console.log("分类结果:", classifyResult);
                
                // 根据分类结果设置显示标志
                aiMessageRef.showContinuation = classifyResult.TextContinuation || false;
                aiMessageRef.showPolishment = classifyResult.TextPolishment || false;
                aiMessageRef.showExtraction = classifyResult.Extraction || false;
                
            } catch (classifyError) {
                console.error("分类接口调用失败:", classifyError);
                // 分类失败时使用默认值（不显示任何功能按钮）
                aiMessageRef.showContinuation = false;
                aiMessageRef.showPolishment = false;
                aiMessageRef.showExtraction = false;
            }

            // 2. 调用对话接口
            const requestBody = {
                config: config.value,
                title: '用户对话',
                content: historyMessages,
                ContentRequest: userMessage,
                image: selectedImage.value // 包含图片数据
            };

            try {
                aiMessageRef.loading = false;
                // 使用setTimeout让出主线程，给DOM更新机会
                await new Promise(resolve => setTimeout(resolve, 0));

                // 根据是否有图片选择不同的API端点
                let apiEndpoint;
                let requestData;
                
                if (selectedImage.value) {
                    // 有图片时使用多模态API
                    apiEndpoint = '/api/dialog/multimodal';
                    requestData = requestBody;
                } else {
                    // 没有图片时使用普通API，不包含image字段
                    apiEndpoint = '/api/dialog';
                    requestData = {
                        config: config.value,
                        title: '用户对话',
                        content: historyMessages,
                        ContentRequest: userMessage
                    };
                }
                
                const response = await fetch(`http://localhost:5000${apiEndpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });

                // 使用异步生成器处理流式响应
                for await (const chunk of processStream(response)) {
                    if (!currentAIResponse.value) break; // 防止组件卸载后的无效操作
                    
                    switch (chunk.type) {
                        case 'content':
                            try {
                                const parsed = JSON.parse(chunk.data);
                                if (parsed.choices?.[0]?.delta?.content) {
                                    const textChunk = parsed.choices[0].delta.content;
                                    currentAIResponse.value.content += textChunk;
                                } else {
                                    currentAIResponse.value.content += chunk.data;
                                }
                            } catch (e) {
                                currentAIResponse.value.content += chunk.data;
                            }
                            scrollToBottom();
                            break;
                            
                        case 'done':
                            currentAIResponse.value.loading = false;
                            break;
                    }
                }
            } catch (error) {
                console.error('对话错误:', error);
                if (currentAIResponse.value) {
                    currentAIResponse.value.content = `请求失败: ${error.message}`;
                    currentAIResponse.value.loading = false;
                }
            } finally {
                isLoading.value = false;
                currentAIResponse.value = null;
                selectedImage.value = null; // 清空选中的图片
                showPreview.value = false; // 隐藏预览
                scrollToBottom();
            }
        };

        onMounted(() => {
            // 组件挂载时创建新会话
            createNewSession();
            scrollToBottom();
        });

        watch(messages, scrollToBottom, { deep: true });

        // 语音播放相关
        const currentPlayingVoice = ref(null);
        
        // 播放语音函数
        const playVoice = async (msg) => {
            // 如果有正在播放的语音，先停止
            if (currentPlayingVoice.value) {
                currentPlayingVoice.value.pause();
                currentPlayingVoice.value = null;
            }
            
            try {
                // 调用后端代理API
                const response = await fetch('http://localhost:5000/api/AIread', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text: msg.content,
                        apiKey: config.value.apiKey,
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`语音API请求失败: ${response.status}`);
                }
                
                // 处理二进制音频响应
                const audioBlob = await response.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                
                // 创建并播放音频
                const audio = new Audio(audioUrl);
                currentPlayingVoice.value = audio;
                
                audio.play();
                
                // 播放完成后清理
                audio.onended = () => {
                    currentPlayingVoice.value = null;
                    URL.revokeObjectURL(audioUrl);
                };
                
            } catch (error) {
                console.error('语音播放错误:', error);
                alert(`语音播放失败: ${error.message}`);
            }
        };

        // 图片输入相关
        const triggerImageUpload = () => {
            imageInput.value.click();
        };

        const handleImageUpload = async (event) => {
            const file = event.target.files[0];
            if (!file) return;

            // 验证文件类型
            if (!file.type.startsWith('image/')) {
                alert('请选择图片文件');
                return;
            }

            // 验证文件大小（5MB限制）
            if (file.size > 5 * 1024 * 1024) {
                alert('图片大小不能超过5MB');
                return;
            }

            try {
                // 将图片转换为base64格式
                const base64 = await fileToBase64(file);
                selectedImage.value = {
                    data: base64,
                    type: file.type,
                    name: file.name
                };
                
                // 在输入框中显示图片已选择
                const imageText = `[已选择图片: ${file.name}]`;
                if (userInput.value.trim()) {
                    userInput.value += '\n' + imageText;
                } else {
                    userInput.value = imageText;
                }
                
            } catch (error) {
                console.error('图片处理错误:', error);
                alert(`图片处理失败: ${error.message}`);
            } finally {
                // 清空文件输入
                if (imageInput.value) {
                    imageInput.value.value = '';
                }
            }
        };

        // 将文件转换为base64格式
        const fileToBase64 = (file) => {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => {
                    // 移除data:image/xxx;base64,前缀，只保留base64数据
                    const base64 = reader.result.split(',')[1];
                    resolve(base64);
                };
                reader.onerror = error => reject(error);
            });
        };

        // 图片预览功能
        const showImagePreview = () => {
            showPreview.value = true;
        };

        const hideImagePreview = () => {
            showPreview.value = false;
        };

        // 移除图片功能
        const removeImage = () => {
            selectedImage.value = null;
            showPreview.value = false; // 隐藏预览
            // 清空输入框中的图片提示文本
            userInput.value = userInput.value.replace(/\[已选择图片: .*?\]\n?/g, '').trim();
        };

        // 处理历史面板折叠状态变化
        const handleHistoryToggle = (collapsed) => {
            isHistoryCollapsed.value = collapsed;
        };

        // 计算输入框宽度
        const inputAreaWidth = computed(() => {
            // 检查是否在浏览器环境中
            if (typeof window !== 'undefined' && window.innerWidth <= 768) {
                return '100%';
            }
            return isHistoryCollapsed.value ? '100%' : '100%';
        });

        return {
            messages,
            userInput,
            isLoading,
            messagesContainer,
            sendMessage,
            containerWidth,
            containerHeight,
            formatTime,
            gotoContinuation,
            gotoPolishment,
            gotoExtraction,
            playVoice,
            imageInput,
            triggerImageUpload,
            handleImageUpload,
            selectedImage,
            showPreview,
            showImagePreview,
            hideImagePreview,
            removeImage,
            // 历史记录相关
            currentSessionId,
            createSession,
            loadSession,
            handleSessionDeleted,
            handleHistoryCleared,
            handleHistoryToggle,
            inputAreaWidth,
        };
    }
};
</script>

<style scoped>
/* 新增布局样式 */
.chat-layout {
    display: flex;
    width: 100%;
    height: 100vh;
    min-height: 0;
}

/* 基础布局与容器样式 */
.chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    background-color: #ffffff;
    min-width: 280px;
    max-width: 100%;
    min-height: 0;
    height: 100%;
    position: relative;
}

/* 消息区域样式 */
.messages {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 1% 2%;
    background-color: #f9fafb;
    display: flex;
    flex-direction: column;
}

/* 滚动条美化 */
.messages::-webkit-scrollbar {
    width: 6px;
}

.messages::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}

/* 消息气泡基础样式 */
.message {
    margin-bottom: 6px;
    padding: 6px 12px;
    border-radius: 16px;
    max-width: 75%;
    word-wrap: break-word;
    position: relative;
    animation: fadeIn 0.3s ease-out;
    font-size: 0.96rem;
}

/* 消息进入动画 */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 用户消息样式 */
.user {
    margin-left: auto;
    background: linear-gradient(135deg, #4080ff, #1890ff);
    color: white;
    border-bottom-right-radius: 6px;
    box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

/* AI消息样式 */
.ai {
    margin-right: auto;
    background-color: #f5f5f5;
    border-bottom-left-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 消息内容样式 */
.message-content {
    line-height: 1.3;
    position: relative;
    display: flex;
    flex-direction: column;
}

/* 用户名样式 */
.username {
    font-weight: 600;
    margin-right: 4px;
    display: block;
    font-size: 0.8rem;
    opacity: 0.7;
    text-align: left;
    margin-bottom: 2px;
}

/* 时间戳样式 */
.timestamp {
    font-size: 0.65rem;
    color: #b0b0b0;
    margin-top: 2px;
    display: block;
    text-align: right;
}

/* 输入区域样式 */
/* 输入区域样式 */
.input-area {
    display: flex;
    flex-direction: column;
    padding: 0.5% 2%;
    border-top: 1px solid #e5e7eb;
    background-color: white;
    box-sizing: border-box;
    width: 100%;
    z-index: 10;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    transition: width 0.3s ease;
}

/* 输入按钮组样式 - 调整为靠右排列 */
.input-buttons {
    display: flex;
    align-items: center;
    gap: 8px;
    justify-content: flex-end; /* 添加靠右排列 */
    margin-top: 8px; /* 保持与文本框的间距 */
}

/* 响应式设计中的输入框调整 */
@media (max-width: 768px) {
    .input-area {
        position: relative;
        bottom: auto;
        right: auto;
    }
    
    /* 小屏幕上按钮可能需要调整间距 */
    .input-buttons {
        gap: 4px;
    }
}
/* 文本输入框样式 */
textarea {
    flex: 1;
    padding: 6px 12px;
    border: 1px solid #d1d5db;
    border-radius: 16px;
    resize: none;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 1rem;
    line-height: 1.4;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-sizing: border-box;
}

textarea:focus {
    outline: none;
    border-color: #1890ff;
    box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.2);
}

/* 图片上传按钮样式 */
.image-upload-btn {
    padding: 8px 12px;
    background: linear-gradient(135deg, #52c41a, #389e0d);
    color: white;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

.image-upload-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #49aa19, #2f7a0a);
    box-shadow: 0 4px 12px rgba(82, 196, 26, 0.3);
    transform: translateY(-1px);
}

.image-upload-btn:active:not(:disabled) {
    transform: translateY(1px);
    box-shadow: 0 2px 6px rgba(82, 196, 26, 0.2);
}

.image-upload-btn:disabled {
    background-color: #f6ffed;
    color: #b7eb8f;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

.image-upload-btn i {
    font-size: 0.9rem;
}

/* 发送按钮样式 */
button {
    padding: 8px 14px;
    background: linear-gradient(135deg, #4080ff, #1890ff);
    color: white;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

button:hover:not(:disabled) {
    background: linear-gradient(135deg, #3170e0, #1880d0);
    box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
    transform: translateY(-1px);
}

button:active:not(:disabled) {
    transform: translateY(1px);
    box-shadow: 0 2px 6px rgba(24, 144, 255, 0.2);
}

button:disabled {
    background-color: #e5edff;
    color: #94b3ff;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

/* 加载状态动画优化 */
.loading-dots {
    display: inline-block;
    position: relative;
    width: 5vw;
    /* 使用视口宽度单位 */
    height: 3vw;
    /* 使用视口宽度单位 */
}

.loading-dots::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    margin: auto;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    border-radius: 50%;
    border: 3px solid #1890ff;
    border-top-color: transparent;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* 响应式设计优化 */
@media (max-width: 640px) {
    .chat-layout {
        flex-direction: column;
        height: 100%;
    }
    
    .chat-container {
        border-radius: 0;
        height: 100%;
        flex: 1;
    }
}

@media (max-width: 768px) {
    .input-area {
        position: relative;
        bottom: auto;
        right: auto;
    }
}

/* 用户消息("我")标签居右 */
.user .username {
    text-align: right;
    margin-left: auto;
    /* 右对齐辅助 */
}

/* AI消息("严小希")标签居左 */
.ai .username {
    text-align: left;
    margin-right: auto;
    /* 左对齐辅助 */
}

/* 时间戳对齐优化 */
.user .timestamp {
    text-align: left;
    /* 用户消息时间戳居左 */
}

.ai .timestamp {
    text-align: right;
    /* AI消息时间戳居右 */
}

/* 优化消息内容布局 */
.message-content {
    line-height: 1.6;
    position: relative;
    display: flex;
    flex-direction: column;
}

/*续写功能跳转条*/
.continuation-bar {
    margin-top: 12px;
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(to right, transparent, #d1d5db, transparent);
    margin-bottom: 10px;
}

.continuation-btn {
    background: transparent;
    border: 1px solid #1890ff;
    color: #1890ff;
    border-radius: 16px;
    padding: 3px 12px;
    font-size: 0.8rem;
    transition: all 0.2s;
    margin-top: 5px;
    cursor: pointer;
}

.continuation-btn:hover {
    background-color: #1890ff;
    color: white;
    box-shadow: 0 2px 6px rgba(24, 144, 255, 0.3);
    transform: translateY(-1px);
}

/* 语音播放按钮样式 */
.voice-play-btn {
    background: none;
    border: none;
    color: #6b7280;
    cursor: pointer;
    padding: 2px 6px;
    border-radius: 4px;
    margin-right: 8px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.voice-play-btn:hover {
    background-color: #e5edff;
    color: #1890ff;
}

.voice-play-btn i {
    font-size: 0.9rem;
}

/* 响应式设计中调整按钮大小 */
@media (max-width: 640px) {
    .voice-play-btn {
        padding: 1px 4px;
        margin-right: 5px;
    }
    
    .voice-play-btn i {
        font-size: 0.8rem;
    }
}

/* 图片预览区域样式 */
.image-preview-area {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-bottom: 1px solid #e5e7eb;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.image-preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.image-preview-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #1e40af;
}

.remove-image-btn {
    background: none;
    border: none;
    color: #ef4444;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.remove-image-btn:hover {
    background-color: #fef2f2;
    color: #dc2626;
}

.remove-image-btn i {
    font-size: 0.8rem;
}

.image-preview-content {
    display: flex;
    justify-content: center;
}

.image-thumbnail-container {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-thumbnail-container:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.image-thumbnail {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.3s ease;
}

.image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.image-thumbnail-container:hover .image-overlay {
    opacity: 1;
}

.image-overlay i {
    color: white;
    font-size: 1.2rem;
    margin-bottom: 4px;
}

.image-filename {
    color: white;
    font-size: 0.7rem;
    text-align: center;
    max-width: 90px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 响应式设计中的图片预览区域 */
@media (max-width: 640px) {
    .image-preview-area {
        padding: 8px 12px;
    }
    
    .image-thumbnail-container {
        width: 80px;
        height: 80px;
    }
    
    .image-filename {
        max-width: 70px;
        font-size: 0.65rem;
    }
    
    .image-preview-title {
        font-size: 0.8rem;
    }
    
    .image-preview-modal {
        max-width: 95%;
        max-height: 95%;
    }
    
    .image-preview-modal-header {
        padding: 12px 16px;
    }
    
    .image-preview-modal-title {
        font-size: 1rem;
        max-width: 200px;
    }
    
    .image-preview-modal-content {
        padding: 16px;
        max-height: 60vh;
    }
}

/* 图片全屏预览遮罩 */
.image-preview-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease;
}

.image-preview-modal {
    background: white;
    border-radius: 12px;
    max-width: 90%;
    max-height: 90%;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.image-preview-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #e5e7eb;
    background: #f9fafb;
}

.image-preview-modal-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #374151;
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.close-preview-btn {
    background: none;
    border: none;
    color: #6b7280;
    cursor: pointer;
    padding: 8px;
    border-radius: 6px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-preview-btn:hover {
    background-color: #f3f4f6;
    color: #374151;
}

.close-preview-btn i {
    font-size: 1.2rem;
}

.image-preview-modal-content {
    padding: 20px;
    text-align: center;
    max-height: 70vh;
    overflow: auto;
}

.image-preview-full {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>