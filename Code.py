### Hide and Seek – kombiniert ###
import pygame as py
import random

py.init()

#Grund Ding
win_size = (800, 800)
screen = py.display.set_mode(win_size)
py.display.set_caption("Hide and Seek")
clock = py.time.Clock()
FPS = 60

# Hintergrund
background = py.image.load("Hintergrund.png").convert()
background = py.transform.scale(background, (800, 800))


#Sounds prov.
#background_sound = py.mixer.Sound("Name der Musik")
#background_sound.set_volume(0.5)
#background_sound.play(-1) # -1 unendlich wiederholen

#ducken_sound = py.mixer.Sound("Name der Ducken Musik")
#ducken_sound.set_volume(0.5)

#jump_sound = py.mixer.Sound("Name der jump Musik")
#jump_sound.set_volume(0.5)


# Spieler grösse
spieler_breite = 120
spieler_hoehe = 120

# Laufbilder
WalkRight = [
    py.image.load("pictures/johannes/run.r.1.png"),
    py.image.load("pictures/johannes/run.r.2.png"),
    py.image.load("pictures/johannes/run.r.3.png"),
    py.image.load("pictures/johannes/run.r.4.png"),
    py.image.load("pictures/johannes/run.r.5.png"),
    py.image.load("pictures/johannes/run.r.6.png"),
    py.image.load("pictures/johannes/run.r.7.png"),
    py.image.load("pictures/johannes/run.r.8.png")
]

WalkLeft = [
    py.image.load("pictures/johannes/run.l.1.png"),
    py.image.load("pictures/johannes/run.l.2.png"),
    py.image.load("pictures/johannes/run.l.3.png"),
    py.image.load("pictures/johannes/run.l.4.png"),
    py.image.load("pictures/johannes/run.l.5.png"),
    py.image.load("pictures/johannes/run.l.6.png"),
    py.image.load("pictures/johannes/run.l.7.png"),
    py.image.load("pictures/johannes/run.l.8.png")
]

standing = py.image.load("pictures/johannes/stand.l.png")


standing = py.transform.scale(standing, (spieler_breite, spieler_hoehe))                   #ChatGPT -> die Figut hat sonst beim laufen immer die grösse wider auf die kleine zurükgestellt


for i in range(len(WalkRight)):
    WalkRight[i] = py.transform.scale(WalkRight[i], (spieler_breite, spieler_hoehe))
    WalkLeft[i] = py.transform.scale(WalkLeft[i], (spieler_breite, spieler_hoehe))

# Spielerklasse
class Player:
    def __init__(self):
        self.breite = spieler_breite
        self.höhe = spieler_hoehe
        self.x = random.randint(0, 700)
        self.y = 350
        self.velocity = 3

        self.left = False
        self.right = False
        self.walkCount = 0

    def move(self):
        keys = py.key.get_pressed()

        if keys[py.K_LEFT]:
            self.x -= self.velocity
            self.left = True
            self.right = False
        elif keys[py.K_RIGHT]:
            self.x += self.velocity
            self.right = True
            self.left = False
        else:
            self.left = False
            self.right = False
            self.walkCount = 0

    def draw(self):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0

        if self.left:
            screen.blit(WalkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(WalkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(standing, (self.x, self.y))

# Hindernisklasse
class Hindernis:
    def __init__(self, bild_pfad):
        self.breite = random.randint(100, 300)
        self.höhe = random.randint(100, 300)
        self.x = random.randint(0, 800 - self.breite)
        self.y = 350

        self.image = py.image.load(bild_pfad).convert_alpha()
        self.image = py.transform.scale(self.image, (self.breite, self.höhe))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Objekte
player = Player()

hindernisse1 = Hindernis("Klorolle.png")
hindernisse2 = Hindernis("Laptop.png")
hindernisse3 = Hindernis("Test.png")
hindernisse4 = Hindernis("Uhr.png")

# Game Loop
running = True
while running:
    clock.tick(FPS)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.blit(background, (0, 0))

    player.move()
    player.draw()

    hindernisse1.draw()
    hindernisse2.draw()
    hindernisse3.draw()
    hindernisse4.draw()

    py.display.update()

py.quit()
