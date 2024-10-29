import pygame
import sys
import os

import json


class CoreFunctions:
    def terminate(_):
        pygame.quit()
        sys.exit()

    def play_sound(self, name, loop=0, start=0, fade=0):
        pygame.mixer.music.load(os.path.join('static', 'sounds', name))
        pygame.mixer.music.play(loop, start, fade)

    def load_image(self, name):
        return pygame.image.load(os.path.join('static', 'images', name))

    def show_image(self, name):
        start_image = pygame.transform.scale(self.load_image(name), (APP_CFG['width'], APP_CFG['height']))
        screen.blit(start_image, (0, 0))

    def load_level(self, filename):
        with open(os.path.join('levels', f'{filename}'), 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def display_jumps(self, jumps, color):
        font = pygame.font.SysFont("8-BIT WONDER.TTF", 30)
        text = font.render(f"you've made {jumps} jumps!", True, color)
        screen.blit(text, (215, 75))


class ScreenMethods:
    def menu_click_waiter(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    functions.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return '1.txt'
                    elif event.key == pygame.K_2:
                        return '2.txt'
                    elif event.key == pygame.K_ESCAPE:
                        functions.terminate()
            pygame.display.flip()
            clock.tick(APP_CFG['fps'])

    def display_jumps(self, jumps, color):
        font = pygame.font.SysFont("8-BIT WONDER.TTF", 30)
        text = font.render(f"you've made {jumps} jumps", True, color)
        screen.blit(text, (215, 75))

    def generate_level(self, level):
        # добавляем в группу, которую будем отрисовывать и свою группу, которую будем проверять на столкновение с персонажем
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] in '1234':
                    platforms.add(Tile('earth' + level[y][x], x, y))
                    all_sprites.add(Tile('earth' + level[y][x], x, y))
                elif level[y][x] == 'c':
                    coins.add(Tile('c', x, y))
                    all_sprites.add(Tile('c', x, y))

    def generate_background(self, background, coords):
        screen.fill('black')
        screen.blit(background, coords)


class Screens(ScreenMethods):
    def start_screen(self):
        functions.play_sound('menu.mp3', -1, 0, 1500)
        functions.show_image('start_image.png')
        return self.menu_click_waiter()

    def main_game_screen(self, levelname):
        clock = pygame.time.Clock()
        camera = Camera()
        functions.play_sound('main.mp3', -1, 0, 1000)

        global platforms, all_sprites, coins
        platforms, all_sprites, coins = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
        player = Player(200, 550)
        player.image.set_alpha(225)
        left, right = False, False

        while True:
            platforms.empty()
            all_sprites.empty()
            all_sprites.add(player)

            self.generate_background(functions.load_image('level_background.png'), (0, camera.dy - 728))
            self.generate_level(functions.load_level(levelname))

            camera.update(player)
            for sprite in platforms:
                camera.apply(sprite)
                sprite.image.set_alpha(225)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_LEFT]:
                        left, right = True, False
                    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                        left, right = False, True
                    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        screens.pause_screen()
                elif event.type == pygame.KEYUP:
                    left, right = False, False

            player.update(left, right, platforms)
            all_sprites.draw(screen)
            clock.tick(APP_CFG['fps'])
            pygame.display.flip()

    def lose_screen(self, jumps):
        functions.play_sound('lose.mp3', 1, 0, 1500)
        functions.show_image('lose_image.png')
        self.display_jumps(jumps, 'white')
        self.main_game_screen(self.menu_click_waiter())

    def win_screen(self, jumps):
        functions.play_sound('coin.mp3', 0, 0, 2500)
        functions.show_image('win_image.png')
        self.display_jumps(jumps, 'black')
        self.main_game_screen(self.menu_click_waiter())

    def pause_screen(self):
        functions.show_image('level_background.png')
        font = pygame.font.SysFont("8-BIT WONDER.TTF", 30)
        text = font.render("Press Esc to exit", True, 'white')
        exit_coords = (235, 75)
        screen.blit(text, exit_coords)
        self.menu_click_waiter()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(platforms)
        tile_width, tile_height = APP_CFG['width'] / 10, APP_CFG['height'] / 10
        tile_levels, tile_levels_visible = APP_CFG['tile_levels'], APP_CFG['tile_levels_visible']
        self.tile_type = tile_type
        tile_images = {
            'earth1': 'earth1.png',
            'earth2': 'earth2.png',
            'earth3': 'earth3.png',
            'earth4': 'earth4.png',
            'c': 'coin.png',
            'empty': 'grass.png'
        }

        self.tilesprite = pygame.sprite.Sprite()
        self.image = functions.load_image(tile_images[self.tile_type])
        self.rect = self.image.get_rect()

        # проверяем, должна ли платформа находится на экране и, если да, рисуем её
        if pos_y < (tile_levels - tile_levels_visible - 1):
            self.rect.x = tile_width * pos_x
            self.rect.y = tile_height * (pos_y - (tile_levels - tile_levels_visible - pos_y))
        else:
            self.rect.x = tile_width * pos_x
            self.rect.y = tile_height * (pos_y - (tile_levels - tile_levels_visible))


class Camera:
    def __init__(self):
        self.dx, self.dy = 0, 0

    def apply(self, obj):
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dy = -(target.rect.y + target.rect.h // 2 - APP_CFG['height'] // 4 - 128)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = functions.load_image('santa.png')
        self.rect = self.image.get_rect()
        self.rect.x += pos_x
        self.rect.y += pos_y
        self.dx, self.dy = 0, 0
        self.direction = 'right'

        self.jumps = 0

    def update(self, left, right, platforms):
        self.collide(platforms)
        self.check_win(coins)
        if left:
            self.dx -= 1
            if self.direction != 'left':
                self.direction = 'left'
                self.image = pygame.transform.flip(self.image, True, False)
        elif right:
            self.dx += 1
            self.direction = 'right'
            self.image = functions.load_image('santa.png')

        if not (left or right):
            if self.dx > 4:
                self.dx /= 2
            else:
                self.dx = 0

        # ускорение свободного падения
        self.dy += 1.5
        # такую большую скорость можно набрать только упав, тогда мы проиграли
        if self.dy > 50:
            screens.lose_screen(self.jumps)
        # обновляем координаты
        self.rect.y += self.dy
        self.rect.x += self.dx
        # при выходе за рамки экрана появляемся с другой стороны
        if self.rect.x > 640:
            self.rect.x -= 630
        elif self.rect.x < 0:
            self.rect.x += 650

    def collide(self, platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i):
                # проверяем, упали мы на платформу или летим снизу
                if self.dy > 0:
                    # если мы летели сверху, то должны отскочить
                    if self.rect.y + 64 <= i.rect.y:
                        self.dy = -20
                        # был совершен прыжок
                        self.jumps += 1
                        functions.play_sound("jump.mp3")

    def check_win(self, items):
        for item in items:
            if pygame.sprite.collide_rect(self, item):
                screens.win_screen(self.jumps)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    functions = CoreFunctions()

    with open('app_cfg.json') as cfg_file:
        APP_CFG = json.load(cfg_file)
        pygame.display.set_caption(APP_CFG['title'])
        screen = pygame.display.set_mode([APP_CFG['width'], APP_CFG['height']])

    screens = Screens()
    screens.main_game_screen(screens.start_screen())
    functions.terminate()
