import pygame
import random
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 650, 750
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Field:
    def __init__(self, field):
        self.field = field

    def cell(self, x, y):
        return int(x / tile_width), int(y / tile_height)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self.tile_type = tile_type


class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (tile_width - 2, tile_height - 2))
        self.img = self.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self.speed = 1
        self.cur_dir = None
        self.next_dir = None
        self.cur_cell = field.cell(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)
        self.check_cells = None

    def set_check_cells(self, x, y):
        self.check_cells = [list(tiles_group)[(self.cur_cell[1] - 1) * (x + 1) + (self.cur_cell[0] - 1):(self.cur_cell[1] - 1) * (x + 1) + self.cur_cell[0] + 2],
                            list(tiles_group)[(self.cur_cell[1]) * (x + 1) + (self.cur_cell[0] - 1):(self.cur_cell[1]) * (x + 1) + self.cur_cell[0] + 2],
                            list(tiles_group)[(self.cur_cell[1] + 1) * (x + 1) + (self.cur_cell[0] - 1):(self.cur_cell[1] + 1) * (x + 1) + self.cur_cell[0] + 2]]
        '''print(self.rect)
        for i in self.check_cells:
            for s in i:
                print(s.rect)
        # print(self.check_cells)'''


    def turn(self, dir):
        global x, y
        if dir == 'r':
            if self.check_cells[1][2].tile_type == 'wall':
                return False
            self.image = self.img
        if dir == 'l':
            if self.check_cells[1][0].tile_type == 'wall':
                return False
            self.image = pygame.transform.rotate(self.img, 180)
        if dir == 'u':
            if self.check_cells[0][1].tile_type == 'wall':
                return False
            self.image = pygame.transform.rotate(self.img, 90)
        if dir == 'd':
            if self.check_cells[2][1].tile_type == 'wall':
                return False
            self.image = pygame.transform.rotate(self.img, -90)
        if dir is not None:
            return True

    def move(self, dir):
        if dir == 'r':
            self.rect = self.rect.move(self.speed, 0)
        elif dir == 'l':
            self.rect = self.rect.move(-self.speed, 0)
        elif dir == 'u':
            self.rect = self.rect.move(0, -self.speed)
        elif dir == 'd':
            self.rect = self.rect.move(0, self.speed)

    def stop(self, dir):
        if dir == 'r' and self.check_cells[1][2].tile_type == 'wall':
            self.cur_dir = None
        elif dir == 'l' and self.check_cells[1][0].tile_type == 'wall':
            self.cur_dir = None
        elif dir == 'u' and self.check_cells[0][1].tile_type == 'wall':
            self.cur_dir = None
        elif dir == 'd' and self.check_cells[2][1].tile_type == 'wall':
            self.cur_dir = None

    def update(self):
        global x, y
        map_x, map_y = field.cell(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)
        if (map_x, map_y) != self.cur_cell:
            self.cur_cell = (map_x, map_y)
            self.set_check_cells(x, y)
        if self.check_cells[1][1].rect.centerx - 1 <= self.rect.centerx <= self.check_cells[1][1].rect.centerx + 1 and\
                self.check_cells[1][1].rect.centery - 1 <= self.rect.centery <= self.check_cells[1][1].rect.centery + 1:
            if self.turn(self.next_dir):
                self.cur_dir, self.next_dir = self.next_dir, None
            self.stop(self.cur_dir)
        self.move(self.cur_dir)
        tile = list(tiles_group)[map_y * (x + 1) + map_x]
        if tile.tile_type == 'tile_point':
            tile.tile_type = 'tile_empty'
            tile.image = pygame.transform.scale(tile_images[tile.tile_type], (tile_width, tile_height))
            draw(tiles_group)
        # print(field.cell(self.rect.x, self.rect.y))


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[name], (tile_width, tile_height))
        self.img = self.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self.speed = 1
        self.next_dir = None
        self.possible_dirs = []
        self.cur_dir = None
        self.cur_cell = field.cell(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)
        self.check_cells = None

    def set_check_cells(self, x, y):
        self.check_cells = [list(tiles_group)[(self.cur_cell[1] - 1) * (x + 1) + (self.cur_cell[0] - 1):(self.cur_cell[1] - 1) * (x + 1) + self.cur_cell[0] + 2],
                            list(tiles_group)[(self.cur_cell[1]) * (x + 1) + (self.cur_cell[0] - 1):(self.cur_cell[1]) * (x + 1) + self.cur_cell[0] + 2],
                            list(tiles_group)[(self.cur_cell[1] + 1) * (x + 1) + (self.cur_cell[0] - 1):(self.cur_cell[1] + 1) * (x + 1) + self.cur_cell[0] + 2]]

    def change_dir(self):
        opposites = {'l': 'r', 'r': 'l', 'u': 'd', 'd': 'u'}
        if self.cur_dir is not None:
            if len(self.possible_dirs) > 1:
                try:
                    d = self.possible_dirs.pop(self.possible_dirs.index(opposites[self.cur_dir]))
                    o = self.possible_dirs.pop(self.possible_dirs.index(opposites[d]))
                except ValueError:
                    pass
        try:
            self.cur_dir = random.choice(self.possible_dirs)
        except IndexError:
            self.cur_dir = o

    def set_possible_dirs(self):
        self.possible_dirs = []
        if self.check_cells[1][2].tile_type != 'wall':
            self.possible_dirs.append('r')
        if self.check_cells[1][0].tile_type != 'wall':
            self.possible_dirs.append('l')
        if self.check_cells[0][1].tile_type != 'wall':
            self.possible_dirs.append('u')
        if self.check_cells[2][1].tile_type != 'wall':
            self.possible_dirs.append('d')

    def move(self, dir):
        if dir == 'r':
            self.rect = self.rect.move(self.speed, 0)
        elif dir == 'l':
            self.rect = self.rect.move(-self.speed, 0)
        elif dir == 'u':
            self.rect = self.rect.move(0, -self.speed)
        elif dir == 'd':
            self.rect = self.rect.move(0, self.speed)

    def update(self):
        global x, y, pacman, running
        map_x, map_y = field.cell(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)
        if (map_x, map_y) != self.cur_cell:
            self.cur_cell = (map_x, map_y)
        self.set_check_cells(x, y)
        if self.check_cells[1][1].rect.centerx <= self.rect.centerx <= self.check_cells[1][1].rect.centerx and\
                self.check_cells[1][1].rect.centery <= self.rect.centery <= self.check_cells[1][1].rect.centery:
            self.set_possible_dirs()
            self.change_dir()
        self.move(self.cur_dir)
        if map_x == pacman.cur_cell[0] and map_y == pacman.cur_cell[1]:
            game_over_screen()


