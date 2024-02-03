import pygame
import random
import os
import math

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Simple Game")

# Constants
window_width = 540
window_height = 960
clock = pygame.time.Clock()
speed1 = 0
speed2 = 0
speed3 = 0
hits = 0
font = pygame.font.Font(None, 24)
path = os.path.dirname(__file__) + "\\" 
bg_image = pygame.image.load(path+'background.png')
bg_image = pygame.transform.scale(bg_image, (window_width, window_height))
nebula1_img = pygame.image.load(path+'nebula_1.png')
#nebula1_img = pygame.transform.grayscale(nebula1_img)
nebula1_img = pygame.transform.scale(nebula1_img, (440, 360))
nebula2_img = pygame.image.load(path+'nebula_2.png')
nebula2_img = pygame.transform.scale(nebula2_img, (716, 388))
stars1_img = pygame.image.load(path+'stars_1.png')
stars1_img = pygame.transform.scale(stars1_img, (window_width, window_height))
# stars1_img = pygame.transform.grayscale(stars1_img)
stars2_img = pygame.image.load(path+'stars_2.png')
stars2_img = pygame.transform.scale(stars2_img, (window_width, window_height))
stars2_img = pygame.transform.grayscale(stars2_img)
eximage = pygame.image.load(path+'explosion.png')

BG_COLOR = (246, 246, 235)
RED = (201, 49, 39)
GREEN = (121, 222, 121)
BLUE = (0, 167, 250)
PINK = (255, 194, 209)
BLACK = (66, 66, 66)

# Window Screen
surface = pygame.display.set_mode([window_width, window_height])

