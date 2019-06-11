import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('image/R1.png'), pygame.image.load('image/R2.png'), pygame.image.load('image/R3.png'), pygame.image.load('image/R4.png'), pygame.image.load('image/R5.png'), pygame.image.load('image/R6.png'), pygame.image.load('image/R7.png'), pygame.image.load('image/R8.png'), pygame.image.load('image/R9.png')]
# walkRight = [pygame.image.load(pygame.path.join('caminho/pasta','R1.png'))] caso a imagem se encontre em um diretório diferente
walkLeft = [pygame.image.load('image/L1.png'), pygame.image.load('image/L2.png'), pygame.image.load('image/L3.png'), pygame.image.load('image/L4.png'), pygame.image.load('image/L5.png'), pygame.image.load('image/L6.png'), pygame.image.load('image/L7.png'), pygame.image.load('image/L8.png'), pygame.image.load('image/L9.png')]
bg = pygame.image.load('image/bg.jpg')
char = pygame.image.load('image/standing.png')

#/

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height): #self: atributo da classe
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velo = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not (self.standing):
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



class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy (object):
    walkRight = [pygame.image.load('image/R1E.png'), pygame.image.load('image/R2E.png'), pygame.image.load('image/R3E.png'), pygame.image.load('image/R4E.png'), pygame.image.load('image/R5E.png'), pygame.image.load('image/R6E.png'), pygame.image.load('image/R7E.png'), pygame.image.load('image/R8E.png'), pygame.image.load('image/R9E.png'), pygame.image.load('image/R10E.png'), pygame.image.load('image/R11E.png')]
    walkLeft = [pygame.image.load('image/L1E.png'), pygame.image.load('image/L2E.png'), pygame.image.load('image/L3E.png'), pygame.image.load('image/L4E.png'), pygame.image.load('image/L5E.png'), pygame.image.load('image/L6E.png'), pygame.image.load('image/L7E.png'), pygame.image.load('image/L8E.png'), pygame.image.load('image/L9E.png'), pygame.image.load('image/L10E.png'), pygame.image.load('image/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw (self, win):
        self.move()
        if self.walkCount +1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move (self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
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




def redrawGameWindow():

    win.blit(bg, (0,0))

    krilin.draw(win)
    saibaman.draw(win)

    for kienzan in kienzans:
        kienzan.draw(win)

    pygame.display.update()



#main loop
krilin = player(300, 410, 64, 64)
kienzans = []
saibaman  = enemy(100, 410, 64,64, 450)
run = True
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for kienzan in kienzans:
        if kienzan.x < 500 and kienzan.x > 0:
            kienzan.x += kienzan.vel
        else:
            kienzans.pop(kienzans.index(kienzan))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_x]:
        if krilin.left:
            facing = -1
        else:
            facing = 1
        if len(kienzans) < 5:
            kienzans.append(projectile(round(krilin.x + krilin.width //2), round(krilin.y + krilin.height //2), 6, (240,248,255), facing))

    if keys[pygame.K_LEFT] and krilin.x > krilin.velo:
        krilin.x -= krilin.velo
        krilin.left = True
        krilin.right = False
        krilin.standing = False
    elif keys[pygame.K_RIGHT] and krilin.x < 500 - krilin.width - krilin.velo:
        krilin.x += krilin.velo
        krilin.left = False
        krilin.right = True
        krilin.standing = False
    else:
        krilin.standing = True
        krilin.walkCount = 0
    if not (krilin.isJump):
        if keys[pygame.K_z]:
            krilin.isJump = True
            krilin.right = False
            krilin.left = False
            krilin.walkCount = 0
    else:
        if krilin.jumpCount >= -10:
            neg = 1
            if krilin.jumpCount < 0:
                neg = -1
            krilin.y -= (krilin.jumpCount ** 2) * 0.5 * neg
            krilin.jumpCount -= 1
        else:
            krilin.isJump = False
            krilin.jumpCount = 10

    redrawGameWindow()

pygame.quit()