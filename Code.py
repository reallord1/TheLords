### Hide and Seek ### Gil, Gimmy und Finnosaurus
import pygame as py # abkürzung von pygame --> übersichtlicher und schneller bei code
import random # damit wir die random funktion benutzen können


py.init() # damit wir sounds, grafiken etc benutzen können


# Hintergrundmusik -> Sound laden -> am beispiel von Ihnen weiterentwickelt
py.mixer.music.load("game_music.wav")
py.mixer.music.set_volume(0.5)
py.mixer.music.play(-1)  # -1 = Endlosschleife

star_sound = py.mixer.Sound("star_sound.wav")
star_sound.set_volume(0.9)

game_over_sound = py.mixer.Sound("game_over_sound.wav")
game_over_sound.set_volume(0.8) #gut hörbar

win_sound = py.mixer.Sound("win_sound.wav")
win_sound.set_volume(0.9) #noch besser höhrbar wie game_over, da wichtiger

jump_sound = py.mixer.Sound("jump_sound.wav")
jump_sound.set_volume(0.6)

duck_sound = py.mixer.Sound("ducken_sound.wav")
duck_sound.set_volume(0.6)

background_paused = False


# Grund Ding
win_size = (800, 800) # definiert grösse vom Bildschirm
screen = py.display.set_mode(win_size)
clock = py.time.Clock() # iniziisert das Zeit feature --> alles im FPS wiederholt sich immer jede minute
FPS = 60

# Chatgpt gefragt wie man den code übersichtlicher machen kann und hat load_img funktion vorgeschlagen
# https://github.com/search?q=pygame.image.load+language%3APython&type=Code&l=Python ; https://github.com/search?q=pygame.Surface.convert_alpha+language%3APython&type=Code&l=Python

def load_img(path, size=None): # Bild Laden (damit die codes kompakter schreiben kann) 
    img = py.image.load(path).convert_alpha() # convert alpha damit der transparente Teil vom Bild nicht schwarz wird --> vorheriges Problem
    if size is not None:
        img = py.transform.scale(img, size)
    return img
    
background = py.transform.scale(
    py.image.load("Hintergrund.png").convert_alpha(),
    (800, 800)
)

# Grösse vom Spieler
spieler_breite = 90
spieler_hoehe = 130

