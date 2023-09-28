import pygame 
import os
import random

pygame.init()

win = pygame.display.set_mode((910, 643))

pygame.display.set_caption("First Game")

walkRight = pygame.image.load(os.path.join("images", "scienziatoright64.png"))
coronaImg = pygame.image.load(os.path.join("images", "corona.png"))
walkLeft = pygame.image.load(os.path.join("images", "scienziatoleft64.png"))
bg = pygame.image.load(os.path.join("images", "ospedale.png"))
bulletSound = pygame.mixer.Sound(os.path.join("sounds", "blood.wav"))
coronaSound = pygame.mixer.Sound(os.path.join('sounds',"blood.wav"))
#coronaSound = pygame.mixer.Sound(os.path.join("sounds", "cardicoro.wav"))
music = pygame.mixer.music.load(os.path.join('music',"themesong.mp3"))
#music = pygame.mixer.music.load(os.path.join("music", "coronavirus.mp3"))
#music = pygame.mixer.music.load(os.path.join('music',"quarantena.mp3"))
fatality = pygame.mixer.Sound(os.path.join("sounds", "fatality.wav"))
splat = pygame.image.load(os.path.join("images", "splat.png"))
pygame.mixer.music.play(-1)

# caption e icon
pygame.display.set_caption("Pandemia")

virus = pygame.image.load(os.path.join("images", "virus.png"))
pygame.display.set_icon(virus)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Times", 16, True)
font2 = pygame.font.Font(os.path.join("fonts", "halo3.ttf"), 50)
font3 = pygame.font.Font(os.path.join("fonts", "halo3.ttf"), 45)
font4 = pygame.font.Font(os.path.join("fonts", "halo3.ttf"), 120)


# score
docscore = 8
corscore = 13


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 31, 64)
        self.health = 8
        self.visible = True

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft, (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight, (self.x, self.y))
                self.walkCount += 1
            elif self.up:
                win.blit(walkRight, (self.x, self.y))
                self.walkcount += 1
            elif self.down:
                win.blit(walkRight, (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                win.blit(walkRight, (self.x, self.y))
            else:
                win.blit(walkLeft, (self.x, self.y))

        pygame.draw.rect(
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 40, 10)
        )
        pygame.draw.rect(
            win,
            (0, 128, 0),
            (self.hitbox[0], self.hitbox[1] - 10, 40 - (5 * (8 - self.health)), 10),
        )
        self.hitbox = (self.x, self.y, 31, 64)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        elif self.health == 0:
            win.blit(splat, (self.x, self.y))
        else:
            self.visible = False
        print("dochit")


class enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 13
        self.visible = True

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

        if not (self.standing):
            if self.left and self.right and self.up and self.down:
                win.blit(coronaImg, (self.x, self.y))
                self.walkcount += 1
        else:
            win.blit(coronaImg, (self.x, self.y))

        pygame.draw.rect(
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 65, 13)
        )
        pygame.draw.rect(
            win,
            (0, 128, 0),
            (self.hitbox[0], self.hitbox[1] - 10, 65 - (5 * (13 - self.health)), 13),
        )
        self.hitbox = (self.x, self.y, 64, 64)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        elif self.health == 0:
            win.blit(splat, (self.x, self.y))
        else:
            self.visible = False
        print("corhit")


