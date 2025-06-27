# 严小希AI助手 - 智能桌面宠物与文本处理系统

这是一个AI基础的大作业

我是*严小希*，期待你的到来

我是*马涵希*，期待你的到来

<div align="center">

![严小希](pictures/yanxx.png)

**一个集成了桌面宠物、AI文本处理、OCR识别和智能对话的综合性AI助手系统**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.2+-green.svg)](https://vuejs.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

</div>

## 📖 项目简介

严小希AI助手是一个创新的桌面应用程序，结合了可爱的桌面宠物和强大的AI文本处理功能。系统包含一个基于PyQt6的桌面宠物"严小希"，以及一个基于Vue.js的Web界面，提供多种AI辅助功能。

### 🌟 核心特性

#### 🐾 桌面宠物功能
- **智能桌面宠物**：可爱的"严小希"角色，支持动画和交互
- **随机移动**：宠物会在屏幕上智能移动，增加趣味性
- **自定义设置**：支持缩放、移动间隔、颜色等个性化设置
- **右键菜单**：快速访问各种功能
- **系统托盘**：后台运行，不占用桌面空间

#### 🤖 AI文本处理功能
- **AI文本续写**：基于上下文智能续写文章
- **文本润色**：提升文本质量和表达效果
- **智能摘抄**：自动提取文章重点内容
- **OCR识别**：图片文字识别和提取
- **智能对话**：与严小希进行自然语言对话
- **文本朗读**：将文本转换为语音

#### 🎨 用户界面
- **现代化Web界面**：基于Vue.js和Element Plus
- **响应式设计**：适配不同屏幕尺寸
- **用户系统**：支持注册、登录和个人设置
- **历史记录**：保存用户操作历史
- **多模态交互**：支持文本和图片输入

## 🚀 快速开始

### 系统要求

- **操作系统**：Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**：3.8 或更高版本
- **Node.js**：16.0 或更高版本
- **内存**：至少 4GB RAM
- **存储空间**：至少 500MB 可用空间

### 安装步骤（用户）

#### 1. 克隆项目

```bash
git clone https://github.com/xiaoce-2025/aibasis_homework.git
cd aibasis_homework
```

#### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3. 启动系统
```bash
cd backend
python main.py
```

### 安装步骤（开发者）

#### 1. 克隆项目

```bash
git clone https://github.com/xiaoce-2025/aibasis_homework.git
cd aibasis_homework
```

#### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3. 安装前端依赖

```bash
cd ../gui
npm install
```

#### 4. 启动应用

**启动严小希**
```bash
cd backend
python main.py
```

**启动api服务端**
```bash
cd backend
python Api.py
```

**启动Web界面**
```bash
cd gui
npm run serve
```


### 配置说明

1. **API密钥配置**：在 `backend/config.py` 中配置相关AI服务的API密钥
2. **数据库配置**：系统使用JSON文件存储数据，无需额外数据库配置
3. **端口配置**：默认后端运行在5000端口，前端运行在8080端口

## 📚 详细文档

- [📖 用户手册](docs/user-manual.md) - 详细的使用指南
- [🔧 API文档](docs/api-documentation.md) - 完整的API接口说明
- [🏗️ 技术架构](docs/technical-architecture.md) - 系统架构和技术栈
- [👨‍💻 开发指南](docs/development-guide.md) - 开发者文档
- [🐛 常见问题](docs/faq.md) - 问题解答

## 🎯 功能演示

### 桌面宠物操作

1. **启动宠物**：运行 `python main.py` 启动桌面宠物
2. **移动宠物**：拖拽宠物到任意位置
3. **右键菜单**：右键点击宠物访问功能菜单
4. **设置调整**：通过设置菜单调整宠物外观和行为

### Web界面功能

1. **用户登录**：注册新账户或使用现有账户登录
2. **AI续写**：输入文本开头，AI自动续写后续内容
3. **文本润色**：上传文本，AI优化表达和语法
4. **OCR识别**：上传图片，自动识别文字内容
5. **智能对话**：与严小希进行自然语言交流

## 🏗️ 项目架构

```
aibasis_homework/
├── backend/                 # 后端服务
│   ├── main.py             # 桌面宠物主程序
│   ├── Api.py              # Flask API服务
│   ├── AIContinuation.py   # AI续写模块
│   ├── AIPolishment.py     # AI润色模块
│   ├── AITextExtracts.py   # AI摘抄模块
│   ├── TextOCR.py          # OCR识别模块
│   ├── YanxxDialog.py      # 智能对话模块
│   ├── Auth.py             # 用户认证模块
│   └── resources/          # 资源文件
├── gui/                    # 前端界面
│   ├── src/                # Vue.js源码
│   ├── public/             # 静态资源
│   └── package.json        # 依赖配置
├── docs/                   # 文档目录
└── README.md              # 项目说明
```


## 🙏 致谢

- **泡泡大人**：加入泡门，拥抱美好生活！正因为有您，我们才会创造出*严小希*这一可爱的角色
- **櫟染**：为我们提供了部分动画原画支持
- **辛勤付出的老师和助教们**
- **firefly1145141919810**和**xiaoce-2025**

## 更新日志
### Beta 1.0
更新日期：2025年4月21日

更新内容：
1. 完善了基础功能（ai续写，GUI导航、设置、首页等）
2. 支持了使用html的gui版本

### Beta 1.1
更新日期：2025年4月23日

更新内容：
1. 增加了登录和注册功能
2. 调整了GUI

### 看上去是终版
更新日期：2025年6月27日

更新内容：
1. 完成了全部内容
2. 修复了一些已知问题

*由于时间紧张，本版本尚未发布release，敬请谅解

---

<div align="center">

**让严小希陪伴你的每一天！** ✨

</div>