# bewegen vom player ; https://www.geeksforgeeks.org/python/pygame-character-animation/ -> Dannach noch ausgeschnitten und vormatiert
WalkRight = [load_img(f"pictures/johannes/run.r.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 9)] # Liste von Bildern wird erstellt --> für jede Zahl ein bild von Johannes gegeben
WalkLeft  = [load_img(f"pictures/johannes/run.l.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 9)]
JumpRight = [load_img(f"pictures/johannes/Jump.r.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 5)]
JumpLeft  = [load_img(f"pictures/johannes/Jump.l.{i}.png", (spieler_breite, spieler_hoehe)) for i in range(1, 5)]

# stehende Bilder laden
stand_right = load_img("pictures/johannes/stand.r.png", (spieler_breite, spieler_hoehe))
stand_left  = load_img("pictures/johannes/stand.l.png", (spieler_breite, spieler_hoehe))

# sitzende Bilder Laden
duck_hoehe = 100 # er wird kleiner wenn er sich duckt
sit_right = load_img("pictures/johannes/sit.r.png", (spieler_breite, duck_hoehe)) 
sit_left  = load_img("pictures/johannes/sit.l.png", (spieler_breite, duck_hoehe))


# Player
class Player:
    def __init__(self):
        self.x = 100
        self.y = 500 # wei weit oben und links/rechts der Player ist
        self.rect = py.Rect(self.x, self.y, spieler_breite, spieler_hoehe) ##  colliderect funktioniert nur mit rect objekten ; radius definieren nur mit rectanges; https://www.geeksforgeeks.org/python/adding-collisions-using-pygame-rect-colliderect-in-pygame/?utm_source=chatgpt.com
        self.velocity = 5 # wie schnell der Player laufen kann
        self.left = False # für das richtige Bild
        self.right = False # für das richtige Bild
        self.walkCount = 0 # setzt auf erstes Bild von Player zurück wenn SPiel anfängt
        self.ducken = False # für das richtige Bild
        self.last_direction = "right" #
        self.jump = False # sehen ob Player am springen ist --> im späteren bewegungs Code wichtig
        self.jumpCount = 0 # setzt auf erstes Bild von Player wenn er springen soll zurück wenn SPiel anfängt
        self.start_y = self.y # damit wir kontrollieren wie hoch er springen kann

    def move(self):
        keys = py.key.get_pressed() # wenn diese taste gedrückt wird, bewegt er sich so...
        moving_left  = keys[py.K_LEFT]
        moving_right = keys[py.K_RIGHT]

        if keys[py.K_UP] and not self.jump:
            self.jump = True
            self.jumpCount = 0 # setzt auf erstes Bild von Player wenn er springen soll zurück wenn SPiel anfängt
            jump_sound.play() # Sound spielen 
            
            
        if keys[py.K_DOWN] and not self.ducken and not (moving_left or moving_right):
            self.ducken = True
            duck_sound.play() # Sound spielen
        elif not keys[py.K_DOWN]:
            self.ducken = False

        if moving_left and self.x > -45: # self.x > -45 damit er nicht aus dem Bild geht nur halbt drausen maximal
            self.x -= self.velocity # wie schnell er laufen  kann
            self.left = True # Bilder
            self.right = False # Bilder
            self.last_direction = "left" # für das richtige Bild
        elif moving_right and self.x < 800 -45: # self.x < 800 -45 damit er nicht aus dem Bild geht nur halbt drausen maximal
            self.x += self.velocity
            self.right = True # Bilder
            self.left = False # Bilder
            self.last_direction = "right" # für das richtige Bild
        else:
            self.left = False
            self.right = False
            self.walkCount = 0 # Bild wieder auf erste wenn Player einfach steht

        if self.jump:
            if self.jumpCount < 28: # frames: solange jumpCount weniger als 28 ist, geht der player nach oben
                self.y = self.start_y - (28 - self.jumpCount) * 2.4 # berechnet wie hoch der player springt und macht dass er dann wieder zurück auf den Boden fällt
            else:
                self.y = self.start_y
                self.jump = False # zeigt das Sprung vorbei ist
            self.jumpCount += 1

    def draw(self):
        if self.jump: # alles hier passiert nur wenn der Player gerade am Springen ist
            frame = min(self.jumpCount // 6, 3) # zeigt welche Bilder animation von ihm angezeigt werden
            if self.last_direction == "right":
                screen.blit(JumpRight[frame], (self.x, self.y))
            else:
                screen.blit(JumpLeft[frame], (self.x, self.y))
            return

        if self.ducken:
            if self.last_direction == "right": # das richtige sprungbild wird ausgewählt abhängig davon zu welcher Seite der Player läuft
                screen.blit(sit_right, (self.x, self.y + 30))
            else:
                screen.blit(sit_left, (self.x, self.y + 30))
            return

        if self.walkCount + 1 >= 24: # nachdem alle Frames durchgegangen sind fängt es wieder von vorne an: erstes Bild wird wieder gezeigt
            self.walkCount = 0

        if self.left:
            screen.blit(WalkLeft[self.walkCount // 3], (self.x, self.y)) # jedes Bild wird ein Frame(Einzelnes Bild im Python STyle) angezeigt --> insgesamt 8 Bilder also / 8 Bilder mal 3 Frames = 24 
            self.walkCount += 1
        elif self.right:
            screen.blit(WalkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            if self.last_direction == "right": # spieler schaut in die direktion in der er zuletzt gelaufen ist 
                screen.blit(stand_right, (self.x, self.y)) # blit zeigt bild auf Bildschirm an
            else:
                screen.blit(stand_left, (self.x, self.y))
        
        self.rect.topleft = (self.x, self.y) # colliderect funktioniert nur mit rect objekten


#Kopf gleiches konzet wie bei class oben player und hindernis
class Kopf:
    def __init__(self, x, y):
        self.x = x # wo ist der Kopf... (unten genaue koordinaten geschrieben)
        self.y = y
       
        self.augen_offen = load_img("augen_offen.png") # definiert
        self.augen_offen = py.transform.scale(self.augen_offen, (300, 500)) # grösse angepasst/definiert

        self.augen_zu = load_img("augen_zu.png")
        self.augen_zu = py.transform.scale(self.augen_zu, (300, 500))

        self.zeige_offen = True  #  dieses Bild wird am Anfang gezeigt

        # blinzeln jede 4 sek --> bilder (aufen offen & zu)  wechseln
        # https://www.pygame.org/docs/ref/time.html#pygame.time.get_ticks
        self.last_switch = py.time.get_ticks()
        self.switch_interval = 2000 # 2 Sek

    def draw(self):
        current_time = py.time.get_ticks() # Zeiteinheit in milisekunden
        
        # schauen ob 4sek vorbei
        if current_time - self.last_switch >= self.switch_interval: # schauen ob genug Zeit vergangen ist : Die Zeit die bis jetzt vergangen minus zeit wenn Bild zuletzt gewechelt wurde und grösser als zwei sekunden ist, wird das Bild gewechselt
            self.zeige_offen = not self.zeige_offen
            self.last_switch = current_time # speichert neue Zeit wenn Bild von Augen offen zuletzt dort war

        # Bilder von augen offen und augen zu werden überhaupt gezeigt
        if self.zeige_offen:
            screen.blit(self.augen_offen, (self.x, self.y))
        else: 
            screen.blit(self.augen_zu, (self.x, self.y))
            
kopf = Kopf(250, 25) # Wo der Kopf genau liegt


# Hindernisse
class Hindernis:
    def __init__(self, bild_pfad, breite, hoehe, x_position, y_position): # beschreibungen von den versch Hindernissen
    
        self.x = x_position # ich kann wie weit rechts oder links die Gegenstände sind selber entscheiden
        self.y = y_position  # ich kann höhe von gegenständern manuel selber entscheiden              
        self.image = load_img(bild_pfad) #Bilder von Hindernissen können nun gezeigt werden . mit load_img kompakter
        
        self.image = py.transform.scale(self.image, (breite, hoehe)) # anpassung von grösse von Hindernissen

    def draw(self):
        screen.blit(self.image, (self.x, self.y)) # Bilder von Hindernissen werden angezeigt

# Stoppuhr -- musste angepasst werden weil die anzahl "elemente" breite und hoehe etc nicht den anderen einheitlich oben gleich waren --> führte zu immenser Frustration während vier tagen um herauszufinden was falsch war
class Stoppuhr:
    def __init__(self):
        self.image1 = load_img("Stoppuhr_1.png", (120, 120)) #"Stoppuhr_1.png" & "Stoppuhr_alarm.png" Bild von Chatgpt generieren lassen
        self.image2 = load_img("Stoppuhr_alarm.png", (120, 120))

    def draw(self):
        time = py.time.get_ticks()
       
        if (time // 400) % 2 == 0: # jede 400 ms werden die Bilder gewechselt # Die zeit dividuert durch 400ms und gerundet --> wenn gerade  Zahl dann image 1 gezeigt sonst image 2
            screen.blit(self.image1, (670, 10)) # wo die Bilder auftauchen
        else:
            screen.blit(self.image2, (670, 10))
            
        


# Stern
class Stern:
    def __init__(self):
        self.image = load_img("star.png", (60, 60)) # "Stern.png" Bild von Chatgpt generieren lassen
        self.x = random.randint(0, 740) # mit random funktion : auf welcher breite der Stern random auftauchen kann
        self.y = random.randint(480, 580) # auf welcher höhe der Stern random auftauchen kann
        self.rect = py.Rect(self.x, self.y, 60, 60) #rect wichtig für colliderate Feature, denn colliderate hat nur mit rechteckigen Bildern funktioniert...

    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # wird auf Bildschirm angezeigt
        self.rect.topleft = (self.x, self.y)

    # sodass die sterne nach Berührung von player respawnen
    # https://github.com/search?q=pygame.Rect.collidelist+language%3APython&type=Code&l=Python
    # untertützung von chatgpt: hatte schwierigkeiten herauszufinden wo denn genau colliderect im code reinsoll --> gameloop oder oben...
    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect): # wenn Player stern berührt....
          
            self.x = random.randint(0, 740) # auf welcher breite der Stern spawnen kann
            self.y = random.randint(450, 580) # auf welche der höhe der stern spawnen kann
            
            self.rect.topleft = (self.x, self.y)# rect damit colliderate funktioniert

# Objekte
player = Player() # mussten wir wie oben ändern --> anzahl elemente stimmten nicht überein --> Grund für vorherigen Kollaps des Spieles

#Quelle von Hindernissen https://www.megavoxels.com/learn/how-to-make-a-pixel-art-watermelon/

# musste mehrmals angepasst werden, weil wir sonst nicht die grössse von jedem Hinderniss seperat ändern können
hindernisse = [
    Hindernis("chocolate.png", 200, 200, 350, 457),
    Hindernis("cake.png", 170, 170, 640, 480),
    Hindernis("microwave.png", 200, 200, 10, 465),
]


stoppuhr = Stoppuhr() # damit man die SToppuhr aufrufen und schlussendlich sehen kann , gleiches gilt für stern = Stern() etc..

stern = Stern() 


# score machen
# https://www.makeuseof.com/pygame-game-scores-displaying-updating/
score = 0 # am Anfang des Spieles immer auf 0 gestellt
font = py.font.SysFont(None, 40) # None: standart systemschriftart und 40 ist Buchstabengrösse-> Man sieht den score nicht auf jedem Laptop, ich sehe ihn nicht, die anderen schon


# für Hintergrund
# https://github.com/search?q=pygame.key.get_pressed+language%3APython&type=Code&l=Python


# alles immer auf 800*800 grösse 
startbild = load_img("Start_Bildschirm.png", (800, 800)) #starthintergrund
game_started = False # wenn spiel noch nicht angefangen hat wird Startbild gezeigt

# für endbildschirm
endbild = load_img("End_Bildschirm.png", (800, 800)) # Während dem Spiel Hintergrund 
game_over = False

wonbild = load_img("Won_Bildschirm.png", (800, 800)) # gewinnerhintergrund



def reset_game():
    global player, stern, score, game_over, game_started # global, da die Variabeln ausserhalb dieser Funktion deffiniert sind -> ChatGPT Idee gebracht, da es nicht funktioniert hat
    
    player = Player()   # neuer Spieler
    stern = Stern()     # neuer Stern
    score = 0           # Score zurücksetzen
    game_over = False # damit Game nicht fertig ist
    game_started = True # damit Game wieder läuft
    
    kopf.zeige_offen = True # damit man nciht direkt wider stirbt
    kopf.last_switch = py.time.get_ticks()  # Reset der Blinzel-Timer -> Jil hat es oben verwendet desshalb auf diese Idee gekommen
    
    py.mixer.music.stop() # damit sicher nicht zwei übereinander sind 
    py.mixer.music.play(-1)   # Musik wieder starten wen Speil wieder started



running = True
while running: # solange running Variable wahr ist...
    clock.tick(FPS) # Zeit --> sekunden definiert

    for event in py.event.get(): # wenn irgendwas passiert wie fenster schliessen, dann ist running= false und das spiel stoppt
        if event.type == py.QUIT:
            running = False

#Hintergrundmusik ein/aus
        if event.type == py.KEYDOWN:
            if event.key == py.K_m:  # Taste M für Musik ein aus
                if background_paused:
                    py.mixer.music.unpause()
                else:
                    py.mixer.music.pause()
                background_paused = not background_paused

            
            
    # https://github.com/search?q=pygame.key.get_pressed+language%3APython&type=Code&l=Python 
    keys = py.key.get_pressed() # wenn die leertaste gedrückt wird is game started true --> normaler hintergrung initiiert --> mit boolean erzeugt
    if keys[py.K_SPACE]:
        if not game_started:
            game_started = True
        elif game_over: # damit es geht, wenn man restarted, nachdem man verloren hat
            reset_game()
            
 
    
    screen.fill((30, 30, 30))
    
    if not game_started:
        
        screen.blit(startbild, (0, 0)) # startbildschirm wird gezeigt
        
    elif game_over:
        
        screen.blit(endbild, (0, 0))# endbildschirm wird angezeigt
        
    else:
        
        screen.blit(background, (0, 0)) # normaler Hintergrund erscheint mit dem Player, Hindernissen, Kopfm Stoppuhr, Stern etc...
        
    
        
        for h in hindernisse: # Liste gamcht -- > übersichtlicher
            h.draw()
        
        kopf.draw()
        
        hinter_hindernis = True # damit die Variabel überhaupt existiert
        
        # immer wenn "augen_offen.png" dort ist und der Player nicht hinter einem Hindernis ist: "End_Bildschirm.png"
        # (hat zuerst nicht mit colliderect feature nicht funktioniert, weil es ungenau war)
        if kopf.zeige_offen: #  # schauen ob auge_offen.png an ist
            hinter_hindernis = False # neuer Boolean
            
            for h in hindernisse:
                hindernis_rect = py.Rect(h.x, h.y, h.image.get_width(), h.image.get_height()) # die höhe und breite der Hindernisse aufrufen
                 
            
                # chatgpt gefragt, was für ein feature es braucht zum zeigen das die figur im Radius ist --> contains
                # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.contains
                #https://github.com/search?q=pygame.Rect.contains+language%3APython&type=Code&l=Python
                #der Player muss im kompletten radius von sicherer Ort bzw vom sicheren rectangle rect.sein
                if hindernis_rect.contains(player.rect):
                    hinter_hindernis = True
                
                   
                    #schauen ob der Player auf ca. gleichen höhe ist wie Hindernisse : ca ist wichtig, weil wenn genau ist, code vorher nicht funktioniert hat
                    if player.rect.bottom > hindernis_rect.top: # ist untersterteil des player weiter oben als der radius des quadrates wo er sicher ist : zum sehen ob er im radius bzw sicher ist
                        hinter_hindernis = True
                        

        # wenn Player nicht hinter hindernis ist --> game over & End_Bildschirm wird aktiviert
        if not hinter_hindernis and not game_over: # and not game_over: damit er nur einmal abgespielt wird
            game_over = True
            py.mixer.music.stop() #wenn verloren keine Musik mehr
            game_over_sound.play() # game_over Sound spielen

        
        stoppuhr.draw()
        stern.draw()
        
        # https://www.geeksforgeeks.org/python/adding-collisions-using-pygame-rect-colliderect-in-pygame/?utm_source=chatgpt.com
        if stern.rect.colliderect(player.rect): # collidirect  wird aufgerufen
            score += 1 # immer wenn stern und player colliden --> score wird um einen Punkt höher
            star_sound.stop() #wenn man sehr schnell hintereinander zwei Sterne einsammelt, kann der zweite "verschluckt werdem", so nicht mehr
            star_sound.play() #stern sound
            stern.x = random.randint(0, 740) # wo sich der Stern auftauchen (random) kann
            stern.y = random.randint(460, 580)
            stern.rect.topleft = (stern.x, stern.y) # linker eckpunkt vom STern  ist definiert höhe und wie breit worden
            
        #https://www.pygame.org/docs/ref/time.html#pygame.time.wait
        if score == 15: # damit das spiel nach 20 geholten sternen passt -> 10 zu kurz -> zu 15 geändert 20 eher zu lang
            py.mixer.music.stop() # keine Musik wenn gewonnen
            win_sound.play() # win sound spielen
            screen.blit(wonbild, (0, 0)) 
            py.display.update() # updated bildschirm
            py.time.wait(5000)   # Hintergrund bleibt für nur 5 Sekunden
            running = False   # spiel stoppt
            
            
        player.move() # ruft das bewegen des SPielers auf: sonst könnte er sich nicht von Ort bewegen
        player.draw() # damit Spieler auf Bildschirm gezeigt wird
        
        text = font.render("Score: " + str(score), True, (0, 0, 0)) # WIrd in Zahl umgewandlet mit str, und (0,0,0) sagt welche Farbe der Text sein soll (SChwarz)
        screen.blit(text, (20, 20)) # wo der score angezeigt wird (linker echen oben)


        
    py.display.flip() # https://realpython.com/pygame-a-primer/#background-and-setup
      # haben auch mit dieser Website gearbeitet: https://realpython.com/pygame-a-primer/
