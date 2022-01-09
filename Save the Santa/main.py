import pygame
from random import randint
from sprite import *

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()

def load_image(name):
    fullname = os.path.join('data', 'images', name)
    image = pygame.image.load(fullname)
    return image


def start_screen():
    pygame.mixer.music.load("data\sounds\menu.mp3")
    pygame.mixer.music.play(-1, 0, 500)

    start_image = pygame.transform.scale(load_image('start_image.png'), (WIDTH, HEIGHT))
    screen.blit(start_image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)
    

def main_game():
    #pygame.mixer.music.load("data\sounds\main.mp3")
    #pygame.mixer.music.play(-1, 0, 1000)

    running = True
    while running:
        generate_background(load_image('level background.png'))
        generate_level(load_level('level.txt'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        pygame.display.flip()
    

def generate_background(background):
    screen.blit(background, (0, 0))
  

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        tile_width = WIDTH / 10
        tile_height = HEIGHT / 10
        tile_levels = 11
        tile_levels_visible = 9
        tile_images = {
        'earth1': 'earth1.png',
        'earth2': 'earth2.png',
        'earth3': 'earth3.png',
        'earth4': 'earth4.png',
        'empty': 'grass.png'
        }
        if pos_y < (tile_levels - tile_levels_visible - 1):
            self.coords = tile_width * pos_x, tile_height * (pos_y - (tile_levels - tile_levels_visible - pos_y))
        else:
            self.coords = tile_width * pos_x, tile_height * (pos_y - (tile_levels - tile_levels_visible))

        self.image = load_image(tile_images[tile_type])
        screen.blit(self.image, self.coords)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('earth1', x, y)
            elif level[y][x] == '2':
                Tile('earth2', x, y)
            elif level[y][x] == '3':
                Tile('earth3', x, y)
            elif level[y][x] == '4':
                Tile('earth4', x, y)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Save the Santa')
    size = WIDTH, HEIGHT = 640, 960
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    WHITE = (242, 240, 229)
    FPS = 60
    #start_screen()
    main_game()   
    pygame.quit()
