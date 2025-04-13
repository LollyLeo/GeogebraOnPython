import pygame
from geometry import *

color_color = (0, 0, 0)
base_color = (255, 0, 0)
print('f')
a = 500
size = (a, a)
screen = pygame.display.set_mode(size)
scc = (255, 255, 255)
screen.fill(scc)
running = True


class Dpoint(Point):
    def __init__(self, x, y=None, polar=False):
        self.X = 0
        self.Y = 0
        if isinstance(x, Point):
            np = Dpoint(x.x, x.y)
            self.x = np.x
            self.y = np.y
            self.r = (self.x**2 + self.y**2)**0.5
            self.a = np.a
            if self.a < 0:
                self.a += 2 * pi
        else:
            super().__init__(x, y, polar)
            
        global v
        self.v = v/fps
        w = 0
        self.speedX = w
        self.speedY = w
        self.allowed = True
        #self.speedX = sqrt(50)
        #self.speedY = sqrt(50)        
        
    def draw(self):
        global color_color, base_color
        circ(int(self.x), int(self.y), 2, base_color)
        
class Dcircle(Circle):
    def __init__(self, x, y, r=None):
        super().__init__(x, y, r)
        self.colored = False
    
    def draw(self):
        global color_color, base_color
        if not self.colored:
            circ(int(self.p.x), int(self.p.y), int(Vector(self.p, self.ponc).r), color_color, 1)
        else:
            circ(int(self.p.x), int(self.p.y), int(Vector(self.p, self.ponc).r), base_color, 1)

class Dline(Line):
    def __init__(self, p1, p2=None, c=None):
        if isinstance(p1, Line):
            self.a = p1.a
            self.b = p1.b
            self.c = p1.c
            self.p1 = p1.p1
            self.p2 = p1.p2
            self.v = p1.v
        else:
            super().__init__(p1, p2, c)
        self.colored = False
        self.const = 'f'
    
    def draw(self):
        global color_color, base_color
        if self.const != 'f':
            glt = sideps(self.p1, self.p1 + self.const.normal)
        else:
            glt = sideps(self.p1, self.p2)
        pp1 = glt[0]
        pp2 = glt[1]
        if self.colored:
            seg(pp1.x, pp1.y, pp2.x, pp2.y, color_color)
        else:
            seg(pp1.x, pp1.y, pp2.x, pp2.y, base_color)

class Dtriangle(Triangle):
    def __init__(self, p1, p2, p3):
        super().__init__(p1, p2, p3)
        self.colored = False
    
    def draw(self):
        if self.colored:
            seg(self.p1.x, self.p1.y, self.p2.x, self.p2.y, color_color)
            seg(self.p3.x, self.p3.y, self.p2.x, self.p2.y, color_color)
            seg(self.p1.x, self.p1.y, self.p3.x, self.p3.y, color_color)
        else:
            seg(self.p1.x, self.p1.y, self.p2.x, self.p2.y, base_color)
            seg(self.p3.x, self.p3.y, self.p2.x, self.p2.y, base_color)
            seg(self.p1.x, self.p1.y, self.p3.x, self.p3.y, base_color)            
            
def line(x1, y1, x2, y2, color = (0, 0, 0), t = 1, scr = screen):
    pygame.draw.line(scr, color, (x1, y1), (x2, y2), t)

def rect(x1, y1, x2, y2, color = (0, 0, 0), t = 1, scr = screen):
    pygame.draw.rect(scr, color, (x1, y1, x1+x2, y1+y2), t)

def circ(x, y, r, color = (0, 0, 0), t = 0, scr = screen):
    pygame.draw.circle(scr, color, (x, y), r, t)

def seg(x1, y1, x2, y2, color = (0, 0, 0), t = 1, scr = screen):
    pygame.draw.aaline(scr, color, (x1, y1), (x2, y2), t)

def clean_chosen():
    global chosen
    for x in chosen:
        x.colored = False
    chosen = []

def clean_chosenl():
    global chosenl
    for x in chosenl:
        x.colored = False
    chosenl = []
    
def clean_chosenc():
    global chosenc
    for x in chosenc:
        x.colored = False
    chosenc = []
    
def clean_chosenc():
    global chosenc
    for x in chosenc:
        x.colored = False
    chosenc = []

def clean_chosent():
    global chosent
    for x in chosent:
        x.colored = False
    chosent = []

def destroy():
    global ps, ls, ts, cs, chosen, chosenl, chosent, chosenc
    for x in chosen:
        ps.remove(x)
    for x in chosenl:
        ls.remove(x)
    for x in chosent:
        ts.remove(x)
    for x in chosenc:
        cs.remove(x)   
    chosen = []
    chosenl = []
    chosent = []
    chosenc = []


    
X = 250
Y = 250
R = 75
v = 300
fps = 600
pond = Dcircle(X, Y, R)
speed = 0.002 * fps

class Wolf(Dpoint):
    def move(self, pond=pond):
        global speed
        v = Vector(Vector(pond.p, Point(self.X + self.x, self.Y + self.y)), pi / 2, 'f').to_length(speed)
        self.X += v.x
        self.Y += v.y
        if self.X >= 1:
            self.x += floor(self.X) 
            self.X -= 1
        if self.X <= -1:
            self.x -= floor(abs(self.X)) 
            self.X += 1
        if self.Y >= 1:
            self.y += floor(self.Y) 
            self.Y -= 1
        elif self.Y <= -1:
            self.y -= floor(abs(self.Y))
            self.Y += 1
        print(self.X)
        """wnow = (self - pond.p).polar()
        hnow = Vector(pond.p, hare).polar()
        if wnow - hnow > 0:
            diract = 'r'
        else:
            diract = 'l'"""
        
setup = 'p'
colored = []
pygame.event.pump
running = True
clock = pygame.time.Clock()
fps = 70
ps = []
ls = []
ts = []
cs = []
chosen = []
chosenl = []
chosent = []
chosenc = []

o = 2 * pi / R
wolf = Wolf(X, Y - R)
ps.append(wolf)
cs.append(pond)

def vh(hare, wolf, c=pond):
    global speed
    v = Vector(wolf, hare)
    v = Vector(pond.p, v).to_length(speed)
    return v
def vw(wolf, hare, c=pond):
    hof = pond.p +  0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
    screen.fill(scc)
    for x in ps:
        x.move()
        x.draw()
    for x in ts:
        x.draw()
    for x in ls:
        x.draw()
    for x in cs:
        x.draw()
        
    clock.tick(fps)
    pygame.display.update()    