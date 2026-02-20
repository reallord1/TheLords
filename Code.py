### Hide and Seek ### Gil, Gimmy und Finnosaurus
import pygame as py
import random
import sys
from pathlib import Path

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

# Grösse vom Spieler
spieler_breite = 90
spieler_hoehe = 130

# bewegen vom player ; https://www.geeksforgeeks.org/python/pygame-character-animation/
WalkRight = [safe_load(f"pictures/johannes/run.r.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 9)] # Liste von Bildern wird erstellt --> für jede Zahl ein bild von Johannes gegeben
WalkLeft  = [safe_load(f"pictures/johannes/run.l.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 9)]
JumpRight = [safe_load(f"pictures/johannes/Jump.r.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 5)]
JumpLeft  = [safe_load(f"pictures/johannes/Jump.l.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 5)]

stand_right = safe_load("pictures/johannes/stand.r.png", (spieler_breite, spieler_hoehe))
stand_left  = safe_load("pictures/johannes/stand.l.png", (spieler_breite, spieler_hoehe))

duck_hoehe = 100 # er wird kleiner wenn er sich duckt
sit_right = safe_load("pictures/johannes/sit.r.png", (spieler_breite, duck_hoehe))
sit_left  = safe_load("pictures/johannes/sit.l.png", (spieler_breite, duck_hoehe))


# Player
class Player:
    def __init__(self):
        self.x = 100
        self.y = 500 #höhe von player tiefer weil hintergrund neu ist
        self.velocity = 5
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
                screen.blit(sit_right, (self.x, self.y + 30))
            else:
                screen.blit(sit_left, (self.x, self.y + 30))
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


#Kopf gleiches konzet wie bei class oben player und hindernis

class Kopf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 300
        self.height = 300  #grösse vom Kopf

        # Bilder laden
        self.augen_offen = safe_load("augen_offen.png", (self.width, self.height))
        self.augen_zu    = safe_load("augen_zu.png", (self.width, self.height))

        self.zeige_offen = True  # bild am Anfang

        # blinzeln jede 4 sek -_> bilder wechseln
        # https://www.pygame.org/docs/ref/time.html#pygame.time.get_ticks
        self.last_switch = py.time.get_ticks()
        self.switch_interval = 4000  # 4 Sek

    def draw(self):
        current_time = py.time.get_ticks()
        
        # schauen ob 4sek vorbei
        if current_time - self.last_switch >= self.switch_interval:
            self.zeige_offen = not self.zeige_offen
            self.last_switch = current_time

        # Bild zeigen
        if self.zeige_offen:
            screen.blit(self.augen_offen, (self.x, self.y))
        else: 
            screen.blit(self.augen_zu, (self.x, self.y))
            
kopf = Kopf(250, 100)


# Hindernisse
class Hindernis:
    def __init__(self, bild_pfad):
        self.width = 150
        self.height = 150
        self.x = random.randint(0, 650)
        self.y = 510 # tiefe von gegenständen auch angpasst
        self.image = safe_load(bild_pfad, (self.width, self.height))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# Stoppuhr -- musste angepasst werden weil die anzahl "elemente" breite und hoehe etc nicht den anderen einheitlich oben gleich waren --> führte zu immense frustration während vier tagen um herauszufinden was falsch war
class Stoppuhr:
    def __init__(self):
        self.image = safe_load("Stoppuhr.png", (100, 100))

    def draw(self):
        screen.blit(self.image, (700, 0))


# Objekte
player = Player() # musste ich wie oben ändern --> anzahl elemente stimmten nicht überein --> Grund für Kollaps des Spieles

#Quelle von Bildern https://www.megavoxels.com/learn/how-to-make-a-pixel-art-watermelon/

bilder = ["sneaker.png", "ipad.png", "chocolate.png", "cake.png", "microwave.png"]
hindernisse = [Hindernis(bild) for bild in bilder]


stoppuhr = Stoppuhr()



#Kopfwelches einfügen werden


# game loop -
running = True
while running:
    clock.tick(FPS)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.fill((30, 30, 30))
    
    screen.blit(background, (0, 0))

    player.move()
   

    for h in hindernisse:
        h.draw()
    
    player.draw()


    kopf.draw()
    
    stoppuhr.draw()

    

    py.display.flip()

py.quit()