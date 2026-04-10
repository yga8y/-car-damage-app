# 车辆定损AI APP - Kivy版本
# 使用Python Kivy框架构建，可直接打包为APK

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
import json
import sqlite3
from pathlib import Path

# 设置窗口大小
Window.size = (400, 700)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class DatabaseHelper:
    """数据库助手"""
    
    def __init__(self):
        # 使用内存数据库或本地数据库
        self.db_path = Path(__file__).parent / "cardamage.db"
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 创建配件价格表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts_pricing (
                id INTEGER PRIMARY KEY,
                brand TEXT,
                series TEXT,
                part_name TEXT,
                oe_number TEXT,
                factory_price REAL,
                is_safety_part INTEGER,
                replace_rule TEXT
            )
        ''')
        
        # 创建规则表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS damage_rules (
                id INTEGER PRIMARY KEY,
                accident_type TEXT,
                damage_location TEXT,
                damage_type TEXT,
                replace_rule TEXT,
                is_safety_part INTEGER
            )
        ''')
        
        # 插入示例数据
        self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self, cursor):
        """插入示例数据"""
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM parts_pricing")
        if cursor.fetchone()[0] > 0:
            return
        
        # 插入配件价格
        parts = [
            ('丰田', '卡罗拉', '后保险杠', '52159-02955', 1050, 0, '严重破损必换'),
            ('丰田', '卡罗拉', '左后尾灯', '81561-02090', 650, 0, '破损必换'),
            ('丰田', '卡罗拉', '前保险杠', '52119-02977', 1150, 0, '严重破损必换'),
            ('丰田', '卡罗拉', '左前大灯', '81150-02P60', 2380, 1, '破损必换'),
            ('丰田', '卡罗拉', '前挡风玻璃', '56101-02020', 1380, 1, '任何破损必换'),
            ('大众', '朗逸', '后保险杠', '18D807421', 1150, 0, '严重破损必换'),
            ('大众', '朗逸', '左后尾灯', '18D945095', 680, 0, '破损必换'),
            ('本田', '思域', '后保险杠', '04715-TGG-A00ZZ', 1180, 0, '严重破损必换'),
            ('本田', '思域', '左后尾灯', '33550-TGG-A01', 720, 0, '破损必换'),
        ]
        
        cursor.executemany('''
            INSERT INTO parts_pricing (brand, series, part_name, oe_number, factory_price, is_safety_part, replace_rule)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', parts)
        
        # 插入规则
        rules = [
            ('追尾', '后保险杠', '破损', '裂纹/破损/穿孔：更换', 0),
            ('追尾', '后保险杠', '裂纹', '裂纹/破损/穿孔：更换', 0),
            ('追尾', '后保险杠', '穿孔', '裂纹/破损/穿孔：更换', 0),
            ('追尾', '左后尾灯', '裂纹', '裂纹/进水/灯脚断裂：更换', 1),
            ('追尾', '左后尾灯', '破损', '破损必换', 0),
            ('追尾', '后防撞梁', '变形', '任何变形/弯曲：必须更换', 1),
            ('侧撞', '左前车门', '凹陷', '单处凹陷≤3cm：钣金', 0),
            ('侧撞', '左前车门', '撕裂', '多处凹陷/褶皱/撕裂：更换', 0),
            ('正面碰撞', '前保险杠', '破损', '破损/卡扣断裂：更换', 0),
            ('正面碰撞', '左前大灯', '破损', '灯脚断/裂纹/进水：更换', 1),
        ]
        
        cursor.executemany('''
            INSERT INTO damage_rules (accident_type, damage_location, damage_type, replace_rule, is_safety_part)
            VALUES (?, ?, ?, ?, ?)
        ''', rules)
    
    def get_part_price(self, brand, series, part_name):
        """获取配件价格"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT part_name, oe_number, factory_price, is_safety_part, replace_rule
            FROM parts_pricing
            WHERE brand = ? AND series = ? AND part_name LIKE ?
        ''', (brand, series, f'%{part_name}%'))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'part_name': result[0],
                'oe_number': result[1],
                'price': result[2],
                'is_safety_part': bool(result[3]),
                'replace_rule': result[4]
            }
        return None
    
    def get_damage_rule(self, accident_type, damage_location, damage_type):
        """获取定损规则"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT accident_type, damage_location, damage_type, replace_rule, is_safety_part
            FROM damage_rules
            WHERE accident_type = ? AND damage_location LIKE ? AND damage_type LIKE ?
        ''', (accident_type, f'%{damage_location}%', f'%{damage_type}%'))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'accident_type': result[0],
                'damage_location': result[1],
                'damage_type': result[2],
                'replace_rule': result[3],
                'is_safety_part': bool(result[4])
            }
        return None

class HomeScreen(BoxLayout):
    """首页"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # 标题
        title = Label(
            text='[b]车辆定损AI[/b]',
            markup=True,
            font_size='28sp',
            size_hint_y=None,
            height=60,
            color=(0.2, 0.4, 0.8, 1)
        )
        self.add_widget(title)
        
        subtitle = Label(
            text='智能识别 · 精准报价 · 只换不修',
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=(0.5, 0.5, 0.5, 1)
        )
        self.add_widget(subtitle)
        
        # 功能按钮
        btn_layout = GridLayout(cols=1, spacing=15, size_hint_y=None, height=300)
        
        btn_new = Button(
            text='📸 新建定损',
            font_size='18sp',
            background_color=(0.2, 0.6, 0.9, 1),
            background_normal='',
            size_hint_y=None,
            height=60
        )
        btn_new.bind(on_press=lambda x: self.app.show_evaluation_screen())
        btn_layout.add_widget(btn_new)
        
        btn_history = Button(
            text='📋 历史记录',
            font_size='18sp',
            background_color=(0.4, 0.7, 0.4, 1),
            background_normal='',
            size_hint_y=None,
            height=60
        )
        btn_history.bind(on_press=lambda x: self.app.show_history_screen())
        btn_layout.add_widget(btn_history)
        
        btn_help = Button(
            text='❓ 使用帮助',
            font_size='18sp',
            background_color=(0.9, 0.6, 0.2, 1),
            background_normal='',
            size_hint_y=None,
            height=60
        )
        btn_help.bind(on_press=lambda x: self.show_help())
        btn_layout.add_widget(btn_help)
        
        self.add_widget(btn_layout)
    
    def show_help(self):
        """显示帮助"""
        help_text = '''
使用说明：

1. 点击"新建定损"
2. 选择车型和事故类型
3. 输入损伤部位
4. 系统自动计算报价

支持事故类型：
- 追尾
- 侧撞
- 正面碰撞
- 剐蹭

数据基于原厂配件价格
        '''
        popup = Popup(
            title='使用帮助',
            content=Label(text=help_text, text_size=(300, None)),
            size_hint=(None, None),
            size=(350, 400)
        )
        popup.open()