# Player properties
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 48
        self.height = 58
        self.image = pygame.image.load(path+'player_1.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = window_width / 2
        self.rect.centery = window_height - self.height
    def update(self, new_x=0,new_y=0, img='center'):
        self.imgx = img
        if self.imgx == 'center':
            self.image = pygame.image.load(path+'player_1.png')
        elif self.imgx == 'left':
            self.image = pygame.image.load(path+'player_left-1.png')
        elif self.imgx == 'right':
            self.image = pygame.image.load(path+'player_right-1.png')
        self.rect.centerx += new_x
        self.rect.centery += new_y
        if self.rect.centerx <= self.width/2:
            self.rect.centerx = self.width/2
        if window_width - self.rect.centerx <= self.width/2:
            self.rect.centerx = window_width - self.width/2
        if self.rect.centery <= self.height/2:
            self.rect.centery = self.height/2
        if window_height - self.rect.centery <= self.height/2:
            self.rect.centery = window_height - self.height/2

# object group
player = Player()
players = pygame.sprite.Group()
players.add(player)
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()

# Bullet properties
class Bullet(pygame.sprite.Sprite):
    def __init__(self, new_x, new_y):
        super().__init__()
        self.width = 5
        self.height = 10
        self.image = pygame.image.load(path+'bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = new_x
        self.rect.y = new_y

# Target properties
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 40
        self.image = pygame.image.load(path+'Meteo.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, window_width-20)
        self.rect.y = random.randint(-960, -40)

# image background and parallel
def showStar1(speed):
    surface.blit(stars1_img, (0, speed))
    surface.blit(stars1_img, (0, speed - window_height))
    surface.blit(stars1_img, (0, speed - (window_height * 2)))
    surface.blit(stars1_img, (0, speed - (window_height * 3)))
    surface.blit(stars1_img, (window_width/2, speed))
    surface.blit(stars1_img, (window_width/2, speed - window_height))
    surface.blit(stars1_img, (window_width/2, speed - (window_height * 2)))
    surface.blit(stars1_img, (window_width/2, speed - (window_height * 3)))
    surface.blit(stars1_img, (window_width / 3, speed))
    surface.blit(stars1_img, (window_width / 3, speed - window_height))
    surface.blit(stars1_img, (window_width / 3, speed - (window_height * 2)))
    surface.blit(stars1_img, (window_width / 3, speed - (window_height * 3)))

def showStar2(speed):
    surface.blit(stars2_img, (0, speed))
    surface.blit(stars2_img, (0, speed - window_height))
    surface.blit(stars2_img, (0, speed - (window_height * 2)))
    surface.blit(stars2_img, (window_width / 2, speed))
    surface.blit(stars2_img, (window_width / 2, speed - window_height))
    surface.blit(stars2_img, (window_width / 2, speed - (window_height * 2)))
    surface.blit(stars2_img, (window_width / 3, speed))
    surface.blit(stars2_img, (window_width / 3, speed - window_height))
    surface.blit(stars2_img, (window_width / 3, speed - (window_height * 2)))

def createExplosion(xx, yy):
    explosion = {'rectx': xx,'recty': yy,'life': 12}
    return explosion

# image nebular
nebulars = []

def createNeb1(ydiff):
    neb = {'x': random.randint(-330, window_width - 110)
           , 'y': random.randint(-2048, 900)}
    neb['y'] = neb['y'] - ydiff
    return neb

for _ in range(5):
    nebulars.append(createNeb1(0))

def showNebula1(speed):
    for n in nebulars:
        surface.blit(nebula1_img, (n['x'], speed + n['y']))

explosions = []

#add target
for _ in range(16):
    target = Target()
    targets.add(target)

while True:

    # Score properties
    score_text = font.render(f'Score: {hits}', True, (246, 246, 235))

    # Key Settings
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bullet = Bullet(players.sprites()[0].rect.centerx, players.sprites()[0].rect.centery - 27)
        bullets.add(bullet)
    if keys[pygame.K_UP]:
        players.update(0, -10)
    if keys[pygame.K_DOWN]:
        players.update(0, 10)
    if keys[pygame.K_RIGHT]:
        players.update(10, 0, 'right')
    if keys[pygame.K_LEFT]:
        players.update(-10, 0, 'left')

    # Key action
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.quit()
                exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # show bg
    surface.blit(bg_image, (0, 0))
    surface.blit(nebula2_img, (0, speed2 - window_height))

    # remove bullets when out of screen
    for bullet in bullets:
        if bullet.rect.y <= 0:
            bullet.kill()
        else:
            bullet.rect.y -= 10

    # remove nebular image when out of screen
    for neb in nebulars:
        if neb['y'] >= 960:
            nebulars.remove(neb)
            nebulars.append(createNeb1(960))

    # show star image
    showStar1(speed2)
    showStar2(speed1)
    showNebula1(speed3)

    # show objects
    players.draw(surface)
    bullets.draw(surface)
    targets.draw(surface)
    players.update(img = 'center')

    # Objects Speed Settings
    if speed1 >= window_height*2:
        speed1 = 0
    else:
        speed1 += 5
    if speed2 >= window_height*3:
        speed2 = 0
    else:
        speed2 += 1

    if speed3 >= window_height*3:
        speed3 = 0
    else:
        speed3 += 2

    # check collided
    collided_targ = pygame.sprite.groupcollide(targets, bullets, True, True)
    for targ in collided_targ:
        new_x = targ.rect.x
        new_y = targ.rect.y
        explosions.append(createExplosion(new_x, new_y))
        hits += 10
        target = Target()
        targets.add(target)

    # Draw explosion
    for exp in explosions:
        if exp['life'] <= 0:
            explosions.pop(explosions.index(exp))
        else:
            exp['life'] -= 1
            exp['recty'] += 5
        surface.blit(eximage, (exp['rectx'], exp['recty']))

    # Add/Remove target
    for target in targets:
        if target.rect.y > window_height + 100:
            target.kill()
            target = Target()
            targets.add(target)
        else:
            target.rect.y += 5

    # hits = pygame.sprite.groupcollide(rocket, target, False, True)
    surface.blit(score_text, (5, 5))
    pygame.display.update()
    clock.tick(60)
