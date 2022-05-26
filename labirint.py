# Разрfrom telnetlib import G
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
        if packman.rect.x <= window_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= window_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

class Enemy(GameSprite):
    def __init__(self, enemy_image, enemy_x, enemy_y, enemy_size_x, enemy_size_y, enemy_speed):
        GameSprite().__init__(self, enemy_image, enemy_x, enemy_y, enemy_size_x, enemy_size_y)

        self.speed = enemy_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= window_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


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
        packman.update()
        monster.update()

        packman.reset()
        monster.reset()

        barriers.draw(window)
        final_sprite.reset()
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