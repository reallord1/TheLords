###Hide and Seek### by Jil und Jimmy
import pygame as py
import random
 

py.init()                                      # Pygames initialisieren
win_size = (800,800)                           # Fenstergrösse
screen = py.display.set_mode(win_size)         # Fenstergrösse setzen
py.display.set_caption("01 Pygames")           # Titel des Fensters
clock = py.time.Clock()						   # Eine Pygame-Uhr um die Framerate zu kontrollieren


##


background = py.image.load("Hintergrund.png").convert()
background = py.transform.scale(background, (800, 800))


# Die Klasse des Spielers
class Player():                                          # Wie sieht der Player aus?
    #######################################
    # Bauplan des Spielers
    #######################################
    def __init__(self):
        self.breite = 100
        self.höhe = 100
        self.x = random.randint(0,700)
        self.y = random.randint(0,700)
            
    def move(self):
        key = py.key.get_pressed()                                     # Alle gedrückten Tasten abrufen
        if key[py.K_LEFT] == True:                                     
            self.x = self.x - 3
        if key[py.K_RIGHT] == True:
            self.x = self.x + 3
        if key [py.K_DOWN] == True:
            self.y = self.y + 3
        if key [py.K_UP] == True:
            self.y = self.y - 3
            
    def draw(self):
        #py.draw.rect(screen,[100,100,100],(self.x,self.y,self.breite,self.höhe),0)
        player = py.image.load("Hintergrund.png").convert()
        player = py.transform.scale(background, (self.breite, self.höhe))
        screen.blit(player,(self.x,self.y))
            
                
player = Player()

while True:
    
    screen.blit(background, (0, 0))
    
    
    player.move()
    player.draw()
    
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            py.quit()
    
    py.display.update()
    clock.tick(32)
            
            
                
  




    
