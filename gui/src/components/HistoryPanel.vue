<template>
    <div class="history-panel" :class="{ 'collapsed': isCollapsed }">
        <!-- 历史记录头部 -->
        <div class="history-header">
            <div class="history-title">
                <i class="fas fa-history"></i>
                <span>对话历史</span>
            </div>
            <div class="history-controls">
                <button @click="clearHistory" class="clear-btn" title="清空历史记录">
                    <i class="fas fa-trash"></i>
                </button>
                <button @click="toggleCollapse" class="collapse-btn" title="收起/展开">
                    <i :class="isCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
                </button>
            </div>
        </div>

        <!-- 历史记录列表 -->
        <div v-if="!isCollapsed" class="history-list">
            <div v-if="historyList.length === 0" class="empty-history">
                <i class="fas fa-comments"></i>
                <p>暂无对话记录</p>
                <span>开始和严小希对话吧！</span>
            </div>
            
            <div v-else class="history-items">
                <div 
                    v-for="(session, index) in historyList" 
                    :key="session.id"
                    :class="['history-item', { 'active': currentSessionId === session.id }]"
                    @click="selectSession(session)"
                >
                    <div class="session-header">
                        <div class="session-title">
                            <i class="fas fa-comment-dots"></i>
                            <span>{{ session.title || '对话' + (index + 1) }}</span>
                        </div>
                        <div class="session-time">{{ formatDate(session.lastTime) }}</div>
                    </div>
                    <div class="session-preview">
                        <span class="preview-text">{{ session.preview }}</span>
                    </div>
                    <div class="session-actions">
                        <button @click.stop="deleteSession(session.id)" class="delete-session-btn" title="删除此对话">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 新建对话按钮 -->
        <div v-if="!isCollapsed" class="new-chat-section">
            <button @click="createNewSession" class="new-chat-btn">
                <i class="fas fa-plus"></i>
                <span>新建对话</span>
            </button>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
    name: 'HistoryPanel',
    props: {
        messages: {
            type: Array,
            default: () => []
        },
        currentSessionId: {
            type: String,
            default: null
        }
    },
    emits: ['session-selected', 'session-created', 'session-deleted', 'history-cleared', 'toggle-collapse'],
    setup(props, { emit }) {
        const isCollapsed = ref(false);
        const historyList = ref([]);

        // 从localStorage加载历史记录
        const loadHistory = () => {
            try {
                const saved = localStorage.getItem('yanxx_chat_history');
                if (saved) {
                    historyList.value = JSON.parse(saved);
                }
            } catch (error) {
                console.error('加载历史记录失败:', error);
                historyList.value = [];
            }
        };

        // 保存历史记录到localStorage
        const saveHistory = () => {
            try {
                localStorage.setItem('yanxx_chat_history', JSON.stringify(historyList.value));
            } catch (error) {
                console.error('保存历史记录失败:', error);
            }
        };

        // 创建新的对话会话
        const createNewSession = () => {
            const newSession = {
                id: Date.now().toString(),
                title: '新对话',
                preview: '开始新的对话...',
                messages: [],
                lastTime: new Date().toISOString(),
                createdAt: new Date().toISOString()
            };
            
            historyList.value.unshift(newSession);
            saveHistory();
            emit('session-created', newSession);
        };

        // 选择对话会话
        const selectSession = (session) => {
            emit('session-selected', session);
        };

        // 删除对话会话
        const deleteSession = (sessionId) => {
            if (confirm('确定要删除这个对话吗？')) {
                const index = historyList.value.findIndex(s => s.id === sessionId);
                if (index > -1) {
                    historyList.value.splice(index, 1);
                    saveHistory();
                    emit('session-deleted', sessionId);
                }
            }
        };

        // 清空所有历史记录
        const clearHistory = () => {
            if (confirm('确定要清空所有对话历史吗？此操作不可恢复！')) {
                historyList.value = [];
                saveHistory();
                emit('history-cleared');
            }
        };

        // 切换折叠状态
        const toggleCollapse = () => {
            isCollapsed.value = !isCollapsed.value;
            emit('toggle-collapse', isCollapsed.value);
        };

        // 格式化日期
        const formatDate = (dateString) => {
            const date = new Date(dateString);
            const now = new Date();
            const diff = now - date;
            
            // 今天
            if (diff < 24 * 60 * 60 * 1000) {
                return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            }
            // 昨天
            else if (diff < 48 * 60 * 60 * 1000) {
                return '昨天';
            }
            // 一周内
            else if (diff < 7 * 24 * 60 * 60 * 1000) {
                const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
                return days[date.getDay()];
            }
            // 更早
            else {
                return date.toLocaleDateString();
            }
        };

        // 更新当前会话
        const updateCurrentSession = () => {
            if (!props.currentSessionId || props.messages.length === 0) return;
            
            const session = historyList.value.find(s => s.id === props.currentSessionId);
            if (session) {
                // 更新会话信息
                session.messages = [...props.messages];
                session.lastTime = new Date().toISOString();
                
                // 生成预览文本
                const lastUserMessage = props.messages
                    .filter(msg => msg.sender === 'user')
                    .pop();
                
                if (lastUserMessage) {
                    session.preview = lastUserMessage.content.length > 30 
                        ? lastUserMessage.content.substring(0, 30) + '...'
                        : lastUserMessage.content;
                }
                
                // 生成标题
                if (props.messages.length >= 2) {
                    const firstUserMessage = props.messages.find(msg => msg.sender === 'user');
                    if (firstUserMessage) {
                        session.title = firstUserMessage.content.length > 20 
                            ? firstUserMessage.content.substring(0, 20) + '...'
                            : firstUserMessage.content;
                    }
                }
                
                // 重新排序，将当前会话移到顶部
                const index = historyList.value.findIndex(s => s.id === props.currentSessionId);
                if (index > 0) {
                    const session = historyList.value.splice(index, 1)[0];
                    historyList.value.unshift(session);
                }
                
                saveHistory();
            }
        };

        // 监听消息变化，更新当前会话
        watch(() => props.messages, updateCurrentSession, { deep: true });

        // 组件挂载时加载历史记录
        loadHistory();

        return {
            isCollapsed,
            historyList,
            createNewSession,
            selectSession,
            deleteSession,
            clearHistory,
            toggleCollapse,
            formatDate
        };
    }
};
</script>

