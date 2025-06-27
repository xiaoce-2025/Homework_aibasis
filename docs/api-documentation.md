# API 文档

## 概述

严小希AI助手提供RESTful API接口，支持AI文本处理、用户认证、OCR识别等功能。所有API都基于Flask框架构建，支持跨域请求。

**基础URL**: `http://localhost:5000`

**内容类型**: `application/json`

## 认证

目前API使用简单的用户名密码认证，通过POST请求发送JSON格式的认证信息。

## 通用响应格式

所有API响应都遵循以下格式：

```json
{
  "status": "success|error",
  "message": "响应消息",
  "data": {} // 具体数据（可选）
}
```

## API 接口列表

### 1. 连接测试

**接口**: `GET /api/ConnectTest`

**描述**: 测试服务器连接状态

**请求参数**: 无

**响应示例**:
```
服务端连接正常
```

---

### 2. 用户认证

#### 2.1 用户登录

**接口**: `POST /api/UserLogin`

**描述**: 用户登录验证

**请求参数**:
```json
{
  "username": "用户名",
  "password": "密码"
}
```

**响应示例**:
```json
{
  "status": "success",
  "message": "登录成功",
  "user": {
    "username": "用户名",
    "id": "用户ID"
  }
}
```

#### 2.2 用户注册

**接口**: `POST /api/UserSignUp`

**描述**: 新用户注册

**请求参数**:
```json
{
  "username": "用户名",
  "password": "密码",
  "email": "邮箱地址"
}
```

**响应示例**:
```json
{
  "status": "success",
  "message": "注册成功"
}
```

---

### 3. AI文本处理

#### 3.1 AI文本续写

**接口**: `POST /api/submit`

**描述**: 基于输入文本进行AI续写

**请求参数**:
```json
{
  "text": "原始文本内容",
  "style": "续写风格（可选）",
  "length": "期望长度（可选）",
  "tone": "语气风格（可选）"
}
```

**响应示例**:
```json
{
  "status": "success",
  "message": "提交建议已返回",
  "new_suggestions": [
    {
      "id": "建议ID",
      "content": "续写内容",
      "score": 0.95
    }
  ]
}
```

#### 3.2 AI文本润色

**接口**: `POST /api/AIPolish`

**描述**: 对文本进行润色和优化

**请求参数**:
```json
{
  "text": "需要润色的文本",
  "style": "润色风格（可选）",
  "level": "润色程度（可选）"
}
```

**响应示例**:
```json
{
  "status": "success",
  "message": "润色结果已返回",
  "polishedText": "润色后的文本内容"
}
```

#### 3.3 AI智能摘抄

**接口**: `POST /api/AITextExtracts`

**描述**: 自动提取文章重点内容

**请求参数**:
```json
{
  "text": "原文内容",
  "extract_type": "摘抄类型（summary|key_points|quotes）",
  "max_length": "最大长度（可选）"
}
```

**响应示例**:
```json
{
  "status": "success",
  "message": "提交建议已返回",
  "new_suggestions": [
    {
      "type": "摘要",
      "content": "提取的重点内容",
      "importance": 0.9
    }
  ]
}
```

---

### 4. OCR文字识别

#### 4.1 图片OCR识别

**接口**: `POST /api/TextOCR`

**描述**: 识别图片中的文字内容

**请求参数**: 
- Content-Type: `multipart/form-data`
- 文件字段: `image` (图片文件)

**响应示例**:
```json
{
  "status": "success",
  "text": "识别出的文字内容",
  "confidence": 0.95,
  "language": "zh-CN"
}
```

---

### 5. 智能对话

#### 5.1 基础对话

**接口**: `POST /api/dialog`

**描述**: 与严小希进行文本对话

**请求参数**:
```json
{
  "message": "用户消息",
  "user_id": "用户ID（可选）",
  "context": "对话上下文（可选）"
}
```

**响应示例**:
```json
{
  "status": "success",
  "response": "严小希的回复",
  "emotion": "情感状态",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### 5.2 多模态对话

**接口**: `POST /api/dialog/multimodal`

**描述**: 支持图片和文本的多模态对话

**请求参数**:
```json
{
  "message": "用户消息",
  "image": "base64编码的图片（可选）",
  "user_id": "用户ID（可选）"
}
```

**响应示例**:
```json
{
  "status": "success",
  "response": "严小希的回复",
  "image_analysis": "图片分析结果",
  "emotion": "情感状态"
}
```

#### 5.3 对话分类

**接口**: `POST /api/dialog/classify`

**描述**: 对话意图分类

**请求参数**:
```json
{
  "message": "用户消息",
  "user_id": "用户ID（可选）"
}
```

**响应示例**:
```json
{
  "status": "success",
  "intent": "对话意图",
  "confidence": 0.95,
  "category": "分类结果"
}
```

---

### 6. 文本转语音

#### 6.1 AI朗读

**接口**: `POST /api/AIread`

**描述**: 将文本转换为语音

**请求参数**:
```json
{
  "text": "要转换的文本",
  "apiKey": "硅基流动API密钥",
  "voice": "语音类型（可选）"
}
```

**响应**: 
- Content-Type: `audio/mpeg`
- 返回音频文件流

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 错误响应示例

```json
{
  "status": "error",
  "message": "错误描述",
  "error_code": "ERROR_CODE",
  "details": "详细错误信息"
}
```

## 使用示例

### Python 示例

```python
import requests
import json

# 基础配置
BASE_URL = "http://localhost:5000"
headers = {"Content-Type": "application/json"}

# 用户登录
def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/api/UserLogin", 
                           json=data, headers=headers)
    return response.json()

# AI文本续写
def ai_continuation(text):
    data = {
        "text": text,
        "style": "creative",
        "length": 200
    }
    response = requests.post(f"{BASE_URL}/api/submit", 
                           json=data, headers=headers)
    return response.json()

# OCR识别
def ocr_recognition(image_path):
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"{BASE_URL}/api/TextOCR", files=files)
    return response.json()
```

### JavaScript 示例

```javascript
// 基础配置
const BASE_URL = 'http://localhost:5000';

// 用户登录
async function login(username, password) {
    const response = await fetch(`${BASE_URL}/api/UserLogin`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    return await response.json();
}

// AI对话
async function chat(message) {
    const response = await fetch(`${BASE_URL}/api/dialog`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message
        })
    });
    return await response.json();
}
```