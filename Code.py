### Hide and Seek ### Gil, Gimmy und Finnosaurus
import pygame as py
import random

py.init()

# Grund Ding
win_size = (800, 800)
screen = py.display.set_mode(win_size)
py.display.set_caption("Hide and Seek")
clock = py.time.Clock()
FPS = 60

# "safe image loader" -> weil wir grosse schwierigkeiten mit unseren Bilddateien hatten --> "CORRUPTED Files" in der Kommandozeile abgegeben und wir hatten nur einen schwarzen Hintergrund
# https://www.pygame.org/docs/ref/image.html?highlight=image#module-pygame.image --> 
def safe_load(path, size=None):
    try:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError

        img = py.image.load(str(p)).convert_alpha()

        if size:
            img = py.transform.scale(img, size)

        return img
    except:
        # If image fails, return a visible fallback surface
        surf = py.Surface(size if size else (100, 100))
        surf.fill((255, 0, 255))  # bright purple = broken image
        print(f"[WARNING] Failed loading: {path}")
        return surf
    
background = safe_load("Hintergrund.png", (800, 800)) # neu mit safe load :) --> keine corrupted files yuhu


# Spieler grösse
spieler_breite = 90
spieler_hoehe = 130

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

# Sprungbilder
JumpRight = [
    py.image.load("pictures/johannes/Jump.r.1.png"),
    py.image.load("pictures/johannes/Jump.r.2.png"),
    py.image.load("pictures/johannes/Jump.r.3.png"),
    py.image.load("pictures/johannes/Jump.r.4.png")
]

JumpLeft = [
    py.image.load("pictures/johannes/Jump.l.1.png"),
    py.image.load("pictures/johannes/Jump.l.2.png"),
    py.image.load("pictures/johannes/Jump.l.3.png"),
    py.image.load("pictures/johannes/Jump.l.4.png")
]

stand_left = py.image.load("pictures/johannes/stand.l.png")
stand_right = py.image.load("pictures/johannes/stand.r.png")

stand_left  = py.transform.scale(stand_left, (spieler_breite, spieler_hoehe))
stand_right = py.transform.scale(stand_right, (spieler_breite, spieler_hoehe))

sit_right = py.image.load("pictures/johannes/sit.r.png")
sit_left  = py.image.load("pictures/johannes/sit.l.png")

# Duck-Bilder kleiner
duck_hoehe = 100

sit_right = py.transform.scale(sit_right, (spieler_breite, duck_hoehe))
sit_left  = py.transform.scale(sit_left,  (spieler_breite, duck_hoehe))

for i in range(len(WalkRight)):
    WalkRight[i] = py.transform.scale(WalkRight[i], (spieler_breite, spieler_hoehe))
    WalkLeft[i] = py.transform.scale(WalkLeft[i], (spieler_breite, spieler_hoehe))

for i in range(len(JumpRight)):
    JumpRight[i] = py.transform.scale(JumpRight[i], (spieler_breite, spieler_hoehe))
    JumpLeft[i]  = py.transform.scale(JumpLeft[i], (spieler_breite, spieler_hoehe))

# Spieler
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

        self.ducken = False
        self.last_direction = "right"

        self.jump = False
        self.jumpCount = 0
        self.start_y = self.y

    def move(self):
        keys = py.key.get_pressed()
        moving_left  = keys[py.K_LEFT]
        moving_right = keys[py.K_RIGHT]

        if keys[py.K_UP] and not self.jump:
            self.jump = True
            self.jumpCount = 0

        self.ducken = keys[py.K_DOWN] and not (moving_left or moving_right)

        if moving_left:
            self.x -= self.velocity
            self.left = True
            self.right = False
            self.last_direction = "left"

        elif moving_right:
            self.x += self.velocity
            self.right = True
            self.left = False
            self.last_direction = "right"

        else:
            self.left = False
            self.right = False
            self.walkCount = 0

        if self.jump:
            if self.jumpCount < 28:
                self.y = self.start_y - (28 - self.jumpCount) * 2.4
            else:
                self.y = self.start_y
                self.jump = False
            self.jumpCount += 1

    def draw(self):
        if self.jump:
            frame = min(self.jumpCount // 6, 3)
            if self.last_direction == "right":
                screen.blit(JumpRight[frame], (self.x, self.y))
            else:
                screen.blit(JumpLeft[frame], (self.x, self.y))
            return

        if self.ducken:
            if self.last_direction == "right":
                screen.blit(sit_right, (self.x, self.y + spieler_hoehe - duck_hoehe))
            else:
                screen.blit(sit_left, (self.x, self.y + spieler_hoehe - duck_hoehe))
            return

        if self.walkCount + 1 >= 24:
            self.walkCount = 0

        if self.left:
            screen.blit(WalkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        elif self.right:
            screen.blit(WalkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        else:
            if self.last_direction == "right":
                screen.blit(stand_right, (self.x, self.y))
            else:
                screen.blit(stand_left, (self.x, self.y))

breite = 150
hoehe = 150

# Hindernisse
class Hindernis:

    def __init__(self, bild_pfad, breite, hoehe):


        self.breite = breite
        self.höhe = hoehe
        self.x = random.randint(0, 800 - self.breite)
        self.y = 362

        self.image = py.image.load(bild_pfad).convert_alpha()
        self.image = py.transform.scale(self.image, (self.breite, self.höhe))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        

class Stoppuhr:
    def __init__(self, bild_pfad, breite, hoehe):
        self.breite = 100
        self.höhe = 100
        self.x = 800 - self.breite  
        self.y = 0
        
        self.image = py.image.load(bild_pfad).convert_alpha()
        self.image = py.transform.scale(self.image, (self.breite, self.höhe))


    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        
        
# Objekte
player = Player()


hindernisse1 = Hindernis("Klorolle.png", 120, 120)
hindernisse2 = Hindernis("ipad.png", 120, 120)
hindernisse3 = Hindernis("Test.png", 120, 120)
hindernisse4 = Hindernis("Uhr.png", 120,120)
hindernisse5 = Hindernis("Laptop.png", 120,120)


hindernisse = []
start_x = 100
abstand = 180
bilder = ["Klorolle.png", "ipad.png", "Test.png", "Uhr.png", "Laptop.png"]


breite = 150  
hoehe = 150    
y_position = 280

# quelle: https://docs.python.org/3/library/functions.html#any
gebrauchte_positionen = []

for bild in bilder: # ziel--> dass sich die Gegenstände nicht überlappern 
    while True:
        x = random.randint(0, 800 - breite)
        ueberlappen = any(abs(x - pos) < breite + 10 for pos in gebrauchte_positionen)  
        if not ueberlappen:
            gebrauchte_positionen.append(x)
            break

    hindernis = Hindernis(bild, breite, hoehe)
    hindernis.x = x
    hindernis.y = y_position
    hindernisse.append(hindernis) 
gebrauchte_positionen = []




stoppuhr = Stoppuhr("Stoppuhr.png")




print("Game Loop startet")


running = True
while running:
    clock.tick(FPS)

  
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.blit(background, (0, 0))

   
    player.move()
    player.draw()

    for hindernis in hindernisse:
        hindernis.draw()

  
    stoppuhr.draw()

    py.display.update()

py.quit()