import pygame
import random


# initialize the game engine
pygame.init()

# set window size
screenWidth = 1259
screenHeight = 651

# window size
win = pygame.display.set_mode((screenWidth, screenHeight))
# window title / caption
pygame.display.set_caption("First Game Test")

# load the assets for the game. Excluding music.
walkRight = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'),
             pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'),
             pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'),
            pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'),
            pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')

clock = pygame.time.Clock()

score = 0

class Player(object):
    def __init__(self, x, y, width, height):
        # position of object
        self.x = x
        self.y = y
        # hitbox of object
        self.width = width
        self.height = height
        # constant velocity of object
        self.vel = 5
        # state of the object
        self.isJump = False
        self.jumpCount = 10
        # orientation of objects
        self.left = False
        self.right = True
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 18, self.y + 12, self.width - (18 * 2), self.height - (5 * 2))

    def draw(self, win):
        # since you want each image to stay for 3 frames: (3 * 9 = 27) There are 9 images.
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 18, self.y + 12, self.width - (18 * 2), self.height - (5 * 2))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), 5 )


class Enemy(object):
    walkRight = [pygame.image.load('assets/R1E.png'), pygame.image.load('assets/R2E.png'), pygame.image.load('assets/R3E.png'),
                 pygame.image.load('assets/R4E.png'), pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'),
                 pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'), pygame.image.load('assets/R9E.png'),
                 pygame.image.load('assets/R10E.png'), pygame.image.load('assets/R11E.png')]
    walkLeft = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'), pygame.image.load('assets/L3E.png'),
                pygame.image.load('assets/L4E.png'), pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'),
                pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'), pygame.image.load('assets/L9E.png'),
                pygame.image.load('assets/L10E.png'), pygame.image.load('assets/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 11, self.y, self.width - (16 * 2), self.height)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 150, 0), (self.hitbox[0], self.hitbox[1] - 20, 5 * self.health, 10))
            self.hitbox = (self.x + 11, self.y, self.width - (16 * 2), self.height)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x - self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self, points):
        if self.health > 0:
            self.health -= 1
            points += 0
            return points

        if self.health == 0:
            self.visible = False
            points += 1
            return int(points)

# This is where the display happens. Everything you put here is displayed
def redrawgamewindow(points):
    win.blit(bg, (0, 0))
    text = font.render("Score: %d" %points, 1, (255, 0, 0))
    win.blit(text, (1000, 50))
    man.draw(win)
    for i in goblin:
        i.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


font = pygame.font.SysFont('lato', 30, True)
# create an instance of man
man = Player(250, 569, 64, 64)

# create bullets
bullets = []

goblin = []

gunCooldown = 0
goblinSpawnCooldown = 0

# mainLoop that runs as long as program is running
run = True
while run:
    clock.tick(27)

    gunCooldown += 1
    goblinSpawnCooldown += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    for bullet in bullets:
        for i in goblin:
            if bullet.y - bullet.radius < i.hitbox[1] + i.hitbox[3] and bullet.y + bullet.radius > i.hitbox[1]:
                if bullet.x - bullet.radius > i.hitbox[0] and bullet.x - bullet.radius < i.hitbox[0] + i.hitbox[2]:
                    if i.visible:
                        score = i.hit(score)
                        try:
                            bullets.pop(bullets.index(bullet))
                        except ValueError:
                            print("Bullet is nullified, if enemies are in state of collision the damage becomes split "
                                  "which nullifies bullet")

        if 1256 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            try:
                bullets.pop(bullets.index(bullet))
            except ValueError:
                print("Woops. Looks like collision between the enemy, bullet and the map border has matched.")

    keys = pygame.key.get_pressed()
    if len(goblin) < 3 and goblinSpawnCooldown >= 15:
        goblin.append(Enemy(100, 569, 64, 64, 1200))
        goblinSpawnCooldown = 0

    if keys[pygame.K_SPACE] and gunCooldown >= 12:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) <= 5:
            bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 1, (255, 255, 255),
                                      facing))
        gunCooldown = 0

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (screenWidth - (man.width + man.vel)):
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    elif keys[pygame.K_ESCAPE]:
        run = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0

    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            # Quadratic equation of jumping
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawgamewindow(score)

pygame.quit()

# TODO: Solve issue regarding inability to fire if both Left and Up keys are pressed.
