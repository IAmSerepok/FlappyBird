import math
import random as rand
import pygame as pg
import os


class Bird(pg.sprite.Sprite):

    def __init__(self):

        self.wings_position = 0
        self.start_pos_num = 0
        self.start_poses = [-1, -1, -1, -1, -1, -1, -1, -1,
                            1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1,
                            -1, -1, -1, -1, -1, -1, -1, -1]
        self.position = [screen_width/2 - 30, screen_height/2]
        self.wings_frames = [1, 2, 1, 0]
        self.speed = 0
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(bird_animation_folder, "bird_1.png")).convert()
        self.image.set_colorkey((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def rotate(self, angle):

        self.image = pg.image.load(os.path.join(bird_animation_folder, "bird_" + str(
            bird.wings_frames[bird.wings_position]) + ".png")).convert()
        self.image.set_colorkey((0, 255, 0))
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def fly(self, angle):

        self.wings_position = (self.wings_position + 1) % 4
        if game_stage == 1:
            self.rotate(angle)


class Ground(pg.sprite.Sprite):

    def __init__(self):

        self.frame_num = 0
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(ground_animation_folder, "ground_0.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, screen_height)

    def update(self):

        self.frame_num = (self.frame_num + 1) % 6
        self.image = pg.image.load(os.path.join(ground_animation_folder, "ground_" + str(self.frame_num) + ".png")).convert()


class Pipe(pg.sprite.Sprite):

    def __init__(self, pos):

        type = rand.randint(0, 12)
        self.is_passed = False
        self.hitbox = [100 + 20*(type+1) - delta_y, 100 + 20*(type+1) + delta_y + 200]
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(pipe_textures_folder, "pipe_" + str(type) + ".png")).convert()
        self.image.set_colorkey((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos, 0

    def update(self, bird, counter):

        self.rect.x -= 4

        if ((bird.rect.bottomright[0] >= self.rect.x + delta_x) & (bird.rect.bottomright[0] <= self.rect.bottomright[0] - delta_x))|((bird.rect.x >= self.rect.x + delta_x) & (bird.rect.x <= self.rect.bottomright[0] - delta_x)):
            if (bird.rect.bottomright[1] > self.hitbox[1]) | (bird.rect.y < self.hitbox[0]):
                if bird.speed < 0:
                    bird.speed = 0
                global game_stage
                game_stage = 3
                pg.time.set_timer(WINGS, 0)
                pg.time.set_timer(PIPES_MOVE, 0)
                pg.time.set_timer(GROUND_MOVE, 0)
                pg.time.set_timer(GENERATE_PIPES, 0)

        if (self.is_passed is False) & (self.rect.center[0] > bird.position[0] - 68/2) & (self.rect.center[0] < bird.position[0] + 68/2):
            self.is_passed = True
            counter.update(counter.score + 1)

class Background(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(data_folder, "background_0.jpg")).convert()
        self.rect = self.image.get_rect()
        self.bottomleft = (0, screen_height)


class ScoreNumber(pg.sprite.Sprite):

    def __init__(self, number, center_x):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(score_numbers_folder, "number_" + str(number) + ".png")).convert()
        self.image.set_colorkey((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, 150)


class ScoreCounter:

    def __init__(self, group_):

        self.group = group_
        self.score = 0
        self.numbers = []
        number = ScoreNumber(0, screen_width/2)
        group_.add(number)
        self.numbers.append(number)

    def update(self, score_):

        self.score = score_
        for numb in self.numbers:
            numb.kill()
        self.numbers = []
        sub_numbers = []
        sub = score_
        dx = screen_width/2
        while sub > 0:
            sub_numbers.append(sub % 10)
            sub //= 10
        sub_numbers.reverse()
        dx -= len(sub_numbers) // 2 * 48
        if len(sub_numbers) % 2 == 0:
            dx += 48 / 2
        for _ in range(len(sub_numbers)):
            numb = ScoreNumber(sub_numbers[_], dx + _ * 48)
            self.group.add(numb)
            self.numbers.append(numb)


class MiniScoreNumber(pg.sprite.Sprite):

    def __init__(self, number, center_):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(score_numbers_folder, "number_mini_" + str(number) + ".png")).convert()
        self.image.set_colorkey((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = center_


class MiniScoreCounter:

    def __init__(self, group_, y_):

        self.group = group_
        self.numbers = []
        number = MiniScoreNumber(0, (screen_width/2, y_))
        self.group.add(number)
        self.numbers.append(number)

    def update(self, score_, y_):

        if score_ == 0:

            for numb in self.numbers:
                numb.kill()
            self.numbers = []
            number = MiniScoreNumber(0, (screen_width / 2, y_))
            self.group.add(number)
            self.numbers.append(number)

        else:
            for numb in self.numbers:
                numb.kill()
            self.numbers = []
            sub_numbers = []
            sub = score_
            dx = screen_width/2
            while sub > 0:
                sub_numbers.append(sub % 10)
                sub //= 10
            sub_numbers.reverse()
            dx -= len(sub_numbers) // 2 * 36
            if len(sub_numbers) % 2 == 0:
                dx += 36 / 2
            for _ in range(len(sub_numbers)):
                numb = MiniScoreNumber(sub_numbers[_], (dx + _ * 36, y_))
                self.group.add(numb)
                self.numbers.append(numb)


class Menu(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(data_folder, "menu.png")).convert()
        self.image.set_colorkey((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, 350)


class RestartButton(pg.sprite.Sprite):

    def __init__(self):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(data_folder, "restart_button.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, 550)


#мировые константы
g = 1000 #ускорения свободного падения(пикс./сек.)
dt = 0.015 #шаг дискретизации времени
normalizing_vector = 150 # нормаль для вычисления угла
delta_x, delta_y = 23, 10 #допуск

#окно
pg.init()
pg.display.set_caption("Flappy bird")

#директории
game_folder = os.path.dirname(__file__)
data_folder = os.path.join(game_folder, "data")
bird_animation_folder = os.path.join(data_folder, "bird_frames")
ground_animation_folder = os.path.join(data_folder, "ground_frames")
pipe_textures_folder = os.path.join(data_folder, "pipe_textures")
score_numbers_folder = os.path.join(data_folder, "score_number_textures")

#параметры экрана/настройки игры
screen_size = screen_width, screen_height = 600, 780
screen = pg.display.set_mode(screen_size)

background_sprites = pg.sprite.Group()
other_sprites = pg.sprite.Group()
pipe_sprites = pg.sprite.Group()
counter_sprites = pg.sprite.Group()
menu_sprites = pg.sprite.Group()

bird = Bird()
ground = Ground()
other_sprites.add(bird)
other_sprites.add(ground)
background_sprites.add(Background())
counter = ScoreCounter(counter_sprites)
menu_counter = MiniScoreCounter(menu_sprites, 310)
highscore_counter = MiniScoreCounter(menu_sprites, 420)
menu_sprites.add(Menu())
menu_sprites.add(RestartButton())

pipe_list = []

pipe1 = Pipe(1050)
pipe_sprites.add(pipe1)
pipe_list.append(pipe1)
pipe2 = Pipe(650)
pipe_sprites.add(pipe2)
pipe_list.append(pipe2)

#считываем лучший результат
file = open(os.path.join(data_folder, "highscore.txt"), "r")
highscore = int(file.readline())
file.close()

fps = 60
game_stage = 1  # 1 - В ожидании 1 клика
                # 2 - Игра
                # 3 - Попадание в столб/землю
                # 4 - Меню

clock = pg.time.Clock()

WINGS = pg.USEREVENT + 1
PHYSICAL_CALCULATIONS = pg.USEREVENT + 2
PIPES_MOVE = pg.USEREVENT + 3
GROUND_MOVE = pg.USEREVENT + 4
GENERATE_PIPES = pg.USEREVENT + 5
START_BIRD_ANIMATION = pg.USEREVENT + 6

pg.time.set_timer(WINGS, 100)
pg.time.set_timer(START_BIRD_ANIMATION, 20)
pg.time.set_timer(GROUND_MOVE, int(1000 * dt))

while game_stage >= 0:

    clock.tick(fps)

    for event in pg.event.get():

        if event.type == pg.MOUSEBUTTONDOWN:

            if game_stage == 1:
                bird.speed = -400
                pg.time.set_timer(START_BIRD_ANIMATION, 0)
                pg.time.set_timer(WINGS, 100)
                pg.time.set_timer(PIPES_MOVE, int(1000 * dt))
                pg.time.set_timer(PHYSICAL_CALCULATIONS, int(1000 * dt))
                pg.time.set_timer(GENERATE_PIPES, 1500)
                game_stage = 2

            if game_stage == 2:
                bird.speed = -400

            if game_stage == 4:
                if (event.pos[0] >= 190) & (event.pos[0] <= 411) & (event.pos[1] >= 520) & (event.pos[1] <= 580):
                    game_stage = 1
                    bird.kill()
                    bird = Bird()
                    other_sprites.add(bird)
                    counter.update(0)
                    pipe_list = []
                    pipe_sprites = pg.sprite.Group()
                    pipe1 = Pipe(1050)
                    pipe_sprites.add(pipe1)
                    pipe_list.append(pipe1)
                    pipe2 = Pipe(650)
                    pipe_sprites.add(pipe2)
                    pipe_list.append(pipe2)

                    pg.time.set_timer(WINGS, 100)
                    pg.time.set_timer(START_BIRD_ANIMATION, 20)
                    pg.time.set_timer(GROUND_MOVE, int(1000 * dt))

        if event.type == START_BIRD_ANIMATION:
            bird.start_pos_num = (bird.start_pos_num + 1) % len(bird.start_poses)
            bird.position[1] += bird.start_poses[bird.start_pos_num]

        if event.type == WINGS:

            angle = math.atan(bird.speed / normalizing_vector)
            angle *= 180 / math.pi
            if angle < -25:
                angle = -25
            bird.fly(-angle)

        if event.type == PIPES_MOVE:
            pipe_sprites.update(bird, counter)

        if event.type == GROUND_MOVE:
            ground.update()

        if event.type == GENERATE_PIPES:

            pipe = Pipe(650)
            pipe_sprites.add(pipe)
            pipe_list[0].kill()
            pipe_list.pop()
            pipe_list.append(pipe)

        if event.type == PHYSICAL_CALCULATIONS:

            bird.speed += dt * g
            bird.rect.y += dt * bird.speed
            bird.position[1] += dt * bird.speed

            if bird.rect.center[1] < -100:
                bird.rect.center = (bird.rect.center[0], -99)
                bird.position[1] = -99

            angle = math.atan(bird.speed/normalizing_vector)
            angle *= 180/math.pi
            if angle < -25:
                angle = -25
            bird.rotate(-angle)

        if event.type == pg.QUIT:
            pg.quit()

    if bird.position[1] > 675:
        game_stage = 3
        bird.position[1] = 675
        pg.time.set_timer(WINGS, 0)
        pg.time.set_timer(PIPES_MOVE, 0)
        pg.time.set_timer(GROUND_MOVE, 0)
        pg.time.set_timer(PHYSICAL_CALCULATIONS, 0)
        pg.time.set_timer(GENERATE_PIPES, 0)
        game_stage = 4

    screen.fill("gray")
    background_sprites.draw(screen)
    pipe_sprites.draw(screen)
    other_sprites.draw(screen)
    if (game_stage == 3) | (game_stage == 4):
        menu_counter.update(counter.score, 310)
        if counter.score > highscore:
            file = open(os.path.join(data_folder, "highscore.txt"), "w")
            highscore = counter.score
            file.write(str(highscore))
            file.close()
        highscore_counter.update(highscore, 420)
        menu_sprites.draw(screen)
    if (game_stage == 2) | (game_stage == 1):
        counter_sprites.draw(screen)
    pg.display.flip()
