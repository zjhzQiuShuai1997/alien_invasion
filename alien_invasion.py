import  sys
import  pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        """赋给属性 self.screen 的对象是⼀个 surface"""
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("黎小若大战社会人街溜子")
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏主循环"""
        while True:
            #侦听键盘和鼠标事件
            #pygame.event.get() 函数来访问 Pygame 检测到的事件
            #这个函数返回⼀个列表，其中包含它在上⼀次调⽤后发⽣的所有事件
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         sys.exit()
            self._check_events()
            self.ship.update()
            self._update_screen()
            #每次循环时都重绘屏幕
            # self.screen.fill(self.setting.bg_color)
            # self.ship.blitme()
            #每次循环都重新绘制屏幕
            # pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # elif  event.type == pygame.KEYDOWN:
            #     if event.type == pygame.K_RIGHT:
            #         print("RIGHT")
            #         #向右移动飞船
            #         self.ship.moving_right = True
            #     elif event.type == pygame.K_LEFT:
            #         print("LEFT")
            #         self.ship.moving_left = True
            # elif event.type == pygame.KEYUP:
            #     if event.type == pygame.K_RIGHT:
            #         self.ship.moving_right = False
            #     elif event.type == pygame.K_LEFT:
            #         self.ship.moving_left = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