<style scoped>
.history-panel {
    width: 280px;
    height: 100%;
    background: #f8fafc;
    border-right: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    transition: width 0.3s ease;
    overflow: hidden;
}

.history-panel.collapsed {
    width: 60px;
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #e2e8f0;
    background: white;
    min-height: 60px;
}

.history-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #1e293b;
}

.history-title i {
    color: #3b82f6;
}

.history-controls {
    display: flex;
    gap: 4px;
}

.clear-btn, .collapse-btn {
    background: none;
    border: none;
    color: #64748b;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.clear-btn:hover, .collapse-btn:hover {
    background: #f1f5f9;
    color: #475569;
}

.clear-btn i, .collapse-btn i {
    font-size: 0.9rem;
}

.history-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
}

.empty-history {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #94a3b8;
    text-align: center;
}

.empty-history i {
    font-size: 2rem;
    margin-bottom: 12px;
    color: #cbd5e1;
}

.empty-history p {
    margin: 8px 0 4px 0;
    font-weight: 500;
}

.empty-history span {
    font-size: 0.85rem;
}

.history-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.history-item {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}

.history-item:hover {
    border-color: #3b82f6;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.history-item.active {
    border-color: #3b82f6;
    background: #eff6ff;
}

.session-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 6px;
}

.session-title {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
    color: #1e293b;
    flex: 1;
    min-width: 0;
}

.session-title i {
    color: #3b82f6;
    font-size: 0.8rem;
}

.session-title span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.session-time {
    font-size: 0.75rem;
    color: #94a3b8;
    white-space: nowrap;
    margin-left: 8px;
}

.session-preview {
    margin-bottom: 8px;
}

.preview-text {
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.session-actions {
    display: flex;
    justify-content: flex-end;
    opacity: 0;
    transition: opacity 0.2s;
}

.history-item:hover .session-actions {
    opacity: 1;
}

.delete-session-btn {
    background: none;
    border: none;
    color: #ef4444;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.delete-session-btn:hover {
    background: #fef2f2;
    color: #dc2626;
}

.delete-session-btn i {
    font-size: 0.8rem;
}

.new-chat-section {
    padding: 16px;
    border-top: 1px solid #e2e8f0;
    background: white;
}

.new-chat-btn {
    width: 100%;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.new-chat-btn:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.new-chat-btn i {
    font-size: 0.9rem;
}

/* 折叠状态样式 */
.history-panel.collapsed .history-title span,
.history-panel.collapsed .history-controls,
.history-panel.collapsed .history-list,
.history-panel.collapsed .new-chat-section {
    display: none;
}

.history-panel.collapsed .history-header {
    justify-content: center;
    padding: 16px 8px;
}

.history-panel.collapsed .collapse-btn {
    position: absolute;
    right: 8px;
}

/* 滚动条样式 */
.history-list::-webkit-scrollbar {
    width: 4px;
}

.history-list::-webkit-scrollbar-track {
    background: transparent;
}

.history-list::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 2px;
}

.history-list::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .history-panel {
        width: 100%;
        height: auto;
        max-height: 300px;
        border-right: none;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .history-panel.collapsed {
        width: 100%;
        max-height: 60px;
    }
}
</style> 