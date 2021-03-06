import pygame
import sys

# 导入绝对路径，使程序可运行
sys.path.append("D:/workspacePythonIDE/")
from hm_pygame.hm_game_vo import *


class PlaneGame:
    """飞机大战主类"""

    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprite()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 500)
        pygame.time.set_timer(HERO_FIRE_EVENT, 300)

    def start_game(self):
        """ 开始游戏 """
        print("游戏开始...")
        while True:
            self.clock.tick(FRESH_PER_SECOND)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新精灵组
            self.__update_sprite()
            # 更新显示
            pygame.display.update()
        pass

    @staticmethod
    def game_over():
        """ 结束游戏 """
        pygame.quit()
        exit()

    def __create_sprite(self):
        """ 创建精灵组 """
        pygame.init()
        # 创建背景
        bg1 = BackGround()
        bg2 = BackGround(is_alt=True)
        back_group = pygame.sprite.Group(bg1, bg2)
        self.back_group = back_group
        # 创建敌机精灵
        self.enemy_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        # 创建英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.again = GameOn("./images/again.png")
        self.over = GameOn("./images/gameover.png", y=self.again.rect.bottom + 50)
        self.on_group = pygame.sprite.Group()
        # pygame.font.get_fonts()  来查看系统支持那些字体
        my_font = pygame.font.SysFont("simsunnsimsun", 18, bold=True)
        text_image = my_font.render("【王者归来-best】", False, (255, 77, 70))
        d1 = GameIcon("./images/light.png", y=0, x=0)
        d1.rect.left = SCREEN_RECT.left
        d1.rect.top = SCREEN_RECT.top
        d2 = GameIcon("./images/light.png", y=0, x=0)
        d2.rect.right = SCREEN_RECT.right
        d2.rect.top = SCREEN_RECT.top
        d3 = GameIcon(None, y=0, x=0, imag=text_image)
        d3.rect.centerx = SCREEN_RECT.centerx
        self.icon_group = pygame.sprite.Group(d1, d2, d3)

    def __event_handler(self):
        # 监听通用事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.game_over()
            # elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            #     key_click(event, self.hero.rect)
            elif event.type == pygame.MOUSEMOTION:
                mouse_move(event, self.hero.rect)
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy_group.add(Enemy())
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(self.on_group) > 0:
                    if mouse_button(event, self.again, self.over) == 1:
                        # 继续游戏
                        self.on_group.empty()
                        self.hero_group.add(self.hero)
                    elif mouse_button(event, self.again, self.over) == 2:
                        # 结束游戏
                        PlaneGame.game_over()
            else:
                print(event)
        key_press(pygame.key.get_pressed(), self.hero.rect)

    def __check_collide(self):
        dicts = pygame.sprite.groupcollide(Hero.bullet_group, self.enemy_group, True, True)
        for key in dicts:
            print("__check_collide dicts.key %s = %s value %s = %s" % (
                type(key), key.rect, type(dicts[key][0]), dicts[key][0].rect))
            for en in dicts[key]:
                self.bomb_group.add(Bomb(en.image_url, en.rect))
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        for enemy in enemies:
            print("__check_collide dicts.enemies %s = %s " % (type(enemy), enemy.rect))
            self.bomb_group.add(Bomb(enemy.image_url, enemy.rect))
        if len(enemies) > 0:
            self.bomb_group.add(Bomb(self.hero.image_url, self.hero.rect))
            self.hero.kill()
            # PlaneGame.game_over()

    def __update_sprite(self):
        #  更新桌布
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        Hero.bullet_group.update()
        Hero.bullet_group.draw(self.screen)
        self.bomb_group.update()
        self.bomb_group.draw(self.screen)
        if len(self.hero_group) == 0 and len(self.on_group) == 0:
            self.on_group.add(self.again, self.over, GameOn("./images/vipIconl.png", y=self.again.rect.top - 50))
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.on_group.update()
        self.on_group.draw(self.screen)
        self.icon_group.update()
        self.icon_group.draw(self.screen)


if __name__ == '__main__':
    pm = PlaneGame()
    pm.start_game()
