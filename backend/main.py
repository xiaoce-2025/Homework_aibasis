from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu, 
                            QVBoxLayout, QSlider, QLineEdit, QDialog, QPushButton, 
                            QHBoxLayout, QDoubleSpinBox, QFormLayout, QColorDialog)
from PyQt6.QtGui import QImage, QPixmap, QAction, QCursor, QIcon, QColor
from PyQt6.QtCore import Qt, QTimer, QPoint, QPointF
import random
import os
import sys
import math
import threading
import subprocess
import time
from Api import app

class SettingsDialog(QDialog):
    def __init__(self, current_scale, current_interval, current_bg_color, current_border_color, current_word_color, parent=None):
        super().__init__(parent)
        self.setWindowTitle("桌宠设置")
        self.setWindowIcon(QIcon.fromTheme("preferences-system"))
        self.setFixedSize(350, 400)  # 增加窗口大小以容纳颜色选择器
        
        self.scale_value = current_scale
        self.interval_value = current_interval
        self.bg_color_value = current_bg_color
        self.border_color_value = current_border_color
        self.word_color_value = current_word_color
        self.parent_pet = parent
        
        # 创建布局
        layout = QFormLayout()
        
        # === 缩放比例控件 ===
        # 创建滑块
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(5, 50)  # 对应0.5到5.0
        self.scale_slider.setValue(int(current_scale * 10))
        self.scale_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.scale_slider.setTickInterval(5)
        self.scale_slider.valueChanged.connect(self.slider_changed)
        
        # 创建输入框
        self.scale_input = QDoubleSpinBox()
        self.scale_input.setRange(0.5, 5.0)
        self.scale_input.setSingleStep(0.1)
        self.scale_input.setValue(current_scale)
        self.scale_input.valueChanged.connect(self.input_changed)
        
        # === 移动间隔控件 ===
        # 创建滑块
        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setRange(4, 60)  # 对应2.0s到30.0s (步长0.5s)
        self.interval_slider.setValue(int(current_interval * 2))  # 乘以2转换为整数
        self.interval_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.interval_slider.setTickInterval(5)
        self.interval_slider.valueChanged.connect(self.interval_slider_changed)
        
        # 创建输入框
        self.interval_input = QDoubleSpinBox()
        self.interval_input.setRange(2.0, 30.0)
        self.interval_input.setSingleStep(0.5)
        self.interval_input.setSuffix(" 秒")
        self.interval_input.setValue(current_interval)
        self.interval_input.valueChanged.connect(self.interval_input_changed)
        
        # === 颜色选择控件 ===
        # 背景颜色选择器
        self.bg_color_button = QPushButton("选择背景颜色")
        self.bg_color_button.clicked.connect(self.choose_bg_color)
        self.bg_color_preview = QLabel()
        self.bg_color_preview.setFixedSize(30, 20)
        self.bg_color_preview.setStyleSheet(f"background-color: {current_bg_color}; border: 1px solid black;")
        
        # 边框颜色选择器
        self.border_color_button = QPushButton("选择边框颜色")
        self.border_color_button.clicked.connect(self.choose_border_color)
        self.border_color_preview = QLabel()
        self.border_color_preview.setFixedSize(30, 20)
        self.border_color_preview.setStyleSheet(f"background-color: {current_border_color}; border: 1px solid black;")
        
        # 文字颜色选择器
        self.word_color_button = QPushButton("选择文字颜色")
        self.word_color_button.clicked.connect(self.choose_word_color)
        self.word_color_preview = QLabel()
        self.word_color_preview.setFixedSize(30, 20)
        self.word_color_preview.setStyleSheet(f"background-color: {current_word_color}; border: 1px solid black;")
        
        # 创建按钮
        self.apply_button = QPushButton("应用")
        self.apply_button.clicked.connect(self.apply_settings)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.close)
        
        # 添加控件到布局
        layout.addRow("缩放比例:", self.scale_input)
        layout.addRow(self.scale_slider)
        
        layout.addRow("移动间隔:", self.interval_input)
        layout.addRow(self.interval_slider)
        
        # 添加颜色选择器
        bg_color_layout = QHBoxLayout()
        bg_color_layout.addWidget(self.bg_color_button)
        bg_color_layout.addWidget(self.bg_color_preview)
        layout.addRow("背景颜色:", bg_color_layout)
        
        border_color_layout = QHBoxLayout()
        border_color_layout.addWidget(self.border_color_button)
        border_color_layout.addWidget(self.border_color_preview)
        layout.addRow("边框颜色:", border_color_layout)
        
        word_color_layout = QHBoxLayout()
        word_color_layout.addWidget(self.word_color_button)
        word_color_layout.addWidget(self.word_color_preview)
        layout.addRow("文字颜色:", word_color_layout)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def parse_rgba_color(self, rgba_str):
        """解析rgba颜色字符串，返回QColor对象"""
        try:
            # 处理 "rgba(255, 255, 255, 0.86)" 格式
            if rgba_str.startswith("rgba(") and rgba_str.endswith(")"):
                values = rgba_str[5:-1].split(",")
                if len(values) == 4:
                    r = int(values[0].strip())
                    g = int(values[1].strip())
                    b = int(values[2].strip())
                    a = float(values[3].strip())
                    return QColor(r, g, b, int(a * 255))
            # 处理 "rgba(255 255 255 220)" 格式
            elif rgba_str.startswith("rgba(") and rgba_str.endswith(")"):
                values = rgba_str[5:-1].split()
                if len(values) == 4:
                    r = int(values[0])
                    g = int(values[1])
                    b = int(values[2])
                    a = int(values[3])
                    return QColor(r, g, b, a)
        except:
            pass
        # 默认返回白色
        return QColor(255, 255, 255, 255)
    
    def slider_changed(self, value):
        # 滑块值改变时更新输入框
        scale = value / 10.0
        self.scale_input.blockSignals(True)  # 防止循环触发
        self.scale_input.setValue(scale)
        self.scale_input.blockSignals(False)
    
    def input_changed(self, value):
        # 输入框值改变时更新滑块
        self.scale_slider.blockSignals(True)  # 防止循环触发
        self.scale_slider.setValue(int(value * 10))
        self.scale_slider.blockSignals(False)
    
    def interval_slider_changed(self, value):
        # 间隔滑块值改变时更新输入框
        interval = value / 2.0
        self.interval_input.blockSignals(True)
        self.interval_input.setValue(interval)
        self.interval_input.blockSignals(False)
    
    def interval_input_changed(self, value):
        # 间隔输入框值改变时更新滑块
        self.interval_slider.blockSignals(True)
        self.interval_slider.setValue(int(value * 2))
        self.interval_slider.blockSignals(False)
    
    def apply_settings(self):
        # 应用设置
        self.scale_value = self.scale_input.value()
        self.interval_value = self.interval_input.value()
        
        if self.parent_pet:
            self.parent_pet.update_scale(self.scale_value)
            self.parent_pet.update_move_interval(self.interval_value)
            self.parent_pet.update_colors(self.bg_color_value, self.border_color_value, self.word_color_value)
        
        self.accept()

    def choose_bg_color(self):
        """选择背景颜色"""
        # 获取当前颜色作为初始值
        current_color = self.parse_rgba_color(self.bg_color_value)
        color = QColorDialog.getColor(current_color, self, "选择背景颜色")
        if color.isValid():
            # 转换为rgba格式
            rgba_color = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()/255:.2f})"
            self.bg_color_preview.setStyleSheet(f"background-color: {rgba_color}; border: 1px solid black;")
            self.bg_color_value = rgba_color

    def choose_border_color(self):
        """选择边框颜色"""
        # 获取当前颜色作为初始值
        current_color = self.parse_rgba_color(self.border_color_value)
        color = QColorDialog.getColor(current_color, self, "选择边框颜色")
        if color.isValid():
            # 转换为rgba格式
            rgba_color = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()/255:.2f})"
            self.border_color_preview.setStyleSheet(f"background-color: {rgba_color}; border: 1px solid black;")
            self.border_color_value = rgba_color

    def choose_word_color(self):
        """选择文字颜色"""
        # 获取当前颜色作为初始值
        current_color = self.parse_rgba_color(self.word_color_value)
        color = QColorDialog.getColor(current_color, self, "选择文字颜色")
        if color.isValid():
            # 转换为rgba格式
            rgba_color = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()/255:.2f})"
            self.word_color_preview.setStyleSheet(f"background-color: {rgba_color}; border: 1px solid black;")
            self.word_color_value = rgba_color

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.scale=2.0 # 默认桌宠大小比例
        self.setFixedSize(int(128*self.scale), int(128*self.scale))  # 宠物尺寸
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

         # 平滑移动相关变量
        self.random_move_is_open = True # 默认开启随机移动
        self.move_interval = 5000 #运动时间间隔
        self.target_pos = None  # 目标位置 (QPointF)
        self.current_pos = QPointF()  # 当前位置 (浮点数)
        self.move_speed = 2.0  # 移动速度 (像素/帧)
        self.is_moving = False  # 是否正在移动 
        
        # 加载图片资源
        self.pet_images = self.load_images("resources/yxx_images")
        self.current_image = QLabel(self)
        self.action_index = 0  # 初始化动画帧索引
        
        # 动画定时器
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(30)  # 300ms 切换一帧
        
        # 平滑移动定时器 (更快的刷新率)
        self.smooth_move_timer = QTimer()
        self.smooth_move_timer.timeout.connect(self.smooth_move)
        self.smooth_move_timer.start(16)  # ~60 FPS
        
        # 随机目标设置定时器
        self.target_timer = QTimer()
        self.target_timer.timeout.connect(self.set_random_target)
        self.target_timer.start(self.move_interval)  # 设置新目标
        
        # 设置托盘图标
        self.setup_tray_icon()

        # 创建右键菜单
        self.context_menu = QMenu(self)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.create_context_menu()

        # 修改气泡框创建方式
        self.speech_bubble = QLabel()
        self.speech_bubble_color="rgba(255 255 255 220)"
        self.border_color="pink"
        self.word_color="pink"
        # 使用ToolTip标志确保气泡框显示在最顶层
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.ToolTip
        self.speech_bubble.setWindowFlags(flags)
        self.speech_bubble.setAutoFillBackground(True)
        #self.speech_bubble.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.speech_bubble.setStyleSheet(f"""
            background-color: {self.speech_bubble_color};
            border: 1px solid {self.border_color};
            border-radius: 10px;
            padding: 4px;
            font-size: 20px;
            color: {self.word_color};
        """)
        self.speech_bubble.hide()
        
        # 问候语列表
        self.greetings = [
            "泡泡老师太伟大了！", 
            "加入泡门，拥抱美好生活", 
            "你好！", 
            "今天过得怎么样？", 
            "很高兴见到你！",
            "早安，愿你拥有美好的一天！",
            "哈喽，今天心情如何？",
            "你好，最近一切顺利吗？",
            "放松一下吧~",
            "嘿，准备好迎接新挑战了吗？",
            "欢迎加入我们的大家庭！",
            "你好呀，有什么新鲜事分享吗？",
            "嗨，阳光真好啊！",
            "祝你有个丰收的一天！",
            "你好，学习进步了吗？",
            "今天也要加油呀！",
            "嗨，咖啡时间到啦~",
            "微笑面对每一天！",
            "嗨，发现什么好书了吗？",
            "保持好心情最重要！",
            "今天遇到什么开心事了？",
            "星空下的问候！",
            "坚持梦想，终会实现！",
            "嗨，新技能学得如何？",
            "感恩遇见，珍惜当下！",
            "保持好奇心，探索世界！",
            "微笑是最好的见面礼！",
            "嗨，昨晚睡得好吗？",
            "注意劳逸结合哦！",
            "夕阳无限好，珍惜此刻！",
            "坚持阅读，收获智慧！",
            "哈喽，游戏通关了吗？"
            "嘿，今天的阳光和你一样灿烂呢！",
            "最近又发现什么有趣的新知识了吗？",
            "解难题时的专注样子超酷的！",
            "给你分享个超棒的学习小技巧~",
            "保持微笑，世界也会对你微笑哦",
            "好奇宝宝今天探索了什么新领域呀？",
            "课间要不要一起去操场晒晒太阳？",
            "你的乐观总能感染身边的人呢",
            "有什么开心事要分享吗？我准备好听啦",
            "新创意的火花又迸发了吗？",
            "难题什么的，对你来说小菜一碟吧",
            "送你今日份的幸运能量✨",
            "学习累了记得看看窗外的绿树呀",
            "你笑起来的样子超治愈的！",
            "最近帮助了多少个小伙伴呀？",
            "物理题有没有被你的智慧折服？",
            "保持好奇心，世界超有趣的！",
            "要不要试试换个思路解题？",
            "你的积极态度就是最强超能力",
            "课间十分钟也要玩得开心哦",
            "又解锁了什么新技能呀？",
            "难题就像游戏关卡，慢慢突破它",
            "给你个隔空击掌，加油加油！",
            "今天也要做自己的小太阳呀☀️",
            "分享下最近的快乐源泉呗~",
            "你的琥珀色眼睛在发光呢！",
            "放松下肩膀，深呼吸三次吧",
            "有什么新发现要告诉我吗？",
            "学习就像探险，超有意思的对吧？",
            "你解决问题的样子超帅气的！",
            "课间来段即兴舞蹈怎么样？",
            "相信你今天也能创造小奇迹",
            "保持热情，保持可爱！",
            "给你发送正能量光波biu~",
            "最近让多少人被你逗笑啦？",
            "换个角度想，难题也是礼物呢",
            "你的马尾辫今天也活力满满！",
            "课间小憩是学霸的必备技能",
            "又点亮了什么新知识树？",
            "保持探索的心，世界超精彩",
            "今天也要给自己点个赞呀👍",
            "分享下你的快乐咒语呗~",
            "你的存在本身就是正能量！",
            "难题遇到你都变乖了呢",
            "课间要不要来场脑力激荡？",
            "保持你的独特光芒呀✨",
            "今天又温暖了谁的心呢？",
            "学习就像寻宝，超好玩的！",
            "给你寄了份勇气包裹📦",
            "换个解题方式就像换新发型",
            "你的笑声是最好听的BGM",
            "又解锁了什么隐藏技能？",
            "保持好奇，保持童心！",
            "今天也要做快乐传递者呀",
            "分享下你的创意火花呗~",
            "你解决问题的思路超惊艳！",
            "放松眉头，答案就在眼前",
            "最近又帮谁解决了难题呀？",
            "学习就像搭积木，慢慢来",
            "给你发送学霸光环💫",
            "换个思路，豁然开朗！",
            "你的阳光气质无人能挡",
            "课间记得活动活动身体哦",
            "又发现了什么奇妙现象？",
            "保持热情，世界因你不同",
            "今天也要做自己的冠军🏆",
            "分享下你的快乐秘籍呗~",
            "你的存在让教室更明亮！",
            "难题只是暂时的访客啦",
            "课间要不要玩个思维游戏？",
            "保持你的魔法笑容吧😄",
            "今天又点燃了多少热情？",
            "学习就像冒险，超刺激的！",
            "给你传送智慧能量包⚡",
            "换个角度看，收获满满",
            "你的活力让每一天都新鲜",
            "课间记得补充水分和笑容",
            "又创造了什么小惊喜呀？",
            "保持探索，保持热爱！",
            "今天也要温暖身边的人呀",
            "分享下你的新发现呗~",
            "你解题的灵感源源不断呢",
            "放松手指，转转笔休息下",
            "最近又成了谁的救星呀？",
            "学习就像解谜，超有趣！",
            "给你发送幸运四叶草🍀",
            "换个方法，柳暗花明！",
            "你的正能量磁场超强大",
            "课间记得看看蓝天白云",
            "又发明了什么学习妙招？",
            "保持好奇心，永远年轻！",
            "今天也要做快乐制造机",
            "分享下你的创意点子呗~",
            "你思考的样子闪闪发光",
            "难题遇到你都让路啦",
            "课间来段即兴说唱如何？",
            "保持你的独特节奏呀",
            "今天又点亮了多少笑容？",
            "学习就像冲浪，享受过程！",
            "给你快递信心包裹📬",
            "换个思路，海阔天空！"
        ]
        
        # 问候语定时器
        self.greeting_timer = QTimer()
        self.greeting_timer.timeout.connect(self.show_random_greeting)
        self.greeting_timer.start(10000)  # 10秒显示一次问候语

        # 初始移动到右下
        screen_geo = QApplication.primaryScreen().geometry()
        x = screen_geo.width() - self.width()
        y = screen_geo.height() - self.height()
        self.move(x, y)
        self.current_pos = QPointF(x, y)  # 当前位置 (浮点数)

    def create_context_menu(self):
        """创建右键上下文菜单"""
        # 创建菜单
        self.context_menu = QMenu(self)
        
        # 添加测试选项
        test_action = QAction("和严小希对话", self)
        test_action.triggered.connect(self.on_test_action)
        self.context_menu.addAction(test_action)

        # 设置选项
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.on_settings_action)
        self.context_menu.addAction(settings_action)

        if self.random_move_is_open:
            # 关闭随机移动选项：随机移动打开时
            random_move_close_action = QAction("关闭随机移动", self)
            random_move_close_action.triggered.connect(self.on_random_move_close_action)
            self.context_menu.addAction(random_move_close_action)
        else:
            # 开启随机移动选项:随机移动关闭时
            random_move_open_action = QAction("开启随机移动", self)
            random_move_open_action.triggered.connect(self.on_random_move_open_action)
            self.context_menu.addAction(random_move_open_action)
        
        # 添加退出选项
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.quit)
        self.context_menu.addAction(quit_action)

    def show_context_menu(self, pos):
        """在指定位置显示右键菜单"""
        # 将局部坐标转换为全局坐标
        self.create_context_menu()
        global_pos = self.mapToGlobal(pos)
        self.context_menu.exec(global_pos)

    def on_test_action(self):
        """打开严小希的界面化窗口"""
        try:
            # 获取当前脚本所在的目录
            base_path = os.path.dirname(os.path.abspath(__file__))
            
            # 构建 bat 文件的完整路径 - 假设 bat 文件在 scripts 目录下
            bat_path = os.path.join(base_path, "..", "gui", "dist" , "index.html")
            
            # 使用双引号处理路径中的空格问题
            if os.name == 'nt':  # Windows系统
                command = f'cmd /c ""{bat_path}""'
            else:
                command = f'"{bat_path}"'
            
            # 使用更可靠的 subprocess 模块
            subprocess.Popen(command, shell=True)
            print(f"成功执行: {bat_path}")
            
        except Exception as e:
            print(f"执行 bat 文件失败: {str(e)}")

    def on_settings_action(self):
        """设置选项的响应函数"""
        # 创建并显示设置对话框
        settings_dialog = SettingsDialog(self.scale, self.move_interval/1000, 
                                        self.speech_bubble_color, self.border_color, self.word_color, self)
        settings_dialog.exec()

    def on_random_move_close_action(self):
        """关闭随机移动选项的响应函数"""
        self.random_move_is_open = False

    def on_random_move_open_action(self):
        """开启随机移动选项的响应函数"""
        self.random_move_is_open = True

    def load_images(self, folder_path):
        """加载图片资源，按动作分类"""
        actions = ["idle", "walk", "jump"]
        images = {}
        for action in actions:
            action_path = os.path.join(folder_path, action)
            if os.path.exists(action_path):
                images[action] = [
                    QPixmap(os.path.join(action_path, img))
                    for img in sorted(os.listdir(action_path))
                    if img.lower().endswith(('.png', '.jpg', '.jpeg'))
                ]
        return images

    def set_image(self, pixmap):
        """设置当前显示的图像"""
        self.current_image.setPixmap(pixmap.scaled(
            self.size(), Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.current_image.resize(self.size())

    def update_animation(self):
        """定时更新帧动画"""
        # 根据移动状态选择动画
        current_action = "walk" if self.is_moving else "idle"
        
        if current_action in self.pet_images and self.pet_images[current_action]:
            if self.action_index >= len(self.pet_images[current_action]):
                self.action_index = -50  # 循环播放
            self.set_image(self.pet_images[current_action][max(self.action_index,0)])
            self.action_index += 1

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            # 更新移动状态
            self.is_moving = True
            self.target_pos = None
            # 更新当前位置为浮点数
            self.current_pos = QPointF(self.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_pos
            self.move(new_pos.x(),new_pos.y())
            # 更新当前位置
            self.current_pos = QPointF(new_pos)

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        # 释放后更新移动状态
        self.is_moving = False

    def setup_tray_icon(self):
        """创建系统托盘图标"""
        tray_icon = QSystemTrayIcon(self)
        # 使用内置图标作为备选方案
        tray_icon.setIcon(QIcon.fromTheme("face-smile") or QIcon("resources/icon.png"))
        
        menu = QMenu()
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)
        
        tray_icon.setContextMenu(menu)
        tray_icon.show()

    def move(self, x, y):
        """重写move方法，同时移动气泡框"""
        super().move(x, y)
        
        # 如果气泡框可见，更新其位置
        if self.speech_bubble.isVisible():
            # 获取桌宠的屏幕位置
            pet_global_pos = self.mapToGlobal(QPoint(0, 0))
            
            # 更新气泡框位置
            bubble_x = pet_global_pos.x() + int(self.width()/2)
            bubble_y = pet_global_pos.y() - int(self.speech_bubble.height()/2)
            self.speech_bubble.move(bubble_x, bubble_y)

    def set_random_target(self):
        """设置随机目标位置"""
        if not self.random_move_is_open:
            return
        if self.is_moving:
            return
            
        screen_geo = QApplication.primaryScreen().geometry()
        
        # 随机生成目标位置
        new_x = random.randint(0, screen_geo.width() - self.width())
        new_y = random.randint(0, screen_geo.height() - self.height())
        
        self.target_pos = QPointF(new_x, new_y)
        self.move_speed = math.sqrt((self.target_pos.x()-self.pos().x())**2+(self.target_pos.y()-self.pos().y())**2)/60
        self.is_moving = True

    def smooth_move(self):
        """平滑移动到目标位置"""
        if not self.target_pos or not self.is_moving:
            return
            
        # 计算到目标的距离
        dx = self.target_pos.x() - self.current_pos.x()
        dy = self.target_pos.y() - self.current_pos.y()
        distance = math.sqrt(dx**2 + dy**2)
        
        # 如果已经到达目标位置
        if distance < self.move_speed:
            # 移动到目标位置并转换为整数
            self.move(int(self.target_pos.x()), int(self.target_pos.y()))
            self.current_pos = self.target_pos
            self.is_moving = False
            return
            
        # 计算移动方向向量
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance
        else:
            direction_x, direction_y = 0, 0
            
        # 计算移动增量
        move_x = direction_x * self.move_speed
        move_y = direction_y * self.move_speed
        
        # 更新当前位置
        self.current_pos.setX(self.current_pos.x() + move_x)
        self.current_pos.setY(self.current_pos.y() + move_y)
        
        # 移动到新位置（调用重写的move方法）
        self.move(int(self.current_pos.x()), int(self.current_pos.y()))

    def move_to_random_position(self):
        """移动宠物到随机位置"""
        screen_geo = QApplication.primaryScreen().geometry()
        x = random.randint(0, screen_geo.width() - self.width())
        y = random.randint(0, screen_geo.height() - self.height())
        self.move(x, y)
        # 初始化当前位置
        self.current_pos = QPointF(x, y)
        self.target_pos = QPointF(x, y)  # 设置当前位置为目标位置

    def update_scale(self, new_scale):
        """更新桌宠的缩放比例"""
        if new_scale == self.scale:
            return
            
        # 保存当前中心位置
        current_center = self.geometry().center()
        
        # 更新缩放比例
        self.scale = new_scale
        
        # 更新窗口大小
        self.setFixedSize(int(128 * self.scale), int(128 * self.scale))
        
        # 重新设置图像
        if self.pet_images:
            current_action = "walk" if self.is_moving else "idle"
            if current_action in self.pet_images and self.pet_images[current_action]:
                # 确保动画索引在有效范围内
                idx = self.action_index % len(self.pet_images[current_action])
                self.set_image(self.pet_images[current_action][idx])
        
        # 计算新位置，使中心点不变
        new_x = current_center.x() - self.width() // 2
        new_y = current_center.y() - self.height() // 2
        
        # 确保新位置在屏幕范围内
        screen_geo = QApplication.primaryScreen().geometry()
        new_x = max(0, min(new_x, screen_geo.width() - self.width()))
        new_y = max(0, min(new_y, screen_geo.height() - self.height()))
        
        # 移动窗口
        self.move(new_x, new_y)
        self.current_pos = QPointF(new_x, new_y)

         # 更新气泡框样式（保持字体比例）
        font_size = max(10, int(20 * new_scale / 2.0))  # 根据缩放比例调整字体大小
        self.speech_bubble.setStyleSheet(f"""
            background-color: {self.speech_bubble_color};
            border: 1px solid {self.border_color};
            border-radius: 10px;
            padding: 4px;
            font-size: {font_size}px;
            color: {self.word_color};
        """)
        
        # 如果气泡框可见，更新其位置
        if self.speech_bubble.isVisible():
            # 获取桌宠的屏幕位置
            pet_global_pos = self.mapToGlobal(QPoint(0, 0))
            
            # 更新气泡框位置
            bubble_x = pet_global_pos.x() + int(self.width()/2)
            bubble_y = pet_global_pos.y() - int(self.speech_bubble.height()/2)
            self.speech_bubble.move(bubble_x, bubble_y)

    def update_move_interval(self, new_interval_seconds):
        """更新移动时间间隔"""
        # 将秒转换为毫秒
        new_interval_ms = int(new_interval_seconds * 1000)
        
        if new_interval_ms == self.move_interval:
            return
            
        self.move_interval = new_interval_ms
        
        # 停止当前定时器
        if self.target_timer and self.target_timer.isActive():
            self.target_timer.stop()
        
        # 创建新的定时器
        self.target_timer = QTimer()
        self.target_timer.timeout.connect(self.set_random_target)
        self.target_timer.start(self.move_interval)
        
    def show_random_greeting(self):
        """随机显示问候语"""
        if not self.greetings:
            return
        
        greeting = random.choice(self.greetings)
        self.speech_bubble.setText(greeting)
        self.speech_bubble.adjustSize()  # 根据文本内容调整大小
        
        # 获取桌宠的屏幕位置
        pet_global_pos = self.mapToGlobal(QPoint(0, 0))
        
        # 定位气泡框在桌宠右上方（使用屏幕坐标）
        bubble_x = pet_global_pos.x() + self.width()
        bubble_y = pet_global_pos.y() - self.speech_bubble.height()
        
        self.speech_bubble.move(bubble_x, bubble_y)
        self.speech_bubble.show()
        
        # 3秒后隐藏气泡框
        QTimer.singleShot(3000, self.speech_bubble.hide)

    def update_colors(self, new_bg_color, new_border_color, new_word_color):
        """更新气泡框的颜色"""
        self.speech_bubble_color = new_bg_color
        self.border_color = new_border_color
        self.word_color = new_word_color
        
        # 根据当前缩放比例计算字体大小
        font_size = max(10, int(20 * self.scale / 2.0))
        
        self.speech_bubble.setStyleSheet(f"""
            background-color: {self.speech_bubble_color};
            border: 1px solid {self.border_color};
            border-radius: 10px;
            padding: 4px;
            font-size: {font_size}px;
            color: {self.word_color};
        """)
        
        # 如果气泡框可见，更新其位置
        if self.speech_bubble.isVisible():
            # 获取桌宠的屏幕位置
            pet_global_pos = self.mapToGlobal(QPoint(0, 0))
            
            # 更新气泡框位置
            bubble_x = pet_global_pos.x() + int(self.width()/2)
            bubble_y = pet_global_pos.y() - int(self.speech_bubble.height()/2)
            self.speech_bubble.move(bubble_x, bubble_y)

def run_flask_server():
    """在新线程中运行Flask服务器"""
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    # 启动Flask服务器线程
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    flask_thread.start()
    
    # 给服务器一点启动时间
    time.sleep(0.5)

    qt_app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(qt_app.exec())