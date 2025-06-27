<template>
    <div class="AIToolsList">
        <!-- 功能导航标题 -->
        <div class="header-section">
            <h1 class="ai-tools-title">严小希工作室の能力大全</h1>
            <p class="ai-tools-subtitle">请问您需要严小希的什么帮助呢？</p>
        </div>

        <!-- 功能卡片网格 -->
        <div class="tools-grid">
            <!-- AI续写卡片 -->
            <router-link to="/AIContinuation" class="tool-card continue-writing">
                <div class="card-content">
                    <div class="icon-wrapper">
                        <svg class="magic-icon" viewBox="0 0 24 24">
                            <path
                                d="M14.5 2.5c1.03 0 1.9.62 2.29 1.5h1.21c.17 0 .33.09.42.23l.03.05 2.47 4.52c.17.3.26.64.26.98v5c0 .85-.34 1.63-.88 2.2l-.12.12-4.5 4.5c-.58.58-1.36.9-2.18.9H6c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h8.5zm-4 4L8 11h2v4H8l2.5 4.5L13 14h-2v-4h2l-2.5-4.5z" />
                        </svg>
                    </div>
                    <h3 class="tool-title">智能续写</h3>
                    <p class="tool-description">基于当前内容自动生成后续文本</p>
                    <div class="action-indicator">
                        <span>立即体验</span>
                        <i class="arrow-icon">→</i>
                    </div>
                </div>
            </router-link>

            <!-- AI润色卡片 -->
            <router-link to="/AIPolishment" class="tool-card text-polish">
                <div class="card-content">
                    <div class="icon-wrapper">
                        <svg class="brush-icon" viewBox="0 0 24 24">
                            <path
                                d="M20.71 4.04c.39.39.39 1.04 0 1.41L18.37 7.8l-2.29-2.29 2.37-2.37c.39-.39 1.02-.39 1.41 0l1.25 1.25zM15.56 9.15L8.7 16H6v-2.7l6.84-6.86 2.29 2.29zM4 20h16v-1c0-2.24-1.75-4-4-4h-2v-2h2c2.24 0 4-1.76 4-4V4H4v16z" />
                        </svg>
                    </div>
                    <h3 class="tool-title">文本润色</h3>
                    <p class="tool-description">优化语言表达，提升文本质量</p>
                    <div class="action-indicator">
                        <span>立即优化</span>
                        <i class="arrow-icon">→</i>
                    </div>
                </div>
            </router-link>

            <!-- AI摘抄卡片 -->
            <router-link to="/AITextExtracts" class="tool-card smart-excerpt">
                <div class="card-content">
                    <div class="icon-wrapper">
                        <svg class="scissors-icon" viewBox="0 0 24 24">
                            <path
                                d="M20 4h-6l2.9 2.9-5.1 5.1 2.2 2.2 5.1-5.1L20 12V4zM4 4h6l-2.9 2.9 5.1 5.1-2.2 2.2-5.1-5.1L4 12V4zm13 12.2l-2.2-2.2-2.9 2.9H14v2H9.8l-2.9-2.9L4 16.8V20h16v-4.8l-2.9-2.9-2.1 2.1z" />
                        </svg>
                    </div>
                    <h3 class="tool-title">自动摘抄</h3>
                    <p class="tool-description">实现摘抄自由，从这里开始！<br>再也不用担心被语文老师停晚自习啦~</p>
                    <div class="action-indicator">
                        <span>开始摘抄</span>
                        <i class="arrow-icon">→</i>
                    </div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<style scoped>
.AIToolsList {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 20px;
}

.header-section {
    text-align: center;
    margin-bottom: 3rem;
}

.ai-tools-title {
    font-size: 2.5rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.ai-tools-subtitle {
    color: #7f8c8d;
    font-size: 1.1rem;
}

.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 1rem;
}

.tool-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-decoration: none;
    color: inherit;
    border: 1px solid #e0e0e0;
}

.tool-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 不同功能的主题色 */
.continue-writing {
    border-top: 4px solid #4CAF50;
}

.text-polish {
    border-top: 4px solid #2196F3;
}

.smart-excerpt {
    border-top: 4px solid #9C27B0;
}

.card-content {
    position: relative;
    height: 100%;
}

.icon-wrapper {
    margin-bottom: 1.5rem;
}

.tool-title {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 0.8rem;
}

.tool-description {
    color: #7f8c8d;
    line-height: 1.6;
    min-height: 60px;
}

.action-indicator {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 2rem;
    color: #4CAF50;
    font-weight: 500;
}

.arrow-icon {
    font-size: 1.2rem;
    transition: transform 0.3s ease;
}

.tool-card:hover .arrow-icon {
    transform: translateX(3px);
}

/* 图标样式 */
.magic-icon,
.brush-icon,
.scissors-icon {
    width: 48px;
    height: 48px;
    fill: currentColor;
}

.continue-writing .icon-wrapper {
    color: #4CAF50;
}

.text-polish .icon-wrapper {
    color: #2196F3;
}

.smart-excerpt .icon-wrapper {
    color: #9C27B0;
}

@media (max-width: 768px) {
    .tools-grid {
        grid-template-columns: 1fr;
    }
}
</style>