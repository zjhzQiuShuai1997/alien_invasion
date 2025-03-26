import  sys
import  pygame
from settings import Settings

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.setting = Settings()
        """赋给属性 self.screen 的对象是⼀个 surface"""
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height))
        pygame.display.set_caption("黎小若大战社会人街溜子")

    def run_game(self):
        """开始游戏主循环"""
        while True:
            #侦听键盘和鼠标事件
            #pygame.event.get() 函数来访问 Pygame 检测到的事件
            #这个函数返回⼀个列表，其中包含它在上⼀次调⽤后发⽣的所有事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #每次循环时都重绘屏幕
            self.screen.fill(self.setting.bg_color)
            #每次循环都重新绘制屏幕
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
