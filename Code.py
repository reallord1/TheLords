###Hide and Seek###
import pygame as py
import random
 

py.init()                                      # Pygames initialisieren
win_size = (800,800)                           # Fenstergrösse
screen = py.display.set_mode(win_size)         # Fenstergrösse setzen
py.display.set_caption("01 Pygames")           # Titel des Fensters
clock = py.time.Clock()						   # Eine Pygame-Uhr um die Framerate zu kontrollieren

 
 
# Die Klasse des Spielers
class Player(py.sprite.Sprite):                                          # Wie sieht der Player aus?
    #######################################
    # Bauplan des Spielers
    #######################################
    def __init__(self):                                            # Hier ist der Bauplan des Players
        super().__init__()                                               # Musst du nicht verstehen
        self.image = py.image.load("res/images/santa/santa0.gif").convert()    # Bild laden
        self.image  = py.transform.scale(self.image, (100, 100))         # Bild skalieren
        self.images = load_images("res/images/santa/","santa",".gif",40,100,100)
        self.rect   = self.image.get_rect()                              # Umrechteck bestimmen
        self.rect.x = random.randint(100,700)                            # zufälliger x-Startpunkt
        self.rect.y = 300
        
    def move(self):
        key = py.key.get_pressed()                                     # Alle gedrückten Tasten abrufen
        if key[py.K_LEFT] == True:                                     
            self.rect.x = self.rect.x - 3
        if key[py.K_RIGHT] == True:
            self.rect.x = self.rect.x + 3
        if key [py.K_DOWN] == True:
            self.image =
            
            
            
    def load_images(path,names,ending,number,xpix,ypix):
        file_names = []
        for i in range(number):
            file_names.append(path+names+str(i)+ending)
            animation = []
        for i in range(number):
            img = py.image.load(file_names[i]).convert()
            animation.append(py.transform.scale(img, (xpix, ypix)))
            aufnehmen
        return animation