def generate_level(level):
    new_player, x, y, pinky, inky, clyde, blinky = None, None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('tile_point', x, y)
            elif level[y][x] == 'O':
                Tile('tile_point_big', x, y)
            elif level[y][x] == '_':
                Tile('tile_empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('tile_empty', x, y)
                new_player = PacMan(x, y)
            elif level[y][x] == 'P':
                Tile('tile_empty', x, y)
                pinky = Ghost(x, y, 'pinky')
            elif level[y][x] == 'I':
                Tile('tile_empty', x, y)
                inky = Ghost(x, y, 'inky')
            elif level[y][x] == 'C':
                Tile('tile_empty', x, y)
                clyde = Ghost(x, y, 'clyde')
            elif level[y][x] == 'B':
                Tile('tile_empty', x, y)
                blinky = Ghost(x, y, 'blinky')
    return new_player, x, y, pinky, inky, clyde, blinky


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # max_width = max(map(len, level_map))
    max_width = WIDTH // tile_width
    for _ in range(HEIGHT // tile_height - len(level_map)):
        level_map.append('.')

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def draw(group):
    global Canvas
    group.draw(Canvas)


# print(load_level('map.txt'))

running = True
FPS = 150
counter = 0
Canvas = pygame.Surface(size)
tile_width = tile_height = 23
clock = pygame.time.Clock()

tile_images = {
    'wall': load_image('block.png'),
    'tile_empty': load_image('ground1.png'),
    'tile_point': load_image('ground_point.png'),
    'tile_point_big': load_image('ground_point_big.png'),
    'blinky': load_image('blinky.png'),
    'clyde': load_image('clyde.png'),
    'inky': load_image('inky.png'),
    'pinky': load_image('pinky.png'),
}
player_image = load_image('pacman.png')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

m = load_level('map_classic.txt')
field = Field(m)
pacman, x, y, pinky, inky, clyde, blinky = generate_level(m)
pacman.set_check_cells(x, y)
print(len(list(tiles_group)), x, y)
tiles_group.draw(Canvas)


def start_screen():
    intro_text = ["ZASTAVKA"]

    fon = pygame.transform.scale(load_image('bg_start_screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen():
    global all_sprites, tiles_group, player_group, field, pacman, x, y, pinky, inky, clyde, blinky
    intro_text = ["GAME OVER!"]

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    m = load_level('map_classic.txt')
    field = Field(m)
    pacman, x, y, pinky, inky, clyde, blinky = generate_level(m)
    pacman.set_check_cells(x, y)
    print(len(list(tiles_group)), x, y)
    tiles_group.draw(Canvas)

    fon = pygame.transform.scale(load_image('bg_start_screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.KEYDOWN:
            dir = None
            if event.key == pygame.K_LEFT:
                dir = 'l'
            if event.key == pygame.K_RIGHT:
                dir = 'r'
            if event.key == pygame.K_UP:
                dir = 'u'
            if event.key == pygame.K_DOWN:
                dir = 'd'
            pacman.next_dir = dir
            # pacman.move(dir)

    # all_sprites.draw(screen)
    if counter % 3 == 0:
        # screen.fill(pygame.Color('black'))
        screen.blit(Canvas, (0, 0))
        player_group.draw(screen)
        pygame.display.flip()
    player_group.update()
    clock.tick(FPS)
    counter += 1

pygame.quit()
