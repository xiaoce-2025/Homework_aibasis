# 技术架构文档

## 系统概述

严小希AI助手是一个基于Python和Vue.js的混合架构应用，集成了桌面宠物、AI文本处理和Web界面功能。系统采用前后端分离的设计模式，通过RESTful API进行通信。

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    严小希AI助手系统架构                        │
├─────────────────────────────────────────────────────────────┤
│  桌面宠物层 (PyQt6)                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   桌面宠物界面   │  │   系统托盘       │  │   右键菜单   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Web界面层 (Vue.js)                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   用户界面       │  │   路由管理       │  │   状态管理   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  API服务层 (Flask)                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   路由处理       │  │   中间件         │  │   错误处理   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  业务逻辑层 (Python)                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   AI文本处理     │  │   OCR识别        │  │   智能对话   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  数据存储层 (JSON)                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   用户数据       │  │   历史记录       │  │   配置信息   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 技术栈

### 后端技术栈

| 技术 | 版本 | 用途 | 说明 |
|------|------|------|------|
| Python | 3.8+ | 主要开发语言 | 系统核心语言 |
| Flask | 2.0+ | Web框架 | API服务提供 |
| PyQt6 | 6.0+ | GUI框架 | 桌面宠物界面 |
| PaddleOCR | 2.0+ | OCR引擎 | 文字识别 |
| requests | 2.25+ | HTTP客户端 | API调用 |
| json | 内置 | 数据序列化 | 配置和数据存储 |

### 前端技术栈

| 技术 | 版本 | 用途 | 说明 |
|------|------|------|------|
| Vue.js | 3.2+ | 前端框架 | 用户界面构建 |
| Element Plus | 2.9+ | UI组件库 | 界面组件 |
| Vue Router | 4.5+ | 路由管理 | 页面导航 |
| Pinia | 3.0+ | 状态管理 | 应用状态 |
| Axios | 1.8+ | HTTP客户端 | API请求 |
| Sass | 1.86+ | CSS预处理器 | 样式管理 |

### 外部服务

| 服务 | 用途 | 说明 |
|------|------|------|
| 硅基流动API | 文本转语音、AI文本处理 | 语音合成服务、文本生成和优化、图片解析 |
| PaddleOCR | OCR识别 | 开源OCR引擎 |

## 模块设计

### 1. 桌面宠物模块 (DesktopPet)

#### 核心组件
- **DesktopPet类**：桌面宠物的主要实现
- **SettingsDialog类**：设置对话框
- **动画系统**：帧动画和状态管理
- **移动系统**：平滑移动和路径规划

#### 技术特点
```python
class DesktopPet(QWidget):
    def __init__(self):
        # 窗口设置
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 动画系统
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        
        # 移动系统
        self.smooth_move_timer = QTimer()
        self.smooth_move_timer.timeout.connect(self.smooth_move)
```

#### 功能模块
- **图像管理**：加载和管理宠物动画帧
- **交互系统**：鼠标事件处理和右键菜单
- **设置系统**：个性化配置管理
- **托盘集成**：系统托盘功能

### 2. API服务模块 (Api.py)

#### 路由设计
```python
# 用户认证
@app.route('/api/UserLogin', methods=['POST'])
@app.route('/api/UserSignUp', methods=['POST'])

# AI文本处理
@app.route('/api/submit', methods=['POST'])
@app.route('/api/AIPolish', methods=['POST'])
@app.route('/api/AITextExtracts', methods=['POST'])

# OCR识别
@app.route('/api/TextOCR', methods=['POST'])

# 智能对话
@app.route('/api/dialog', methods=['POST'])
@app.route('/api/dialog/multimodal', methods=['POST'])

# 文本转语音
@app.route('/api/AIread', methods=['POST'])
```

#### 中间件
- **CORS支持**：跨域请求处理
- **错误处理**：统一错误响应格式
- **日志记录**：请求和响应日志
- **数据验证**：请求参数验证

### 3. AI文本处理模块

#### AIContinuation.py
```python
class ContinueWrite:
    @staticmethod
    def AI_Continuation_Suggest(data):
        # 文本分析
        # 风格识别
        # 内容生成
        # 质量评估
        return suggestions
```

#### AIPolishment.py
```python
class PolishWrite:
    @staticmethod
    def AI_Polishment(data):
        # 语法检查
        # 表达优化
        # 逻辑优化
        # 风格统一
        return polished_text
```

#### AITextExtracts.py
```python
class AutoExtract:
    @staticmethod
    def AI_Auto_Extract(data):
        # 文本分析
        # 重点识别
        # 内容提取
        # 格式整理
        return extracts
```

### 4. OCR识别模块 (TextOCR.py)

#### 技术实现
```python
class TextOCR:
    @staticmethod
    def ocr_processing(request):
        # 图片预处理
        # OCR识别
        # 结果后处理
        # 格式输出
        return result
```

#### 支持特性
- 多语言识别（中文、英文）
- 多种图片格式支持
- 自动语言检测
- 识别结果优化

### 5. 智能对话模块 (YanxxDialog.py)

#### 对话系统
```python
class YanxxDialog:
    @staticmethod
    def AI_Yanxx_dialog(data, classify=False):
        # 意图理解
        # 上下文管理
        # 回复生成
        # 情感表达
        return response
```

#### 多模态支持
- 文本对话
- 图片理解
- 情感识别
- 上下文记忆

### 6. 用户认证模块 (Auth.py)

#### 认证流程
```python
class Auth:
    @staticmethod
    def login(data):
        # 用户验证
        # 密码检查
        # 会话管理
        return result
    
    @staticmethod
    def SignUp(data):
        # 用户注册
        # 数据验证
        # 账户创建
        return result
```

## 数据流设计

### 1. 桌面宠物数据流

```
用户交互 → 事件处理 → 状态更新 → 界面刷新
    ↓
设置变更 → 配置保存 → 参数应用 → 行为调整
```

### 2. Web界面数据流

```
用户操作 → Vue组件 → API请求 → Flask路由 → 业务逻辑 → 数据存储
    ↓
响应数据 → 状态更新 → 界面渲染 → 用户反馈
```

### 3. AI处理数据流

```
输入文本 → 预处理 → AI模型 → 结果生成 → 后处理 → 格式化输出
```

## 安全设计

### 1. 数据安全
- **敏感词过滤**：内置敏感词库进行内容过滤
- **输入验证**：严格的参数验证和类型检查
- **数据加密**：敏感数据加密存储

### 2. 访问控制
- **用户认证**：用户名密码验证
- **会话管理**：安全的会话处理
- **权限控制**：功能访问权限管理

### 3. 网络安全
- **CORS配置**：跨域请求安全控制
- **请求限制**：API调用频率限制
- **错误处理**：安全的错误信息处理

## 性能优化

### 1. 前端优化
- **组件懒加载**：按需加载组件
- **资源压缩**：静态资源压缩
- **缓存策略**：浏览器缓存优化

### 2. 后端优化
- **异步处理**：非阻塞IO操作
- **连接池**：数据库连接复用
- **内存管理**：合理的内存使用

### 3. 系统优化
- **多线程**：并发请求处理
- **资源管理**：系统资源合理分配
- **监控告警**：性能监控和告警

## 部署架构

### 开发环境
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端开发服务器  │    │   后端API服务器  │    │   桌面宠物应用   │
│   (localhost:8080) │    │   (localhost:5000) │    │   (本地运行)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```
