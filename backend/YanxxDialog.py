from flask import request, Response, stream_with_context, json, jsonify
import requests
from openai import OpenAI
import json
import os
import re
import glob
from database import DataBase

# 初始化数据库实例
db = DataBase()

class SensitiveFilter:
    def __init__(self):
        self.words = set()
        self.load_from_directory("sensitive_words") 
    
    def load_from_directory(self, dir_path):
        """从目录加载所有敏感词文件"""
        if not os.path.exists(dir_path):
            print(f"警告: 敏感词目录不存在 - {dir_path}")
            return
        
        # 遍历目录中的所有txt文件
        for file_path in glob.glob(os.path.join(dir_path, "*.txt")):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            # 添加原始词和大小写变体
                            self.words.add(word)
                            self.words.add(word.lower())
                            self.words.add(word.upper())
                print(f"已加载敏感词文件: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"加载敏感词文件 {file_path} 失败: {str(e)}")
    
    def add_words(self, words):
        """添加额外敏感词"""
        self.words.update(words)
    
    def filter(self, text):
        """过滤文本中的敏感词"""
        if not self.words or not text:
            return text
            
        # 使用正则表达式实现高效匹配
        pattern = re.compile("|".join(map(re.escape, self.words)), re.IGNORECASE)
        return pattern.sub("", text)

# 初始化全局敏感词过滤器
sensitive_filter = SensitiveFilter()

class YanxxDialog:
    @staticmethod
    def filter_sensitive_content(content):
        """过滤敏感词并记录日志"""
        if not content:
            return content
            
        filtered = sensitive_filter.filter(content)
        
        # 记录过滤日志
        if filtered != content:
            # 简略日志，避免输出过长内容
            orig_preview = content[:50] + ("..." if len(content) > 50 else "")
            filtered_preview = filtered[:50] + ("..." if len(filtered) > 50 else "")
            print(f"[敏感词过滤] 原始内容: {orig_preview} -> 过滤后: {filtered_preview}")
        
        return filtered

    @staticmethod
    def AI_Yanxx_dialog(InputData, isClassify=False):
        # 1. 敏感词过滤
        # 过滤历史消息
        for msg in InputData['content']:
            msg['content'] = YanxxDialog.filter_sensitive_content(msg['content'])
        
        # 过滤当前请求
        filtered_request = YanxxDialog.filter_sensitive_content(InputData['ContentRequest'])
        
        # 模型关键信息齐全
        if not (InputData['config']['apiKey'] and InputData['config']['apiUrl'] and InputData['config']['ModelName']):
            return jsonify({"error": "配置错误: 缺少API参数"})

        # 模型温度参数在0-2
        if InputData['config']['ModelTemperature'] < 0 or InputData['config']['ModelTemperature'] > 2:
            InputData['config']['ModelTemperature'] = 1

        # 2. 构建消息列表
        # 获取知识库信息
        if not isClassify:
            knowledge_base_info = {
                "自我介绍": db.get("严小希自我介绍"),
                "发型": db.get("严小希发型"),
                "眼睛": db.get("严小希眼睛"),
                "服装": db.get("严小希服装"),
                "性格": db.get("严小希性格"),
                "作品": db.get("严小希作品")
            }
            knowledge_base_str = ""
            for key, value in knowledge_base_info.items():
                if value:
                    knowledge_base_str += f"{key}: {value}\n"
            messages = [
            {"role": "system", "content": f"你是严小希，用户将和你对话。以下是关于你(严小希)的一些信息：\n{knowledge_base_str}"}
            ]
        if isClassify:
            messages = [
                {"role": "system", "content": """
            用户将提供和你的多轮对话信息，请判断用户此轮对话是否有"文本续写"、"文本润色"、"摘抄"相关的需求，并将有需求的选项返回true,否则返回false

            示例输入：
            今天语文老师留了好多的摘抄作业，根本写不完啊！

            示例JSON输出：
            {
                "TextContinuation": false,
                "TextPolishment": false,
                "Extraction": true,
            }
            """}
            ]
        
        # 添加过滤后的历史消息
        for msg in InputData['content']:
            role = "user" if msg['sender'] == 'user' else "assistant"
            messages.append({
                "role": role,
                "content": msg['content']
            })
            
        # 添加过滤后的当前请求
        messages.append({
            "role": "user",
            "content": filtered_request
        })
        
        print("[server]提交对话内容:", json.dumps(messages, ensure_ascii=False))
        
        # 分类器api
        if isClassify:
            client = OpenAI(
                api_key=InputData['config']['apiKey'],
                base_url=InputData['config']['apiUrl'],
            )
            response = client.chat.completions.create(
                model=InputData['config']['ModelName'],
                messages=messages,
                temperature=InputData['config']['ModelTemperature'],
                response_format={
                    'type': 'json_object'
                }
            )
            response_content = response.choices[0].message.content
            if response_content:
                choose_response = json.loads(response_content)
                if not isinstance(choose_response, dict):
                    choose_response = {
                        "TextContinuation": False,
                        "TextPolishment": False,
                        "Extraction": False
                    }
            else:
                choose_response = {
                    "TextContinuation": False,
                    "TextPolishment": False,
                    "Extraction": False
                }
            return jsonify(choose_response)
        # 正常对话api
        def generate():
            try:
                # DeepSeek API配置
                url = InputData['config']['apiUrl'] + "/chat/completions"
                headers = {
                    "Authorization": f"Bearer {InputData['config']['apiKey']}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": InputData['config']['ModelName'],
                    "messages": messages,
                    "stream": True,
                    "temperature": InputData['config']['ModelTemperature']
                }
                
                # 发送流式请求
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    stream=True
                )
                
                # 检查响应状态
                if response.status_code != 200:
                    try:
                        error_info = response.json().get("error", {})
                        error_msg = error_info.get("message", "未知错误")
                        error_type = error_info.get("type", "API错误")
                        error_data = f"{error_type}: {error_msg}"
                    except:
                        error_data = response.text[:200]
                    
                    error_message = f"API错误 {response.status_code}: {error_data}"
                    error_json = json.dumps({"error": error_message})
                    yield f"data: {error_json}\n\n"
                    return
                
                # 处理流式数据
                for chunk in response.iter_lines():
                    if not chunk:
                        continue
                        
                    chunk_str = chunk.decode('utf-8')
                    if not chunk_str.startswith('data:'):
                        chunk_str = f"data: {chunk_str}"
                        
                    if chunk_str.strip() == 'data: [DONE]':
                        if hasattr(InputData, 'choose_response') and InputData['choose_response']:
                            choose_response = InputData['choose_response']
                            if choose_response.get("TextContinuation", False):
                                yield "data: [AIContinuation]\n\n"
                            if choose_response.get("TextPolishment", False):
                                yield "data: [AIPolishment]\n\n"
                            if choose_response.get("Extraction", False):
                                yield "data: [AIExtraction]\n\n"
                        yield "data: [DONE]\n\n"
                        break
                        
                    if chunk_str.startswith('data:') and 'error' not in chunk_str:
                        try:
                            data = json.loads(chunk_str[6:].strip())
                            content_chunk = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            
                            # 对输出内容也进行敏感词过滤
                            filtered_chunk = YanxxDialog.filter_sensitive_content(content_chunk)
                            if filtered_chunk:
                                yield f"data: {filtered_chunk}\n\n"
                        except:
                            yield f"{chunk_str}\n\n"
                    else:
                        yield f"{chunk_str}\n\n"
            
            except Exception as e:
                error_json = json.dumps({"error": f"AI服务错误: {str(e)}"})
                yield f"data: {error_json}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )


    @staticmethod
    def AI_Yanxx_dialog_multimodal(InputData, isClassify=False):
        """处理包含图片的多模态对话"""
        # 1. 敏感词过滤
        # 过滤历史消息
        for msg in InputData['content']:
            msg['content'] = YanxxDialog.filter_sensitive_content(msg['content'])
        
        # 过滤当前请求
        filtered_request = YanxxDialog.filter_sensitive_content(InputData['ContentRequest'])
        
        # 模型关键信息齐全
        if not (InputData['config']['apiKey'] and InputData['config']['apiUrl'] and InputData['config']['ModelName']):
            return jsonify({"error": "配置错误: 缺少API参数"})

        # 模型温度参数在0-2
        if InputData['config']['ModelTemperature'] < 0 or InputData['config']['ModelTemperature'] > 2:
            InputData['config']['ModelTemperature'] = 1

        # 2. 构建消息列表
        # 获取知识库信息
        if not isClassify:
            knowledge_base_info = {
                "自我介绍": db.get("严小希自我介绍"),
                "发型": db.get("严小希发型"),
                "眼睛": db.get("严小希眼睛"),
                "服装": db.get("严小希服装"),
                "性格": db.get("严小希性格"),
                "作品": db.get("严小希作品")
            }
            knowledge_base_str = ""
            for key, value in knowledge_base_info.items():
                if value:
                    knowledge_base_str += f"{key}: {value}\n"
            messages = [
            {"role": "system", "content": f"你是严小希，用户将和你对话。以下是关于你(严小希)的一些信息：\n{knowledge_base_str}"}
            ]
        if isClassify:
            messages = [
                {"role": "system", "content": """
            用户将提供和你的多轮对话信息，请判断用户此轮对话是否有"文本续写"、"文本润色"、"摘抄"相关的需求，并将有需求的选项返回true,否则返回false

            示例输入：
            今天语文老师留了好多的摘抄作业，根本写不完啊！

            示例JSON输出：
            {
                "TextContinuation": false,
                "TextPolishment": false,
                "Extraction": true,
            }
            """}
            ]
        
        # 添加过滤后的历史消息
        for msg in InputData['content']:
            role = "user" if msg['sender'] == 'user' else "assistant"
            messages.append({
                "role": role,
                "content": msg['content']
            })
            
        # 添加过滤后的当前请求（包含图片）
        if InputData.get('image'):
            # 如果有图片，使用字符串格式描述图片
            image_data = InputData['image']
            image_description = f"[图片: {image_data['name']}]"
            combined_content = f"{filtered_request}\n{image_description}"
            messages.append({
                "role": "user",
                "content": combined_content
            })
        else:
            # 纯文本消息
            messages.append({
                "role": "user",
                "content": filtered_request
            })
        
        print("[server]提交多模态对话内容:", json.dumps(messages, ensure_ascii=False))
        
        # 分类器api
        if isClassify:
            client = OpenAI(
                api_key=InputData['config']['apiKey'],
                base_url=InputData['config']['apiUrl'],
            )
            response = client.chat.completions.create(
                model=InputData['config']['ModelName'],
                messages=messages,
                temperature=InputData['config']['ModelTemperature'],
                response_format={
                    'type': 'json_object'
                }
            )
            response_content = response.choices[0].message.content
            if response_content:
                choose_response = json.loads(response_content)
                if not isinstance(choose_response, dict):
                    choose_response = {
                        "TextContinuation": False,
                        "TextPolishment": False,
                        "Extraction": False
                    }
            else:
                choose_response = {
                    "TextContinuation": False,
                    "TextPolishment": False,
                    "Extraction": False
                }
            return jsonify(choose_response)

        # 对话api
        # 创建生成器函数用于流式响应
        def generate():
            try:
                # DeepSeek API配置
                url = InputData['config']['apiUrl'] + "/chat/completions"
                headers = {
                    "Authorization": f"Bearer {InputData['config']['apiKey']}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": InputData['config']['ModelName'],
                    "messages": messages,
                    "stream": True,
                    "temperature": InputData['config']['ModelTemperature']
                }
                
                # 发送流式请求
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    stream=True
                )
                
                # 检查响应状态
                if response.status_code != 200:
                    try:
                        error_info = response.json().get("error", {})
                        error_msg = error_info.get("message", "未知错误")
                        error_type = error_info.get("type", "API错误")
                        error_data = f"{error_type}: {error_msg}"
                    except:
                        error_data = response.text[:200]
                    
                    error_message = f"API错误 {response.status_code}: {error_data}"
                    error_json = json.dumps({"error": error_message})
                    yield f"data: {error_json}\n\n"
                    return
                
                # 处理流式数据
                for chunk in response.iter_lines():
                    if not chunk:
                        continue
                        
                    chunk_str = chunk.decode('utf-8')
                    if not chunk_str.startswith('data:'):
                        chunk_str = f"data: {chunk_str}"
                        
                    if chunk_str.strip() == 'data: [DONE]':
                        if hasattr(InputData, 'choose_response') and InputData['choose_response']:
                            choose_response = InputData['choose_response']
                            if choose_response.get("TextContinuation", False):
                                yield "data: [AIContinuation]\n\n"
                            if choose_response.get("TextPolishment", False):
                                yield "data: [AIPolishment]\n\n"
                            if choose_response.get("Extraction", False):
                                yield "data: [AIExtraction]\n\n"
                        yield "data: [DONE]\n\n"
                        break
                        
                    if chunk_str.startswith('data:') and 'error' not in chunk_str:
                        try:
                            data = json.loads(chunk_str[6:].strip())
                            content_chunk = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            
                            # 对输出内容也进行敏感词过滤
                            filtered_chunk = YanxxDialog.filter_sensitive_content(content_chunk)
                            if filtered_chunk:
                                yield f"data: {filtered_chunk}\n\n"
                        except:
                            yield f"{chunk_str}\n\n"
                    else:
                        yield f"{chunk_str}\n\n"
            
            except Exception as e:
                error_json = json.dumps({"error": f"AI服务错误: {str(e)}"})
                yield f"data: {error_json}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )

        # 多模态对话api
        # 创建生成器函数用于流式响应
        def generate_multimodal():
            try:
                # 多模态API配置
                url = InputData['config']['apiUrl'] + "/chat/completions"
                headers = {
                    "Authorization": f"Bearer {InputData['config']['apiKey']}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": InputData['config']['ModelName'],
                    "messages": messages,
                    "stream": True,
                    "temperature": InputData['config']['ModelTemperature']
                }
                
                # 发送流式请求
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    stream=True
                )
                
                # 检查响应状态
                if response.status_code != 200:
                    try:
                        error_info = response.json().get("error", {})
                        error_msg = error_info.get("message", "未知错误")
                        error_type = error_info.get("type", "API错误")
                        error_data = f"{error_type}: {error_msg}"
                    except:
                        error_data = response.text[:200]
                    
                    error_message = f"API错误 {response.status_code}: {error_data}"
                    error_json = json.dumps({"error": error_message})
                    yield f"data: {error_json}\n\n"
                    return
                
                # 处理流式数据
                for chunk in response.iter_lines():
                    if not chunk:
                        continue
                        
                    chunk_str = chunk.decode('utf-8')
                    if not chunk_str.startswith('data:'):
                        chunk_str = f"data: {chunk_str}"
                        
                    if chunk_str.strip() == 'data: [DONE]':
                        if hasattr(InputData, 'choose_response') and InputData['choose_response']:
                            choose_response = InputData['choose_response']
                            if choose_response.get("TextContinuation", False):
                                yield "data: [AIContinuation]\n\n"
                            if choose_response.get("TextPolishment", False):
                                yield "data: [AIPolishment]\n\n"
                            if choose_response.get("Extraction", False):
                                yield "data: [AIExtraction]\n\n"
                        yield "data: [DONE]\n\n"
                        break
                        
                    if chunk_str.startswith('data:') and 'error' not in chunk_str:
                        try:
                            data = json.loads(chunk_str[6:].strip())
                            content_chunk = data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            
                            # 对输出内容也进行敏感词过滤
                            filtered_chunk = YanxxDialog.filter_sensitive_content(content_chunk)
                            if filtered_chunk:
                                yield f"data: {filtered_chunk}\n\n"
                        except:
                            yield f"{chunk_str}\n\n"
                    else:
                        yield f"{chunk_str}\n\n"
            
            except Exception as e:
                error_json = json.dumps({"error": f"AI服务错误: {str(e)}"})
                yield f"data: {error_json}\n\n"
        
        return Response(
            stream_with_context(generate_multimodal()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )
