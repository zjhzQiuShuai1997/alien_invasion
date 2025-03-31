import  pygame.font

class Scoreboard:
    """显示得分信息的类"""
    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # 显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        # 准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        # round() 函数通常让浮点数（第⼀个实参）精确到⼩数点后某⼀位，其中
        # 的⼩数位数由第⼆个实参指定。如果将第⼆个实参指定为负数，round()
        # 会将第⼀个实参舍⼊到最近的 10 的整数倍，如 10、100、1000 等。这⾥的
        # 代码让 Python 将 stats.score 的值舍⼊到最近的 10 的整数倍，并将结
        # 果存储到 rounded_score 中。

        rounded_score = round(self.stats.score,-1)
        score_str = f"{rounded_score}"
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        # self.screen.bill(): 绘制图像，参数是图像和图像的左上角坐标
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)

    # 显示最高分
    def prep_high_score(self):
        """将最高分渲染为图像"""
        high_score = round(self.stats.high_score,-1)
        high_score_str = f"{high_score}"
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
        # 将最高分放在屏幕顶部
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """将等级渲染为图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)
        # 将等级放置在得分下方，靠右对齐
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10