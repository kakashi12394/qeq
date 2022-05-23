# Разрfrom telnetlib import GA
from importlib.util import find_spec
from pickle import FALSE
from telnetlib import GA
from turtle import back
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed




window_width = 700
window_height = 500

window = display.set_mode((window_width, window_height))
picture = transform.scale(image.load('fields.png'), (700, 500))
display.set_caption('Лабиринт')

barriers = sprite.Group()


w1 = GameSprite('wall.png', window_width / 2 - window_width / 3, window_height / 2, 300, 50)
w2 = GameSprite('wall.png', 370, 100, 50, 400)

barriers.add(w1)
barriers.add(w2)

packman = Player('pac-5.png', 5, window_height - 80, 80, 80, 0, 0)
monster = GameSprite('pac-6.png', window_width - 80, 180, 80, 80)
final_sprite = GameSprite('coin.png', window_width - 85, window_height - 100, 80, 80)

finish = False
run = True
while run:
    window.blit(picture, (0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
        elif e.type == KEYUP:
           if e.key == K_LEFT :
               packman.x_speed = 0
           elif e.key == K_RIGHT:
               packman.x_speed = 0 
           elif e.key == K_UP:
               packman.y_speed = 0
           elif e.key == K_DOWN:
               packman.y_speed = 0

    if not finish:
        window.fill((119, 210, 223))
        w1.reset()
        w2.reset()
        barriers.draw(window)
    
        monster.reset()
        final_sprite.reset()
        packman.reset()
        packman.update()
        if sprite.collide_rect(packman, monster):
            finish = True
            img = image.load('game-over_1.png',)
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_height * d, window_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0,0))
    display.update()
    time.delay(50)