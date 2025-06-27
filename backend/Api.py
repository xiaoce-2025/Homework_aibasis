# -*- coding: utf-8 -*-
# 安装依赖：pip install flask flask-cors
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import requests


app = Flask(__name__)
CORS(app)  # 解决跨域问题


# 连接检测
@app.route('/api/ConnectTest', methods=['GET'])
def connection_test():
    return "服务端连接正常"


# 续写api
from AIContinuation import ContinueWrite
@app.route('/api/submit', methods=['POST'])
def handle_submit():
    """处理用户输入"""
    data = request.json
    print(f"[server]收到续写提交:\n", data)
    # 这里可以添加业务处理逻辑（如保存到数据库、调用AI生成等）


    # 获取续写建议（返回字典）
    output_data = ContinueWrite.AI_Continuation_Suggest(data)
    Re_data = jsonify({
        "status": "success",
        "message": "提交建议已返回",
        "new_suggestions": output_data  # 可以返回新的候选建议
    })
    return Re_data

# 登录验证
from Auth import Auth
@app.route('/api/UserLogin', methods=['POST'])
def user_login():
    data = request.json
    print(f"[server]收到登录请求:\n", data)
    checked = Auth.login(data)
    return checked

@app.route('/api/UserSignUp', methods=['POST'])
def user_signup():
    data = request.json
    print(f"[server]收到注册请求:\n", data)
    checked = Auth.SignUp(data)
    return checked


# 获取历史记录列表(待完成)


# 摘抄api
from AITextExtracts import AutoExtract
@app.route('/api/AITextExtracts', methods=['POST'])
def AI_text_extract():
    """处理用户输入"""
    data = request.json
    print(f"[server]收到摘抄提交:\n", data)
    # 这里可以添加业务处理逻辑（如保存到数据库、调用AI生成等）

    # 获取摘抄内容（返回字典）
    output_data = AutoExtract.AI_Auto_Extract(data)
    # output_data = []
    Re_data = jsonify({
        "status": "success",
        "message": "提交建议已返回",
        "new_suggestions": output_data # 返回摘抄内容
    })
    return Re_data


# 图片OCRapi
from TextOCR import TextOCR
@app.route('/api/TextOCR', methods=['POST'])
def AI_TextOCR():
    """处理用户输入"""
    data = request
    print(f"[server]收到图片OCR提交")
    # 这里可以添加业务处理逻辑（如保存到数据库、调用AI生成等）

    # 获取ocr结果并返回
    Re_data = TextOCR.ocr_processing(data)
    return Re_data


# 对话api
from YanxxDialog import YanxxDialog
@app.route('/api/dialog', methods=['POST'])
def AI_Dialog():
    """处理用户输入"""
    data = request.json
    print(f"[server]收到严小希对话请求提交:\n", data)
    # 这里可以添加业务处理逻辑（如保存到数据库、调用AI生成等）

    # 获取对话
    return YanxxDialog.AI_Yanxx_dialog(data,False)

@app.route('/api/dialog/multimodal', methods=['POST'])
def AI_Dialog_Multimodal():
    """处理包含图片的多模态对话请求"""
    data = request.json
    print(f"[server]收到严小希多模态对话请求提交:\n", data)
    
    # 调用多模态对话处理
    return YanxxDialog.AI_Yanxx_dialog_multimodal(data, False)

@app.route('/api/dialog/classify', methods=['POST'])
def AI_Dialog_classify():
    """处理用户输入"""
    data = request.json
    print(f"[server]收到严小希对话请求提交:\n", data)
    # 这里可以添加业务处理逻辑（如保存到数据库、调用AI生成等）

    # 获取对话
    response = YanxxDialog.AI_Yanxx_dialog(data,True)
    print("分类器返回结果：",response)
    return response


# 润色api
from AIPolishment import PolishWrite
@app.route('/api/AIPolish', methods=['POST'])
def AI_Polish():
    """处理用户输入"""
    data = request.json
    print(f"[server]收到续写提交:\n", data)
    # 这里可以添加业务处理逻辑（如保存到数据库、调用AI生成等）


    # 获取润色后文本
    output_data = PolishWrite.AI_Polishment(data)
    Re_data = jsonify({
        "status": "success",
        "message": "润色结果已返回",
        "polishedText": output_data
    })
    return Re_data


# 文本转语音api
# 硅基流动API配置
SILICON_FLOW_API_URL = "https://api.siliconflow.cn/v1/audio/speech"

@app.route('/api/AIread', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        if data is None:
            return jsonify({"status": "error", "message": "无效的请求数据"}), 400
            
        text = data.get('text', '')
        SILICON_FLOW_API_KEY = data.get('apiKey','')

        print(SILICON_FLOW_API_URL,SILICON_FLOW_API_KEY)
        
        if not text:
            return jsonify({"status": "error", "message": "缺少文本内容"}), 400
        
        # 删除括号内的内容
        import re
        text = re.sub(r'\([^)]*\)', '', text)
        
        # 准备请求硅基流动API
        payload = {
            "model": "FunAudioLLM/CosyVoice2-0.5B",
            "input": text,
            "voice": "FunAudioLLM/CosyVoice2-0.5B:diana"
        }
        
        headers = {
            "Authorization": f"Bearer {SILICON_FLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 转发请求到硅基流动API
        response = requests.post(SILICON_FLOW_API_URL, json=payload, headers=headers)
        
        if response.status_code != 200:
            return jsonify({
                "status": "error", 
                "message": f"API请求失败: {response.status_code}",
                "details": response.text
            }), 500
        
        # 将API响应直接返回给客户端
        return Response(
            response=response.content,
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

