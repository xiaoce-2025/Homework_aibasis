from openai import OpenAI

'''
InputData{
    config: {
        ModelName: ModelName,
        apiKey: apiKey,
        apiUrl: apiUrl,
        ModelTemperature: ModelTemperature,
    },
    content: originalText.value,
    polishStrength: polishStrength.value,
    writingStyle: writingStyle.value,
    additionalRequirements: additionalRequirements.value,
    language: language.value
}      
'''
class PolishWrite:
    #装饰器定义静态变量
    @staticmethod
    def AI_Polishment(InputData):
        # 模型关键信息齐全
        if (not (InputData['config']['apiKey'] and InputData['config']['apiUrl'] and InputData['config']['ModelName'])):
            return []

        # 模型温度参数在0-2
        if (InputData['config']['ModelTemperature'] < 0 or InputData['config']['ModelTemperature'] > 2):
            InputData['config']['ModelTemperature'] = 1

        client = OpenAI(
            api_key=InputData['config']['apiKey'],
            base_url=InputData['config']['apiUrl'],
        )

        system_prompt = """
        用户将提供一段文本，请对这段文本进行润色。直接输出润色后的文本即可。
        """
        # 输入事件信息
        user_prompt = ""
        if (InputData['polishStrength'] == "light"):
            user_prompt += "润色强度：轻度优化 || "
        elif (InputData['polishStrength'] == "medium"):
            user_prompt += "润色强度：中度改写 || "
        elif (InputData['polishStrength'] == "aggressive"):
            user_prompt += "润色强度：全面改写 || "
        
        if (InputData['writingStyle'] == "formal"):
            user_prompt += "目标风格：正式书面 || "
        elif (InputData['writingStyle'] == "academic"):
            user_prompt += "目标风格：学术论文 || "
        elif (InputData['writingStyle'] == "creative"):
            user_prompt += "目标风格：创意写作 || "
        elif (InputData['writingStyle'] == "business"):
            user_prompt += "目标风格：商务沟通 || "

        if (InputData['language'] == "zh-CN"):
            user_prompt += "目标语言：简体中文 || "
        elif (InputData['language'] == "zh-TW"):
            user_prompt += "目标语言：繁体中文 || "
        elif (InputData['language'] == "en-US"):
            user_prompt += "目标语言：英文 || "
        elif (InputData['language'] == "ja-JP"):
            user_prompt += "目标语言：日文 || "
        elif (InputData['language'] == "wyw"):
            user_prompt += "目标语言：文言文 || "

        if (InputData['additionalRequirements']):
            user_prompt += "要求："
            user_prompt += InputData['additionalRequirements']
            user_prompt += " || "
        user_prompt += "待润色内容："
        user_prompt += InputData['content']

        print("[server]已向远程服务器提交润色任务,提交内容：\n", user_prompt)

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = client.chat.completions.create(
            model=InputData['config']['ModelName'],
            messages=messages,
            temperature=InputData['config']['ModelTemperature'],
        )
        # 解析并打印JSON输出
        response = response.choices[0].message.content
        print("[server]AI润色结果已返回:\n", response)
        return response
