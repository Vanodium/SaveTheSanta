import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def show_image(name):
    start_image = pygame.transform.scale(load_image(name), (WIDTH, HEIGHT))
    screen.blit(start_image, (0, 0))


def waiting_click():
    # фунция нужна чтобы отображать одну картинку, пока не будет нажата кнопка мыши
    while True:
        for event in pygame.event.get():
            global levelname
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                levelname = 'level.txt'
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                levelname = 'level1.txt'
                return
            elif event.type == pygame.KEYDOWN:
                if pygame.K_ESCAPE:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name):
    fullname = os.path.join('Save the Santa', 'data', 'images', name)
    image = pygame.image.load(fullname)
    return image


def main_game():
    pygame.mixer.music.load("Save the Santa\data\sounds\main.mp3")
    pygame.mixer.music.play(-1, 0, 1000)

    clock = pygame.time.Clock()

    global platforms, all_sprites, coins
    # группа с монетками
    coins = pygame.sprite.Group()
    # стартовые координаты игрока
    playerx, playery = 200, 550
    player = Player(playerx, playery)
    # пока никуда не двигаемся
    left = right = False

    # создаём камеру
    camera = Camera()
    
    running = True
    while running:
        # группа с летающими платформами
        platforms = pygame.sprite.Group()
        # группа со всеми спрайтами
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        # генерируем фон
        background_y = camera.apply_background() - 728
        generate_background(load_image('level background.png'), (0, background_y))
        
        # генерируем уровень, который грузим из текстового файла
        generate_level(load_level(levelname))
        
        # изменяем ракурс камеры
        camera.update(player)
        
        # обновляем положение всех спрайтов
        for sprite in platforms:
            camera.apply(sprite)
            sprite.image.set_alpha(225)

        player.image.set_alpha(225)

        # в зависимости от нажатых кнопок будем изменять положение игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    left = True
                    right = False
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    right = True
                    left = False
                elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    screens.pause_screen()
            elif event.type == pygame.KEYUP:
                left = right = False

        # в зависимости от нажатых кнопок изменяем положение игрока
        player.update(left, right, platforms)
        # отрисовываем всё на экране
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


def show_jumps(jumps, color):
    font = pygame.font.SysFont("8-BIT WONDER.TTF", 30)
    jumps_text = "you've made " + str(jumps) + " jumps"
    text = font.render(jumps_text, True, color)
    coords = (215, 75)
    screen.blit(text, coords)


def generate_background(background, coords):
    screen.fill('black')
    screen.blit(background, coords)


def load_level(filename):
    filename = "Save the Santa/data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    # добавляем в группу, которую будем отрисовывать и свою группу, которую будем проверять на столкновение с персонажем
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in '1234':
                platforms.add(Tile('earth' + level[y][x], x, y))
                all_sprites.add(Tile('earth' + level[y][x], x, y))
            elif level[y][x] == 'c':
                coins.add(Tile('c', x, y))
                all_sprites.add(Tile('c', x, y))


class Screens:
    def start_screen(self):
        # включаем музыку и отображаем заставку, пока не будет нажата кнопка мыши
        pygame.mixer.music.load("Save the Santa\data\sounds\menu.mp3")
        pygame.mixer.music.play(-1, 0, 1500)
        show_image('start_image.png')
        waiting_click()

    def lose_screen(self, jumps):
        pygame.mixer.music.load("Save the Santa\data\sounds\lose.mp3")
        pygame.mixer.music.play(1, 0, 1500)
        
        show_image('lose_image.png')
        show_jumps(jumps, 'white')
        waiting_click()
        main_game()
        
    def win_screen(self, jumps):
        pygame.mixer.Sound("Save The Santa\data\sounds\coin.mp3").play()
        pygame.mixer.music.load("Save the Santa\data\sounds\win.mp3")
        pygame.mixer.music.play(-1, 0, 2500)
        show_image('win_image.png')
        show_jumps(jumps, 'black')
        waiting_click()
        main_game()

    def pause_screen(self):
        # картинка с текстом, которая отображается при нажатии Esc (пауза)
        show_image('level background.png')
        font = pygame.font.SysFont("8-BIT WONDER.TTF", 30)
        
        text = font.render("Press Esc to exit", True, 'white')
        exit_coords = (235, 75)
        screen.blit(text, exit_coords)
        
        if levelname == 'level.txt':
            txt = "Press LMB to resume"
        else:
            txt = "Press RMB to resume"

        text = font.render(txt, True, 'white')
        resume_coords = (217, 100)
        screen.blit(text, resume_coords)

        waiting_click()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(platforms)

        tile_width = WIDTH / 10
        tile_height = HEIGHT / 10
        tile_levels = 12
        tile_levels_visible = 9
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
        self.image = load_image(tile_images[self.tile_type])
        self.rect = self.image.get_rect()

        # проверяем, должна ли платформа находится на экране и, если да, рисуем её 
        if pos_y < (tile_levels - tile_levels_visible - 1):
            self.rect.x = tile_width * pos_x
            self.rect.y = tile_height * (pos_y - (tile_levels - tile_levels_visible - pos_y))
        else:
            self.rect.x = tile_width * pos_x
            self.rect.y = tile_height * (pos_y - (tile_levels - tile_levels_visible))


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    # сдвинуть объект object на смещение камеры
    def apply(self, object):
        object.rect.y += self.dy
    
    def apply_background(self):
        return self.dy# // 2
    
    # позиционировать камеру на объекте target
    def update(self, target):
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 4 - 128)
    

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        # ускорение персонажа = 0
        self.vx = 0
        self.vy = 0

        # переменная нужна чтобы отображать отзеркаленную картинку при движении в противоположном направлении
        self.direction = 'right'

        if self.direction == 'right':
            self.image = load_image('santa.png')
        self.rect = self.image.get_rect()

        self.rect.x += pos_x
        self.rect.y += pos_y
        # еще не было совершено прыжков
        self.jumps = 0


    def update(self, left, right, platforms):
        self.collide(platforms)
        # проверка на соприкосновение с монеткой
        self.check_win(coins)
        # перемещение по x
        if left is True:
            self.vx -= 1
            if self.direction != 'left':
                self.direction = 'left'
                self.image = pygame.transform.flip(self.image, True, False)
        elif right is True:
            self.vx += 1
            self.direction = 'right'
            self.image = load_image('santa.png')   
            
        # остановка по x
        if not left and not right:
            if self.vx > 4:
                self.vx /= 2
            else:
                self.vx = 0

        # ускорение свободного падения
        self.vy += 1.5
        # такую большую скорость можно набрать только упав, тогда мы проиграли
        if self.vy > 50:
            screens.lose_screen(self.jumps)
        # обновляем координаты
        self.rect.y += self.vy
        self.rect.x += self.vx
        # при выходе за рамки экрана появляемся с другой стороны
        if self.rect.x > 640:
            self.rect.x -= 630
        elif self.rect.x < 0:
            self.rect.x += 650

    def collide(self, platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i):
                # проверяем, упали мы на платформу или летим снизу
                if self.vy > 0:
                    # если мы летели сверху, то должны отскочить
                    if self.rect.y + 64 <= i.rect.y:
                        self.vy = -20
                        # был совершен прыжок
                        self.jumps += 1
                        pygame.mixer.Sound("Save The Santa\data\sounds\jump.mp3").play()
    
    def check_win(self, items):
        for item in items:
            if pygame.sprite.collide_rect(self, item):
                screens.win_screen(self.jumps)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Save the Santa')
    size = WIDTH, HEIGHT = 640, 960
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    screens = Screens()
    screens.start_screen()
    main_game()   
    pygame.quit()
