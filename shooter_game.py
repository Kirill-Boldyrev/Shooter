#Создай собственный Шутер!

from pygame import *
import random
from time import time as timer
init()
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.music.load('space.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()
shoot = mixer.Sound('fire.ogg')
lost = 0
#!базовый класс GameSprite.
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#TODO класс Игрока в игре <<Шутер>>
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 4)
        bullets.add(bullet)
#? класс Врага в игре <<Шутер>>
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = random.randint(1, 500)
#* класс Пуля в игре <<Шутер>>
class Bullet(GameSprite):
    def update(self):
         self.rect.y -= self.speed
         if self.rect.y <= 0:
             self.kill()

class Asteroids(GameSprite):
    def update(self):
        global lives
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = random.randint(1, 500)
playe1 = Player('rocket.png', 50, 425, 5)
enem1 = Enemy('ufo.png', 350, random.randint(-5, 0), random.randint(1, 3))
enem2 = Enemy('ufo.png', 250, random.randint(-5, 0), random.randint(1, 3))
enem3 = Enemy('ufo.png', 150, random.randint(-5, 0), random.randint(1, 3))
enem4 = Enemy('ufo.png', 50, random.randint(-5, 0), random.randint(1, 3))
enem5 = Enemy('ufo.png', 450, random.randint(-5, 0), random.randint(1, 3))
asteroid1 = Asteroids('asteroid.png', 175, random.randint(-5, 0), random.randint(1, 3))
asteroid2 = Asteroids('asteroid.png', 248, random.randint(-5, 0), random.randint(1, 3))
asteroid3 = Asteroids('asteroid.png', 389, random.randint(-5, 0), random.randint(1, 3))
monsters = sprite.Group()
monsters.add(enem1)
monsters.add(enem2)
monsters.add(enem3)
monsters.add(enem4)
monsters.add(enem5)
bullets = sprite.Group()
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)


finish = False
win =  0
live = 3
num_fire = 0
rel_time = False
font1 = font.SysFont('Arial', 26)
text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 252))
font2 = font.SysFont('Arial', 26)
text_win = font1.render('Счёт:' + str(win), 1, (255, 255, 252))
font4 = font.SysFont('Arial', 36)
lost2 = font4.render('YOU LOST!', True, (250, 150, 50))
font5 = font.SysFont('Arial', 36)
lives = font5.render('Жизни:' + str(live), True, (255, 255, 252))
clock = time.Clock()
FPS = 60
run = True
while run:
    if finish != True:
        window.blit(background,(0, 0))
        playe1.reset()
        playe1.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides2 = sprite.spritecollide(playe1, asteroids, True)
        if collides2:
            live -= 1
            lives = font5.render('Жизни:' + str(live), 1, (255, 255, 252))
        if live == 0:
            window.blit(lost2, (200, 200))
            finish = True
        collides1 = sprite.spritecollide(playe1, monsters, True)
        if collides1:
            live -= 1
            lives = font5.render('Жизни:' + str(live), 1, (255, 255, 252))
        for ofar in collides:
            win += 1
            enem1 = Enemy('ufo.png', random.randint(100, 350), random.randint(-5, 0), random.randint(1, 3))
            monsters.add(enem1)
        text_win = font1.render('Счёт:' + str(win), 1, (255, 255, 252))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 252))
        if win >= 10:
            font3 = font.SysFont('Arial', 36)
            win2 = font3.render('YOU WIN!', True, (250, 150, 50))
            window.blit(win2, (200, 200))
            finish = True
        if lost >= 3:
            window.blit(lost2, (200, 200))
            finish = True
        window.blit(text_lose, (0, 0))
        window.blit(text_win, (0, 30))
        window.blit(lives, (500, 0))
        if rel_time:
            now_time = timer()
            if now_time - lost_time < 3:
                font6 = font.SysFont('Arial', 36)
                reload_time = font6.render('Wait, reload...', True, (250, 255, 255))
                window.blit(reload_time, (200, 350))
            else:
                num_fire = 0
                rel_time = False        
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    playe1.fire()
                    shoot.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    lost_time = timer()
                

                    

    clock.tick(FPS)
    display.update()

