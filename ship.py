import pygame

class Ship:
    """管理飞船的类"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()  # 确保这是屏幕矩形

        self.image = pygame.image.load('images/small_ruo.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)  # 初始化为浮点数
        self.y = float(self.rect.y)
        # 初始化移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # 更新浮点数坐标
        if self.moving_right:
            if self.x + self.rect.width < self.screen_rect.right:
                self.x += self.ai_game.settings.ship_speed * self.ai_game.settings.ship_magnification
        if self.moving_left:
            if self.x > 0:
                self.x -= self.ai_game.settings.ship_speed * self.ai_game.settings.ship_magnification
        if self.moving_up:
            if self.y > 0:
                self.y -= self.ai_game.settings.ship_speed * self.ai_game.settings.ship_magnification
        if self.moving_down:
            if self.y + self.rect.height < self.screen_rect.bottom:
                self.y += self.ai_game.settings.ship_speed * self.ai_game.settings.ship_magnification

        # 转换为整数坐标
        self.rect.x = int(self.x)  # 或使用 round(self.x)
        self.rect.y = int(self.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)