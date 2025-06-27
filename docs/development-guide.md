# 开发指南

## 目录

1. [环境搭建](#环境搭建)
2. [项目结构](#项目结构)
3. [开发规范](#开发规范)
4. [开发流程](#开发流程)
5. [调试指南](#调试指南)
6. [测试指南](#测试指南)
7. [部署指南](#部署指南)
8. [贡献指南](#贡献指南)

## 环境搭建

### 系统要求

- **操作系统**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **Git**: 2.0 或更高版本

### 开发环境配置

#### 1. 克隆项目

```bash
git clone https://github.com/xiaoce-2025/aibasis_homework.git
cd aibasis_homework
```

#### 2. 后端环境配置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt
```

#### 3. 前端环境配置

```bash
# 安装Node.js依赖
cd gui
npm install

# 安装开发工具
npm install -g @vue/cli
npm install -g electron
```

### 使用的开发工具的开发工具

#### IDE
- **VS Code**

#### 浏览器扩展
- **Vue.js devtools**: Vue.js调试
- **React Developer Tools**: React调试
- **JSON Formatter**: JSON格式化

#### 其他工具
- **Postman**: API测试
- **GitKraken**: Git图形界面
- **Docker**: 容器化开发

## 项目结构

### 目录结构说明

```
aibasis_homework/
├── backend/                 # 后端代码
│   ├── main.py             # 桌面宠物主程序
│   ├── Api.py              # Flask API服务
│   ├── AIContinuation.py   # AI续写模块
│   ├── AIPolishment.py     # AI润色模块
│   ├── AITextExtracts.py   # AI摘抄模块
│   ├── TextOCR.py          # OCR识别模块
│   ├── YanxxDialog.py      # 智能对话模块
│   ├── Auth.py             # 用户认证模块
│   ├── database.py         # 数据库操作
│   ├── requirements.txt    # Python依赖
│   ├── resources/          # 资源文件
│   │   ├── yxx_images/     # 宠物图片资源
│   │   ├── icon.png        # 应用图标
│   │   └── sensitive_words/ # 敏感词库
│   ├── db.json             # 用户数据
│   └── users.json          # 用户信息
├── gui/                    # 前端代码
│   ├── src/                # Vue.js源码
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面视图
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # 状态管理
│   │   ├── assets/         # 静态资源
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 入口文件
│   ├── public/             # 公共资源
│   ├── package.json        # 项目配置
│   ├── vue.config.js       # Vue配置
│   └── start.bat           # 启动脚本
├── docs/                   # 文档目录
│   ├── api-documentation.md # API文档
│   ├── user-manual.md      # 用户手册
│   ├── technical-architecture.md # 技术架构
│   ├── development-guide.md # 开发指南
│   └── faq.md              # 常见问题
├── pictures/               # 项目图片
├── README.md              # 项目说明
└── .gitignore             # Git忽略文件
```

### 代码组织原则

1. **模块化**: 按功能划分模块，保持模块独立性
2. **分层架构**: 遵循MVC模式，分离业务逻辑和界面
3. **配置分离**: 将配置信息与代码分离
4. **资源管理**: 统一管理静态资源和配置文件

## 开发规范

### Python代码规范

#### 代码格式
```python
# 导入顺序
import os
import sys
import math
import threading
import subprocess
import time

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer

# 函数定义
def function_name(param1, param2):
    """
    函数文档字符串
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Returns:
        返回值说明
    """
    # 函数实现
    result = param1 + param2
    return result

# 类定义
class ClassName:
    """类文档字符串"""
    
    def __init__(self):
        """初始化方法"""
        self.property = None
    
    def method_name(self):
        """方法文档字符串"""
        pass
```

#### 注释规范
```python
# 单行注释：使用#，后面跟一个空格
def calculate_distance(point1, point2):
    # 计算两点之间的欧几里得距离
    dx = point2.x() - point1.x()
    dy = point2.y() - point1.y()
    return math.sqrt(dx**2 + dy**2)

# 多行注释：使用三引号
"""
这是一个多行注释
可以包含多行内容
用于复杂逻辑的说明
"""

# 函数文档字符串
def complex_function():
    """
    复杂函数的详细说明
    
    这个函数实现了以下功能：
    1. 功能1
    2. 功能2
    3. 功能3
    
    Returns:
        dict: 包含处理结果的字典
    """
    pass
```

### JavaScript/Vue.js代码规范

#### 命名规范
```javascript
// 组件名：使用PascalCase
export default {
  name: 'UserProfile'
}

// 变量名：使用camelCase
const userName = 'admin'
const isVisible = true

// 常量：使用UPPER_SNAKE_CASE
const API_BASE_URL = 'http://localhost:5000'

// 函数名：使用camelCase
function getUserInfo() {
  return {}
}
```

#### Vue组件规范
```vue
<template>
  <!-- 模板内容 -->
  <div class="component-name">
    <h1>{{ title }}</h1>
    <button @click="handleClick">点击</button>
  </div>
</template>

<script>
export default {
  name: 'ComponentName',
  props: {
    title: {
      type: String,
      required: true,
      default: ''
    }
  },
  data() {
    return {
      localData: null
    }
  },
  computed: {
    computedValue() {
      return this.localData
    }
  },
  methods: {
    handleClick() {
      this.$emit('click')
    }
  }
}
</script>

<style scoped>
.component-name {
  /* 样式定义 */
}
</style>
```

### Git提交规范

#### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 类型说明
- **feat**: 新功能
- **fix**: 修复bug
- **docs**: 文档更新
- **style**: 代码格式调整
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建过程或辅助工具的变动

#### 示例
```bash
# 新功能
git commit -m "feat(desktop): 添加宠物移动动画"

# 修复bug
git commit -m "fix(api): 修复用户登录验证问题"

# 文档更新
git commit -m "docs(readme): 更新安装说明"
```

## 开发流程

### 1. 功能开发流程

#### 需求分析
1. 理解功能需求
2. 设计技术方案
3. 确定接口规范
4. 制定开发计划

#### 开发实施
1. 创建功能分支
2. 实现核心功能
3. 编写单元测试
4. 进行代码审查

#### 测试验证
1. 功能测试
2. 集成测试
3. 性能测试
4. 用户验收测试

#### 部署上线
1. 合并到主分支
2. 构建生产版本
3. 部署到服务器
4. 监控运行状态

### 2. 分支管理

#### 分支策略
```
main (主分支)
├── develop (开发分支)
│   ├── feature/user-login (功能分支)
│   ├── feature/ai-continuation (功能分支)
│   └── hotfix/critical-bug (热修复分支)
└── release/v1.2.0 (发布分支)
```

#### 分支命名规范
- **功能分支**: `feature/功能名称`
- **修复分支**: `fix/问题描述`
- **热修复分支**: `hotfix/紧急问题`
- **发布分支**: `release/版本号`

### 3. 代码审查

#### 审查要点
1. **代码质量**: 代码可读性、可维护性
2. **功能正确性**: 功能实现是否符合需求
3. **性能影响**: 是否影响系统性能
4. **安全性**: 是否存在安全漏洞
5. **测试覆盖**: 是否有足够的测试用例

#### 审查流程
1. 开发者提交Pull Request
2. 自动检查（CI/CD）
3. 代码审查员审查
4. 修改反馈问题
5. 审查通过合并

## 调试指南

### 后端调试

#### 日志调试
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 使用日志
logger.debug('调试信息')
logger.info('一般信息')
logger.warning('警告信息')
logger.error('错误信息')
```

#### Flask调试
```python
from flask import Flask

app = Flask(__name__)

# 开启调试模式
app.run(debug=True, host='0.0.0.0', port=5000)
```

#### PyQt6调试
```python
# 启用Qt调试信息
import os
os.environ['QT_LOGGING_RULES'] = '*.debug=true;qt.*.debug=false'

# 使用QDebug
from PyQt6.QtCore import QDebug
qDebug() << "调试信息"
```

### 前端调试

#### Vue.js调试
```javascript
// 使用Vue DevTools
// 安装Vue DevTools浏览器扩展

// 使用console调试
console.log('调试信息')
console.warn('警告信息')
console.error('错误信息')

// 使用debugger断点
debugger;
```

#### 网络请求调试
```javascript
// 使用axios拦截器
axios.interceptors.request.use(config => {
  console.log('请求配置:', config)
  return config
})

axios.interceptors.response.use(response => {
  console.log('响应数据:', response)
  return response
})
```

### 常见调试技巧

#### 1. 断点调试
```python
# Python断点
import pdb
pdb.set_trace()

# 或者使用breakpoint() (Python 3.7+)
breakpoint()
```

#### 2. 性能分析
```python
import time
import cProfile

# 时间测量
start_time = time.time()
# 执行代码
end_time = time.time()
print(f"执行时间: {end_time - start_time}秒")

# 性能分析
def profile_function():
    # 要分析的函数
    pass

cProfile.run('profile_function()')
```

#### 3. 内存分析
```python
import tracemalloc

# 开始内存跟踪
tracemalloc.start()

# 执行代码
# ...

# 获取内存使用情况
current, peak = tracemalloc.get_traced_memory()
print(f"当前内存使用: {current / 1024 / 1024:.1f} MB")
print(f"峰值内存使用: {peak / 1024 / 1024:.1f} MB")
```

## 测试指南

### 单元测试

#### Python测试 (pytest)
```python
# test_main.py
import pytest
from backend.main import DesktopPet

class TestDesktopPet:
    def test_initialization(self):
        """测试桌面宠物初始化"""
        pet = DesktopPet()
        assert pet.scale == 2.0
        assert pet.move_interval == 5000
    
    def test_scale_update(self):
        """测试缩放比例更新"""
        pet = DesktopPet()
        original_size = pet.size()
        pet.update_scale(3.0)
        assert pet.scale == 3.0
        assert pet.size() != original_size
```

#### JavaScript测试 (Jest)
```javascript
// test/component.test.js
import { mount } from '@vue/test-utils'
import UserLogin from '@/components/UserLogin.vue'

describe('UserLogin', () => {
  test('renders login form', () => {
    const wrapper = mount(UserLogin)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
  })
  
  test('emits login event', async () => {
    const wrapper = mount(UserLogin)
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('login')).toBeTruthy()
  })
})
```

### 集成测试

#### API测试
```python
# test_api.py
import requests
import pytest

class TestAPI:
    def test_connection(self):
        """测试API连接"""
        response = requests.get('http://localhost:5000/api/ConnectTest')
        assert response.status_code == 200
        assert response.text == '服务端连接正常'
    
    def test_user_login(self):
        """测试用户登录"""
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = requests.post('http://localhost:5000/api/UserLogin', json=data)
        assert response.status_code == 200
        result = response.json()
        assert 'status' in result
```

### 端到端测试

#### 使用Selenium
```python
# test_e2e.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestE2E:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080')
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_user_login_flow(self):
        """测试用户登录流程"""
        # 输入用户名
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('test_user')
        
        # 输入密码
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys('test_password')
        
        # 点击登录按钮
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
        login_button.click()
        
        # 等待登录成功
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'dashboard'))
        )
        
        # 验证登录成功
        assert 'dashboard' in self.driver.current_url
```

## 部署指南

### 开发环境部署

#### 后端部署
```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 启动Flask服务
python Api.py

# 3. 启动桌面宠物
python main.py
```

#### 前端部署
```bash
# 1. 安装依赖
cd gui
npm install

# 2. 启动开发服务器
npm run serve

# 3. 构建生产版本
npm run build
```

### 生产环境部署

#### Docker部署
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "Api.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
  
  frontend:
    build: ./gui
    ports:
      - "80:80"
    depends_on:
      - backend
```

#### 服务器部署
```bash
# 1. 安装系统依赖
sudo apt update
sudo apt install python3 python3-pip nginx

# 2. 部署后端
cd backend
pip3 install -r requirements.txt
sudo systemctl enable flask-app
sudo systemctl start flask-app

# 3. 配置Nginx
sudo nano /etc/nginx/sites-available/flask-app
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 监控和维护

#### 日志管理
```python
# 配置日志轮转
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
```

#### 性能监控
```python
# 使用Flask-Monitoring
from flask_monitoring import Monitor

monitor = Monitor(app)
```

## 问题报告

### Bug报告模板
```
**Bug描述**
简要描述bug的现象

**重现步骤**
1. 步骤1
2. 步骤2
3. 步骤3

**期望行为**
描述期望的正确行为

**实际行为**
描述实际发生的错误行为

**环境信息**
- 操作系统: 
- Python版本: 
- 浏览器版本: 
- 其他相关信息:

**附加信息**
截图、日志文件等
```

### 功能请求模板
```
**功能描述**
详细描述新功能的需求

**使用场景**
描述功能的使用场景

**实现建议**
如果有实现建议，请提供

**优先级**
高/中/低
```

---
