import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # 全屏游戏化，目前测试阶段暂不放开，后续有需要可放开
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        """赋给属性 self.screen 的对象是⼀个 surface"""
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("黎小若大战社会人街溜子")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.invoke_count = 0

        self._create_fleet()
        # 游戏一开始处于非活动状态
        self.game_active = False
        # 创建Play按钮
        self.play_button = Button(self, "PLAY")

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
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                # 删除已经超过页面的子弹,这里的处理移至_update_bullets()方法中
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单机 play 按钮的时候开始游戏"""
        button_check = self.play_button.rect.collidepoint(mouse_pos)
        # collidepoint: 判断鼠标点击位置是否在按钮内
        # mouse_pos: 鼠标点击位置
        if button_check and not self.game_active:
        # if self.play_button.rect.collidepoint(mouse_pos):
            # 重置游戏的统计信息
            # 还原游戏设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True
            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()
            # 创建新的外星人舰队，并将飞船放置底部
            self._create_fleet()
            self.ship.center_ship()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()
            self.sb.prep_level()
            # 游戏开始后隐藏光标
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入到编组bullets中"""
        # if len(self.bullets) < self.settings.bullets_allowed:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹"""
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    # 检查子弹和外星人的碰撞，子弹击中外星飞船
    def _check_bullet_alien_collisions(self):
        #检查是否有子弹击中了外星人
        #如果是，就删除对应的外星人
        # pygame.sprite.groupcollide: 四个参数，第一个是子弹编组，第二个是外星人编组，第三个是子弹是否消失，第四个是外星人是否消失
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并把它放到当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    # 创建外星人团队
    def _create_fleet(self):
        """创建外星人团队"""
        # 先来一个黄毛外星人,他又不断叫来了紫毛外星人，红毛外星人，蓝毛外星人知道蜜雪冰城门口站不下了为止
        # 外星人们间距为一个外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 添加一行外星人后，重置 x 值并递增 y 值
            current_x = alien_width
            current_y += 2 * alien_height
            self.aliens.add(alien)
    # 检查是否有外星人到达边缘
    def _check_fleet_edges(self):
        """在有外星人到达边缘的情况下采取措施"""
        for alien in self.aliens.sprites():
            # print(f"alien.check_edges() {alien.check_edges()}")
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # 改变 fleet_direction 的值
    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # 响应外星人被撞到
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ship_left 减1
            self.stats.ships_left -= 1

            # 清空外星人和子弹的列表
            self.aliens.empty()
            self.bullets.empty()

            #创建一个新的外星舰队，并将飞船放在屏幕的底部中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.game_active = False
            # 游戏结束后显示鼠标黄标
            pygame.mouse.set_visible(True)

    # 检查是否有外星人到达屏幕底部
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                #像飞船被撞到一样进行处理
                self._ship_hit()
                break

    # 更新外星舰队中的所有外星人的位置
    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        """检查是否有外星人位于屏幕边缘，并更新整个外星舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞 spritecollideany：检测是否有两个元素块之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.invoke_count += 1
            print(f"Ship hit!!!{self.invoke_count}")
            self._ship_hit()
            # 检查外星人是否到达屏幕底部
            self._check_aliens_bottom()

    # 更新屏幕上的图像，并切换到新屏幕
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
