from random import  randint

class Settings:
    """存储游戏《黎小若大战社会人街溜子》中所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 游戏框的宽度和高度
        self.screen_width = 1200
        self.screen_height = 800
        # 游戏背景图的颜色
        self.bg_color = (230,230,230)
        # 每次移动的距离
        self.ship_speed = 1.5
        # 移动速度的倍率
        self.ship_magnification = 1
        self.ship_limit = 3


        # 子弹设置
        #子弹发射的距离
        self.bullet_speed = 1.0
        #子弹宽度
        self.bullet_width = 4
        #子弹高度
        self.bullet_height = 8
        #获得强化道具———————子弹数量
        self.bullet_number = 3
        #子弹颜色
        self.bullet_color = (randint(0,255),randint(0,255),randint(0,255))
        #子弹数量
        self.bullets_allowed = 3

        """外星人设置"""
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1


        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 1.0
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
