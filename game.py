import time
import warnings
import random
from gpiozero import Button
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
Hol = 0.2
down = Button(26,hold_repeat=True,hold_time=Hol)
up = Button(8,hold_repeat=True,hold_time=Hol)
left = Button(7,hold_repeat=True,hold_time=Hol)
right = Button(1,hold_repeat=True,hold_time=Hol)

lcd = CharLCD(cols=16, rows=2, pin_rs=4, pin_e=17, pins_data=[19,5,6,13,18, 22, 23, 24],numbering_mode=GPIO.BCM,
              auto_linebreaks=True,
              pin_backlight=None, backlight_enabled=True,compat_mode=True)
lcd.clear()

warnings.simplefilter("ignore")
line = (
	0b00000,
	0b00000,
	0b00000,
	0b11111,
	0b00000,
	0b00000,
	0b00000,
	0b00000
)
stickman = (
	0b00100,
	0b01010,
	0b00100,
	0b01110,
	0b10101,
	0b00100,
	0b01010,
	0b10001
)
lcd.create_char(1,stickman)
lcd.create_char(2,line)
def init():
    lcd.cursor_mode = "hide"
    up.when_pressed = up1
    up.when_held = up1
    down.when_pressed = down1
    down.when_held = down1
    left.when_pressed = left1
    left.when_held = left1
    right.when_pressed = right1
    right.when_held = right1



class Player:
    x = 0
    y = 0
    def __init__(self):
        self.update()
    def update(self):
        lcd.cursor_pos = (self.y, self.x)
        lcd.write_string(chr(1))
        lcd.cursor_pos = (self.y, self.x)
    def move(self,dir):
        if (dir == "up" and (self.y == 1)):
            lcd.cursor_pos = (self.y, self.x)
            lcd.write_string(" ")
            self.y -= 1
        elif (dir == "down" and (self.y == 0)):
            lcd.cursor_pos = (self.y, self.x)
            lcd.write_string(" ")
            self.y += 1
        elif (dir == "left" and (self.x >= 1 and self.x <= 15)):
            lcd.cursor_pos = (self.y, self.x)
            lcd.write_string(" ")
            self.x -= 1
        elif (dir == "right" and (self.x >= 0 and self.x < 14)):
            lcd.cursor_pos = (self.y, self.x)
            lcd.write_string(" ")
            self.x += 1
class Enemy:
    x = 15
    y = 0
    def __init__(self, x=None,y=None):
        if x == None and y == None:
            self.x = 15
            self.y = random.randint(0,1)
        else:
            self.x = x
            self.y = y
    def update(self):
        lcd.cursor_pos = (self.y, self.x)
        lcd.write_string(chr(2))
    def move(self,dir):
        if (dir == "left" and (self.x >= 1 and self.x <= 15)):
            lcd.cursor_pos = (self.y, self.x)
            lcd.write_string(" ")
            self.x -= 1
            self.update()
def Yes():
     lcd.cursor_pos = (1,0)
def No():
    lcd.cursor_pos = (1,9)

player = Player()
def down1():
    if(up.value == 0 and left.value == 0 and right.value == 0):
        player.move("down")
        player.update()
def up1():
    if(down.value == 0 and left.value == 0 and right.value == 0):
        player.move("up")
        player.update()
def left1():
    if(up.value == 0 and down.value == 0 and right.value == 0):
        player.move("left")
        player.update()
def right1():
    if(up.value == 0 and left.value == 0 and down.value == 0):
        player.move("right")
        player.update()
def do_None():
    up.when_pressed = None
    up.when_held = None
    down.when_pressed = None
    down.when_held = None
    left.when_pressed = None
    left.when_held = None
    right.when_pressed = None
    right.when_held = None

init()
score = 0

def logic():
    global Game
    global score
    X = None
    Y = None
    if random.random() < 0.5: # vary to make harder?
        if len(enemies) > 0:
            X = enemies[-1].x
            Y = enemies[-1].y
            if X == 14:
                enemies.append(Enemy(X+1,Y))
            else:
                enemies.append(Enemy())
        else:
            enemies.append(Enemy())

    for e in enemies[::-1]:
        e.move("left")
        if e.x == 0:
            enemies.remove(e)
            score += 1
        if (e.x == player.x and e.y == player.y):
            Game = False
def collision():
    for e in enemies[::-1]:
        if (e.x == player.x and e.y == player.y):
            Game = False

def start():
    speed = 0.5
    global enemies
    enemies = []
    gg = 1
    global Game
    Game = True
    while Game == True:
        if gg % 20 == 0 and round(speed,2) > 0.05:
            speed -= 0.05
        lcd.clear()
        logic()
        for e in enemies[::-1]:
            e.update()
        collision()
        player.update()
        time.sleep(round(speed,2))
        gg += 1

def Main_i_swear():
    global score,Game,enemies,speed
    start()
    lcd.clear()
    lcd.clear()
    do_None()
    print("wait 3 seconds")
    lcd.write_string(f"   Game Over !\n\rScore: {score}")
    time.sleep(3)
    print("press any key")
    while True:
        if(down.value == 1 or left.value == 1 or right.value == 1 or up.value == 1):
            lcd.clear()
            lcd.clear()
            lcd.cursor_pos = (0,0)
            print("press right or left to change option and then up or down to select")
            lcd.write_string("Play Again?\n\r+ YES    + NO")
            lcd.cursor_mode = "line"
            up.when_pressed = None
            up.when_held = None
            down.when_pressed = None
            down.when_held = None
            left.when_pressed = Yes
            left.when_held = None
            right.when_pressed = No
            right.when_held = None
            Yes()
            break
    time.sleep(1)
    while True:
        if(lcd.cursor_pos == (1,0) and (up.value == 1 or down.value == 1)):
            player.x = 0
            player.y = 0
            enemies = []
            speed = 0.5
            print("You chose Yes")
            init()
            Main_i_swear()
        if(lcd.cursor_pos == (1,9) and (up.value == 1 or down.value == 1)):
            print("You chose No")
            lcd.cursor_mode = "hide"
            lcd.clear()
            lcd.close()
            exit()

try:

    Main_i_swear()





except KeyboardInterrupt:
    lcd.clear()
    lcd.close(clear=True)

