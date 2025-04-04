class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        # self.ai_game = ai_game
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0

        # 游戏刚启动时处于非活动状态
        # self.game_active = False

        # 在任何情况下都不应重置最高分
        # self.height_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1