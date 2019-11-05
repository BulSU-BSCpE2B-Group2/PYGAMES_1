import pygame

# initialize the game engine
pygame.init()

#set window size
screenWidth = 1259
screenHeight = 651

# window size
win = pygame.display.set_mode((screenWidth, screenHeight))
# window title / caption
pygame.display.set_caption("First Game Test")

walkRight = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'),
             pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'),
             pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'),
            pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'),
            pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')

clock = pygame.time.Clock()


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
        self.right = False
        self.walkCount = 0
        self.standing = True

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


class Projectile(object):
    def __init__(self, x, y, color, facing):
        self.x = x
        self.y = y
        'self.radius = radius'
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# Refreshing the window every clock.tick
def redrawgamewindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    pygame.display.update()


# create an instance of man
man = Player(250, 569, 64, 64)

# mainLoop that runs as long as program is running
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

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
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
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

    redrawgamewindow()

pygame.quit()