class Pause(object):
    def __init__(self):
        self.paused = pygame.mixer.music.get_busy()

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
        if not self.paused:
            pygame.mixer.music.pause()
        self.paused = not self.paused


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 13 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class projectile2(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 5 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render("CORONAVIRUS HEALTH: " + str(corscore), 1, (255, 255, 255))
    win.blit(text, (680, 10))
    text2 = font.render("MR.SPECIAL HEALTH: " + str(docscore), 1, (255, 255, 255))
    win.blit(text2, (25, 10))
    wintext = font2.render("MR.SPECIAL HAS WON!", 1, (255, 255, 0))
    wintext2 = font3.render("CORONAVIRUS HAS WON!", 1, (255, 255, 0))
    wintext3 = font4.render("TIE", 1, (225, 255, 0))
    if doc.health > 0:
        doc.draw(win)
    if doc.health == 0 and cor.health > 0:
        win.blit(splat, (doc.x, doc.y))
        win.blit(wintext2, (38, 321))
    if doc.health == 1:
        pygame.mixer.music.stop()
    if cor.health > 0:
        cor.draw(win)
    if cor.health == 0 and doc.health > 0:
        win.blit(splat, (cor.x, cor.y))
        win.blit(wintext, (52, 321))
    if doc.health == 0 and cor.health == 0:
        win.blit(splat, (cor.x, cor.y))
        win.blit(splat, (doc.x, doc.y))
        win.blit(wintext3, (335, 300))
    if cor.health == 0 or doc.health == 0:
        pygame.mixer.music.stop()
    else:
        ()
    for bullet in bullets:
        bullet.draw(win)
    for bullet2 in bullets2:
        bullet2.draw(win)

    pygame.display.update()





# mainloop
cor = enemy(740, 480, 64, 64)
doc = player(140, 480, 64, 64)
shoot = 0
PAUSE = Pause()
bullets = []
bullets2 = []
run = True

while run:
    clock.tick(27)

    if shoot > 0:
        shoot += 1
    if shoot > 5:
        shoot = 0

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            ()

    for bullet in bullets:
        if (
            bullet.y - bullet.radius < cor.hitbox[1] + cor.hitbox[3]
            and bullet.y + bullet.radius > cor.hitbox[1]
        ):
            if (
                bullet.x + bullet.radius > cor.hitbox[0]
                and bullet.x - bullet.radius < cor.hitbox[0] + cor.hitbox[2]
            ):
                bulletSound.play()
                cor.hit()
                if corscore > 0:
                    corscore -= 1
                else:
                    corscore = 0
                bullets.pop(bullets.index(bullet))

        if bullet.x < doc.x + 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for bullet2 in bullets2:
        if (
            bullet2.y - bullet2.radius < doc.hitbox[1] + doc.hitbox[3]
            and bullet2.y + bullet2.radius > doc.hitbox[1]
        ):
            if (
                bullet2.x + bullet2.radius > doc.hitbox[0]
                and bullet2.x - bullet2.radius < doc.hitbox[0] + doc.hitbox[2]
            ):
                coronaSound.play()
                doc.hit()
                if docscore > 0:
                    docscore -= 1
                else:
                    docscore = 0
                bullets2.pop(bullets2.index(bullet2))

        if bullet2.x < cor.x + 500 and bullet2.x > cor.x - 500:
            bullet2.x += bullet2.vel
        else:
            bullets2.pop(bullets2.index(bullet2))

    if keys[pygame.K_SPACE]:
        if doc.health != 0 and cor.health != 0:
            if doc.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) < 1:
                bullets.append(
                    projectile(
                        round(doc.x + doc.width // 2),
                        round(doc.y + doc.height // 2),
                        6,
                        (255, 0, 0),
                        facing,
                    )
                )
            else:
                ()
        else:
            facing = 0
            bullets.append(projectile(1000, 1000, 3, (0, 255, 0), facing))

    if keys[pygame.K_RIGHTBRACKET] and shoot == 0: 
        if doc.health != 0 and cor.health != 0:
            facing = 1
            if len(bullets2) < 5:
                bullets2.append(
                    projectile2(
                        round(cor.x + cor.width // 2),
                        round(cor.y + cor.height // 2),
                        3,
                        (0, 255, 0),
                        facing,
                    )
                )
                shoot = 1
        else:
            facing = 0
            bullets2.append(projectile2(1000, 1000, 3, (0, 255, 0), facing))

    if keys[pygame.K_LEFTBRACKET] and shoot == 0:
        if doc.health != 0 and cor.health != 0:
            facing = -1
            if len(bullets2) < 5:
                bullets2.append(
                    projectile2(
                        round(cor.x + cor.width // 2),
                        round(cor.y + cor.height // 2),
                        3,
                        (0, 255, 0),
                        facing,
                    )
                )
                shoot = 1
        else:
            facing = 0
            bullets2.append(projectile2(1000, 1000, 3, (0, 255, 0), facing))

    if keys[pygame.K_LSHIFT]:
        doc.vel = 8
    else:
        doc.vel = 5

    if keys[pygame.K_m]:
        PAUSE.toggle()
    else:
        ()

    if keys[pygame.K_n]:
        coronaSound.stop()
        bulletSound.stop()
    else:
        ()

    # Onkey per l'enemy
    if doc.health != 0 and cor.health != 0:
        if keys[pygame.K_LEFT] and cor.x > cor.vel:
            cor.x -= cor.vel
            cor.left == True
            cor.right == False
            cor.standing == False
        elif keys[pygame.K_RIGHT] and cor.x < 1000 - cor.width - cor.vel:
            cor.x += cor.vel
            cor.right == True
            cor.left == False
            cor.standing == False
        elif keys[pygame.K_UP] and cor.y > cor.vel:
            cor.y -= cor.vel
            cor.up == True
        elif keys[pygame.K_DOWN] and cor.y < 643 - cor.height - cor.vel:
            cor.y += cor.vel
            cor.down == True
        else:
            cor.standing == True
            cor.walkCount == 0
    else:
        ()

    # Onkey per il player
    if doc.health != 0 and cor.health != 0:
        if keys[pygame.K_a] and doc.x > doc.vel:
            doc.x -= doc.vel
            doc.left = True
            doc.right = False
            doc.standing = False
        elif keys[pygame.K_d] and doc.x < 920 - doc.width - doc.vel:
            doc.x += doc.vel
            doc.right = True
            doc.left = False
            doc.standing = False
        elif keys[pygame.K_w] and doc.y > doc.vel:
            doc.y -= doc.vel
            doc.up == True
        elif keys[pygame.K_s] and doc.y < 643 - doc.height - doc.vel:
            doc.y += doc.vel
            doc.down == True
        else:
            doc.standing = True
            doc.walkCount = 0
    else:
        ()

    redrawGameWindow()


pygame.quit()
