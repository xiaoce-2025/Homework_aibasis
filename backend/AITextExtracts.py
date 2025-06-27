
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
        },
    text: inputText.value,
}
'''
class AutoExtract:
    #装饰器定义静态变量
    @staticmethod
    def AI_Auto_Extract(InputData):
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

        client = OpenAI(
            api_key=InputData['config']['apiKey'],
            base_url=InputData['config']['apiUrl'],
        )

        system_prompt = """
        用户将提供一段文本，请对这段文本进行摘抄，并对摘抄内容进行点评。摘抄你所有觉得比较好的内容，点评字数合适即可，按顺序输出原文文本和点评。并以JSON格式输出。

        示例输入：
        老人与海节选：大马林鱼开始快速地围着小渔船游动，将缆绳缠绕到了桅杆上，老人右手高举着钢叉，在它跃出水面的一瞬间，竭尽全力地向它的心脏掷去，一声哀鸣结束了大鱼的生命，它静静地浮在水面上……老人和大鱼一直相持到日落，双方已搏斗了两天一夜，老头不禁回想起年轻时在卡萨兰卡跟一个黑人比赛扳手的经历。一个鱼食送下四十英寸的深处，第二个鱼食送下七十五英寸的深处，第三个和第四个鱼使分别送到了大海下面一百英寸和一百二十五英寸的地方去了。一个孤独的老人拖着疲惫不堪的身子漂泊在茫茫的海面上活像个大战后的勇士。为了治服那条庞大的马林鱼，他已经费下了自己近乎所有的力气。而今，他带着自己捕获的。

        示例JSON输出：
        {
            "source1":{
                "text": "大马林鱼开始快速地围着小渔船游动，将缆绳缠绕到了桅杆上，老人右手高举着钢叉，在它跃出水面的一瞬间，竭尽全力地向它的心脏掷去，一声哀鸣结束了大鱼的生命，它静静地浮在水面上……"
                "comment": "我的心也像一块大石头落了地。我非常钦佩老人那种毫不畏惧、坚持不懈的精神，虽然知道对手实力很强，但他没有丝毫退缩，而是迎难而上。正因为有了这种精神，老渔夫才获得了这场生死较量的胜利。我们在生活中也要学习老渔夫的精神，做事情不怕困难，才能取得成功。"
            }
            "source2": {
                "text": "一个鱼食送下四十英寸的深处，第二个鱼食送下七十五英寸的深处，第三个和第四个鱼使分别送到了大海下面一百英寸和一百二十五英寸的地方去了。"
                "comment": "《老人与海》产生的视觉形象，画面感很强，这与作者应用部分电影化手法是分不开的。作品一开始就使用了特写镜头，对帆和老人的面部做了展示。近景在老人下鱼食的细节上体现最为充分：一个一个放钓丝的动作那么仔细、真切。"
            }
        }
        """
        # 输入事件信息
        user_prompt = InputData['text']

        print("[server]已向远程服务器提交摘抄任务,提交内容：\n", user_prompt)

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
        parsed_response = json.loads(response.choices[0].message.content)
        print("[server]AI摘抄条目已返回:\n", parsed_response)
        # 格式标准化
        # 构建结果列表
        result = []
        id = 0
        for key, content in parsed_response.items():
            id += 1
            result.append({"sentence": content['text'], "comment": content['comment']})
        # 返回处理后的字典
        return result
