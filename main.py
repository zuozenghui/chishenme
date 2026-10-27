import os

from kivy.app import App
from kivy.animation import Animation
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

import random

ANDROID_FONT_DIR = "/system/fonts"
ANDROID_FONT_CANDIDATES = (
    "NotoSansCJK-Regular.ttc",
    "NotoSansCJKsc-Regular.otf",
    "NotoSansSC-Regular.otf",
    "NotoSansHans-Regular.otf",
    "DroidSansFallback.ttf",
)
ANDROID_FONT_KEYWORDS = (
    "CJK", "SansSC", "SansHans", "MiSans",
    "OPPOSans", "HarmonyOS", "SECCJK", "VivoSans",
)

def find_android_font():
    for name in ANDROID_FONT_CANDIDATES:
        path = os.path.join(ANDROID_FONT_DIR, name)
        if os.path.isfile(path):
            return path

    try:
        files = os.listdir(ANDROID_FONT_DIR)
    except OSError:
        return None

    fonts = [f for f in files if f.lower().endswith((".ttf", ".otf", ".ttc"))]
    for keyword in ANDROID_FONT_KEYWORDS:
        regular = [f for f in fonts if keyword in f and "Regular" in f]
        if regular:
            return os.path.join(ANDROID_FONT_DIR, sorted(regular)[0])
        matched = [f for f in fonts if keyword in f]
        if matched:
            return os.path.join(ANDROID_FONT_DIR, sorted(matched)[0])
    return None

def find_windows_font():
    font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for name in ("msyh.ttc", "msyh.ttf", "simhei.ttf", "simsun.ttc", "Deng.ttf"):
        path = os.path.join(font_dir, name)
        if os.path.isfile(path):
            return path
    return None

def use_system_font():
    if platform == "android":
        font = find_android_font()
    elif platform == "win":
        font = find_windows_font()
    else:
        font = None

    if not font:
        print("未找到系统中文字体，使用 Kivy 默认字体")
        return

    print("使用系统字体:", font)
    try:
        LabelBase.register(
            name="Roboto",
            fn_regular=font,
            fn_bold=font,
            fn_italic=font,
            fn_bolditalic=font,
        )
    except Exception as error:
        print("注册系统字体失败:", error)

use_system_font()

if platform not in ("android", "ios"):
    Window.size = (420, 720)

food_list = [
    "牛肉面", "麻辣烫", "黄焖鸡", "螺蛳粉", "饺子", "馄饨",
    "炒饭", "炒面", "汉堡", "炸鸡", "烤肉", "火锅", "米线",
    "砂锅", "包子粥", "大盘鸡", "盖浇饭", "寿司", "酸辣粉",
    "羊汤", "烩面", "冒菜", "烤鱼", "杂粮煎饼", "自助",
    "湘菜", "川菜", "粤式简餐", "披萨", "手抓饼"
]

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 40
        self.spacing = 40

        self.title_label = Label(
            text="今天吃什么",
            font_size=36,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )
        self.add_widget(self.title_label)

        self.result_label = Label(
            text="点下方抽签",
            font_size=28,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.4)
        )
        self.add_widget(self.result_label)

        self.btn = Button(
            text="开始抽签",
            font_size=22,
            size_hint=(0.6, 0.12),
            pos_hint={"center_x": 0.5},
            background_color=(0.95, 0.6, 0.2, 1)
        )
        self.btn.bind(on_press=self.start_draw)
        self.add_widget(self.btn)

    def start_draw(self, instance):
        instance.disabled = True
        self.anim = Animation(duration=1.5)
        self.anim.bind(on_progress=self.on_roll, on_complete=self.on_end)
        self.anim.start(self)

    def on_roll(self, *args):
        self.result_label.text = random.choice(food_list)

    def on_end(self, *args):
        self.result_label.text = f"✅ 就吃：{self.result_label.text}"
        self.btn.disabled = False

class FoodDrawApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    FoodDrawApp().run()