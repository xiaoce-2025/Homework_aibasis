from openai import OpenAI
import json

'''
InputData{
    config: {
        ModelName: ModelName,
        apiKey: apiKey,
        apiUrl: apiUrl,
        maxToken: maxToken,
        ModelTemperature: ModelTemperature,
        generateNum: generateNum,
        generateTextNum: generateTextNum,
    },
    title: title.value,
    content: content.value,
    ContentRequest: ContentRequest.value,
    selectedStyles: selectedStyles.value, // 选中的风格标签
    plotOutline: plotOutline.value // 文章构思
}      
'''
class ContinueWrite:
    #装饰器定义静态变量
    @staticmethod
    def AI_Continuation_Suggest(InputData):
        # 模型关键信息齐全
        if (not (InputData['config']['apiKey'] and InputData['config']['apiUrl'] and InputData['config']['ModelName'])):
            return []

        # 模型温度参数在0-2
        if (InputData['config']['ModelTemperature'] < 0 or InputData['config']['ModelTemperature'] > 2):
            InputData['config']['ModelTemperature'] = 1

        # 模型maxtoken>1且为整数
        InputData['config']['maxToken'] = int(InputData['config']['maxToken'])
        if (InputData['config']['maxToken'] < 1):
            InputData['config']['maxToken'] = 4096

        # 生成数量为1-5的整数
        InputData['config']['generateNum'] = int(
            InputData['config']['generateNum'])
        if (InputData['config']['generateNum'] < 1 or InputData['config']['generateNum'] > 5):
            InputData['config']['generateNum'] = 3

        # 单次生成字数>1 <500
        InputData['config']['generateTextNum'] = int(
            InputData['config']['generateTextNum'])
        if (InputData['config']['generateTextNum'] < 1 or InputData['config']['generateTextNum'] > 500):
            InputData['config']['generateTextNum'] = 100

        client = OpenAI(
            api_key=InputData['config']['apiKey'],
            base_url=InputData['config']['apiUrl'],
        )

        # 风格标签映射
        style_mapping = {
            'romantic': '浪漫',
            'mysterious': '神秘',
            'humorous': '幽默',
            'melancholy': '忧郁',
            'exciting': '激动',
            'peaceful': '平静',
            'nostalgic': '怀旧',
            'optimistic': '乐观',
            'pessimistic': '悲观',
            'dramatic': '戏剧性',
            'realistic': '现实',
            'fantasy': '奇幻',
            'suspense': '悬疑',
            'warm': '温暖',
            'cold': '冷酷'
        }

        system_prompt = """
        用户将提供他写的文章的标题、写作要求、风格/情感标签、文章构思和已完成的部分。请帮助用户进行i种可能的续写（不要求文章结束，只要这段续写符合要求即可），每种可能的续写内容在x字左右。并以JSON格式输出。

        请根据用户选择的风格/情感标签来调整写作风格，根据文章构思来指导情节发展方向。

        示例输入：
        续写数量：3 || 续写字数：100字左右 || 文章标题：严小希的自我介绍 || 写作要求：写一个温馨的自我介绍 || 风格标签：温暖,幽默 || 文章构思：严小希接下来会介绍自己的兴趣爱好 || 文章内容：这里是严小希的自我介绍qwq。 你好呀，我叫严小希，是一位就读于人小附大的高三学生。简短的介绍后，严小希又埋头去做无穷无尽的物理卷子了呢。于是乎，就让我，严小希的好友xiaoce来接着替她介绍一下吧~ 严小希将在今年6月份参加高考并毕业，她一直梦想考入北京大学。在学校中，严小希以其阳光可爱、积极向上的性格在校园内外广受好评。她不仅学业优秀，还十分的可爱。

        示例JSON输出：
        {
            "Attemption1": "除了学习，严小希还有很多有趣的爱好呢！她特别喜欢画画，每当有空闲时间，她就会拿出画笔，在纸上描绘出美丽的风景。她的画作总是充满了温暖和希望，就像她的人一样。xiaoce笑着说："严小希的画真的很棒哦，每次看到都会让人心情变好呢！"",
            "Attemption2": "严小希还很喜欢音乐，特别是钢琴。虽然学习很忙，但她每天都会抽出一点时间来练习。她的琴声总是那么温柔，仿佛能抚平所有的烦恼。有时候，她还会为同学们弹奏一些轻松的小曲子，让大家在紧张的学习生活中找到一丝慰藉。",
            "Attemption3": "说到爱好，严小希还特别喜欢看书。她最喜欢的是那些充满温暖和正能量的故事，每次看完都会和朋友们分享自己的感受。她的书架上摆满了各种各样的书籍，从文学名著到科普读物，应有尽有。xiaoce经常说："和严小希聊天总是很有趣，因为她总能从书中找到很多有趣的话题呢！"",
        }
        """
        
        # 输入事件信息
        user_prompt = "生成数量："
        user_prompt += str(InputData['config']['generateNum'])
        user_prompt += " || 续写字数："
        user_prompt += str(InputData['config']['generateTextNum'])
        user_prompt += " || "
        
        if (InputData['title']):
            user_prompt += "文章标题："
            user_prompt += InputData['title']
            user_prompt += " || "
            
        if (InputData['ContentRequest']):
            user_prompt += "写作要求："
            user_prompt += InputData['ContentRequest']
            user_prompt += " || "
            
        # 添加风格标签
        if (InputData.get('selectedStyles') and len(InputData['selectedStyles']) > 0):
            style_labels = []
            for style in InputData['selectedStyles']:
                mapped_style = style_mapping.get(style, style)
                if mapped_style:
                    style_labels.append(mapped_style)
            if style_labels:
                user_prompt += "风格标签："
                user_prompt += ",".join(style_labels)
                user_prompt += " || "
            
        # 添加文章构思
        if (InputData.get('plotOutline') and InputData['plotOutline'].strip()):
            user_prompt += "文章构思："
            user_prompt += InputData['plotOutline']
            user_prompt += " || "

        user_prompt += "文章内容："
        user_prompt += InputData['content']

        print("[server]已向远程服务器提交续写任务,提交内容：\n", user_prompt)

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = client.chat.completions.create(
            model=InputData['config']['ModelName'],
            messages=messages,
            max_tokens=InputData['config']['maxToken'],
            temperature=InputData['config']['ModelTemperature'],
            response_format={
                'type': 'json_object'
            }
        )
        # 解析并打印JSON输出
        response_content = response.choices[0].message.content
        if response_content:
            parsed_response = json.loads(response_content)
            print("[server]AI续写建议已返回:\n", parsed_response)
            # 格式标准化
            # 构建结果列表
            result = []
            id = 0
            for key, text in parsed_response.items():
                id += 1
                result.append({"id": id, "text": text})
            # 返回处理后的字典
            return result
        else:
            print("[server]AI续写建议返回为空")
            return []