class EvaluationScreen(BoxLayout):
    """定损评估页面"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.db = DatabaseHelper()
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        # 标题
        title = Label(
            text='[b]新建定损[/b]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.2, 0.4, 0.8, 1)
        )
        self.add_widget(title)
        
        # 表单区域
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=250)
        
        # 品牌
        form_layout.add_widget(Label(text='品牌:', size_hint_x=None, width=80))
        self.brand_spinner = Spinner(
            text='丰田',
            values=['丰田', '大众', '本田', '别克', '日产', '比亚迪', '特斯拉', '宝马', '奔驰', '奥迪'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.brand_spinner)
        
        # 车系
        form_layout.add_widget(Label(text='车系:', size_hint_x=None, width=80))
        self.series_input = TextInput(
            text='卡罗拉',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.series_input)
        
        # 年款
        form_layout.add_widget(Label(text='年款:', size_hint_x=None, width=80))
        self.year_spinner = Spinner(
            text='2022',
            values=['2024', '2023', '2022', '2021', '2020', '2019', '2018'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.year_spinner)
        
        # 事故类型
        form_layout.add_widget(Label(text='事故类型:', size_hint_x=None, width=80))
        self.accident_spinner = Spinner(
            text='追尾',
            values=['追尾', '侧撞', '正面碰撞', '剐蹭'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.accident_spinner)
        
        # 损伤部位
        form_layout.add_widget(Label(text='损伤部位:', size_hint_x=None, width=80))
        self.part_input = TextInput(
            text='后保险杠',
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text='如：后保险杠、左后尾灯'
        )
        form_layout.add_widget(self.part_input)
        
        # 损伤类型
        form_layout.add_widget(Label(text='损伤类型:', size_hint_x=None, width=80))
        self.damage_type_spinner = Spinner(
            text='破损',
            values=['破损', '裂纹', '凹陷', '撕裂', '变形', '穿孔'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.damage_type_spinner)
        
        self.add_widget(form_layout)
        
        # 按钮区域
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        btn_back = Button(
            text='返回',
            background_color=(0.7, 0.7, 0.7, 1),
            background_normal=''
        )
        btn_back.bind(on_press=lambda x: self.app.show_home_screen())
        btn_layout.add_widget(btn_back)
        
        btn_evaluate = Button(
            text='开始定损',
            background_color=(0.2, 0.6, 0.9, 1),
            background_normal=''
        )
        btn_evaluate.bind(on_press=self.do_evaluation)
        btn_layout.add_widget(btn_evaluate)
        
        self.add_widget(btn_layout)
        
        # 结果显示区域
        self.result_label = Label(
            text='',
            markup=True,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            color=(0.2, 0.2, 0.2, 1)
        )
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)
    
    def do_evaluation(self, instance):
        """执行定损评估"""
        brand = self.brand_spinner.text
        series = self.series_input.text
        year = self.year_spinner.text
        accident_type = self.accident_spinner.text
        part_name = self.part_input.text
        damage_type = self.damage_type_spinner.text
        
        # 获取规则
        rule = self.db.get_damage_rule(accident_type, part_name, damage_type)
        
        # 获取配件价格
        part_info = self.db.get_part_price(brand, series, part_name)
        
        # 判断建议
        if rule:
            is_safety = rule.get('is_safety_part', False)
            suggest = '更换' if is_safety or damage_type in ['破损', '裂纹', '撕裂', '穿孔'] else '修复'
            reason = rule.get('replace_rule', '')
        else:
            suggest = '更换' if damage_type in ['破损', '裂纹', '撕裂', '穿孔'] else '修复'
            reason = '根据损伤程度判断'
        
        # 计算价格
        if part_info:
            price = part_info.get('price', 0)
            oe_number = part_info.get('oe_number', '')
            is_safety = part_info.get('is_safety_part', False)
        else:
            price = 0
            oe_number = ''
            is_safety = False
        
        labor_cost = 375 if suggest == '更换' else 100
        total = price + labor_cost if suggest == '更换' else labor_cost
        
        # 显示结果
        safety_mark = '[color=ff0000]【安全件】[/color]' if is_safety else ''
        
        result_text = f'''
[b]定损结果[/b]

车型：{brand} {series} {year}
事故类型：{accident_type}

[b]损伤部位：[/b]{part_name} {safety_mark}
[b]损伤类型：[/b]{damage_type}
[b]维修建议：[/b]{suggest}
[b]判定原因：[/b]{reason}

[b]费用明细：[/b]
配件费：¥{price:.0f}
工时费：¥{labor_cost:.0f}
[b]总计：¥{total:.0f}[/b]

OE编号：{oe_number}
        '''
        
        self.result_label.text = result_text

class HistoryScreen(BoxLayout):
    """历史记录页面"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        # 标题
        title = Label(
            text='[b]历史记录[/b]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.2, 0.4, 0.8, 1)
        )
        self.add_widget(title)
        
        # 历史记录列表
        self.history_label = Label(
            text='暂无历史记录\n\n定损记录将显示在这里',
            markup=True,
            text_size=(Window.width - 40, None),
            halign='center',
            valign='center',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.add_widget(self.history_label)
        
        # 返回按钮
        btn_back = Button(
            text='返回首页',
            size_hint_y=None,
            height=50,
            background_color=(0.7, 0.7, 0.7, 1),
            background_normal=''
        )
        btn_back.bind(on_press=lambda x: self.app.show_home_screen())
        self.add_widget(btn_back)

class CarDamageApp(App):
    """主应用"""
    
    def build(self):
        self.title = '车辆定损AI'
        
        # 创建屏幕
        self.home_screen = HomeScreen(self)
        self.evaluation_screen = EvaluationScreen(self)
        self.history_screen = HistoryScreen(self)
        
        # 主布局
        self.root_layout = BoxLayout()
        self.show_home_screen()
        
        return self.root_layout
    
    def show_home_screen(self):
        """显示首页"""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.home_screen)
    
    def show_evaluation_screen(self):
        """显示定损页面"""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.evaluation_screen)
    
    def show_history_screen(self):
        """显示历史记录页面"""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.history_screen)

if __name__ == '__main__':
    CarDamageApp().run()
