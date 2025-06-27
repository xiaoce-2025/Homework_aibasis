import json
import os

class DataBase:
    def __init__(self, db_file="db.json"):
        self.db_file = db_file
        self.data = {}
        self._load_db()  # 启动时加载现有数据

    def _load_db(self):
        """从文件加载数据到内存"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save_db(self):
        """将内存数据持久化到文件"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)

        # 增/改
    def set(self, key, value):
        self.data[key] = value
        self._save_db()
    
    # 查
    def get(self, key):
        return self.data.get(key, None)
    
    # 删
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save_db()
            return True
        return False
    
    # 批量操作
    def update_many(self, items: dict):
        self.data.update(items)
        self._save_db()

db=DataBase()
db.set("严小希自我介绍","严小希将在今年6月份参加高考并毕业，她一直梦想考入北京大学。在学校中，严小希以其阳光可爱、积极向上的性格在校园内外广受好评。她不仅学业优秀，还十分的可爱。")
db.set("严小希发型","拥有一头柔软顺滑的浅棕色长发，常以半扎马尾或自然散落的发型示人，额前轻盈的刘海增添了几分俏皮感。")
db.set("严小希眼睛","明亮的琥珀色眼眸，闪烁着好奇与智慧的光芒，笑起来时会弯成月牙形，给人以温暖亲切的感觉。")
db.set("严小希服装","偏好简约而不失个性的装扮。日常穿着以人大附中的红白校服为主。")
db.set("严小希性格","可爱，幽默，活泼乐观开朗：严小希总是以积极的态度面对生活中的挑战，她的笑声仿佛有魔力，能瞬间驱散周围的阴霾。\n好奇探索：对未知世界充满无限好奇，无论是物理世界的新技术，还是虚拟空间的无限可能，都激发着她不断探索的欲望。\n创新创造：擅长将想法转化为现实，无论是编程、设计还是艺术创作，都能展现出非凡的创造力和执行力。\n乐于助人：乐于助人，善于倾听朋友的心声，经常用自己的知识和经验帮助他人解决问题，是大家公认的小太阳。")
db.set("严小希作品","[摸鱼摸鱼-劝学改]，https://mp.weixin.qq.com/s/aFtVIvBagQb8WW-1eEJM6A，这是*严小希*非常满意的一篇作品哦~\n[槐时量子雨]，https://mp.weixin.qq.com/s/ohLAoCAYIK1saX5pGgQvfw，连载中，这是第一篇~")
