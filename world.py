import pygame
from geometry import *

color_color = (200, 200, 0)
base_color = (0, 0, 0)
print('f')
a = 500
size = (a, a)
screen = pygame.display.set_mode(size)
scc = (255, 255, 255)
screen.fill(scc)
print('r')
class Dpoint(Point):
    def __init__(self, x, y=None, polar=False):
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
        self.colored = False
        
    def draw(self):
        global color_color, base_color
        if self.colored:
            circ(int(self.x), int(self.y), 2, color_color)
        else:
            circ(int(self.x), int(self.y), 2, base_color)
    
    def right(self, fps):
        self.x += 50 / fps
    
    def left(self, fps):
        self.x -= 50 / fps
    
    def up(self, fps):
        self.y -= 50 / fps
    
    def down(self, fps):
        self.y += 50 / fps
        
class Dcircle(Circle):
    def __init__(self, x, y, r=None):
        super().__init__(x, y, r)
        self.colored = False
    
    def draw(self):
        global color_color, base_color
        if self.colored:
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

while running:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #ckicked
                x = event.pos[0]
                y = event.pos[1]                
                if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]: # make a new or select
                    if pressed[pygame.K_l]: # select line
                        print('line selection')
                        thatL = closestl(Dpoint(x, y), ls)
                        if thatL.colored:
                            thatL.colored = False
                            chosenl.remove(thatL)
                        else:
                            chosenl.append(thatL)
                            thatL.colored = True
                    elif pressed[pygame.K_t]:
                        thatT = closestt(Dpoint(x, y), ts)
                        if thatT.colored:
                            thatT.colored = False
                            chosent.remove(thatT)
                        else:
                            chosent.append(thatT)
                            thatT.colored = True
                    elif pressed[pygame.K_c]:
                        print('circle selected')
                        thatC = closestc(Dpoint(x, y), cs)
                        if thatC.colored:
                            thatC.colored = False
                            chosenc.remove(thatC)
                        else:
                            chosenc.append(thatC)
                            thatC.colored = True                        
                    else: # select point
                        print('point selection')
                        thatP = closest(Dpoint(x, y), ps)
                        if thatP.colored:
                            thatP.colored = False
                            chosen.remove(thatP)
                        else:
                            chosen.append(thatP)
                            thatP.colored = True
                else:
                    newP = Dpoint(x, y)
                    ps.append(newP)
        elif event.type == pygame.KEYDOWN:
            if pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]:
                if event.key == pygame.K_i:
                    if len(chosenl) == 2:
                        newP = Dpoint(chosenl[0].in_both(chosenl[1]))
                        ps.append(newP)
                        clean_chosenl()
                    elif len(chosenl) == 1 and len(chosenc) == 1:
                        glt = chosenc[0].cross(chosenl[0])
                        newP = Dpoint(glt[0])
                        ps.append(newP)
                        newP = Dpoint(glt[1])
                        ps.append(newP)
                        clean_chosenc()
                        clean_chosenl()
                    else:
                        print("Wrong amount of selected lines")
                elif event.key == pygame.K_d:
                    destroy()
                elif event.key == pygame.K_t:
                    if len(chosen) == 3:
                        newT = Dtriangle(chosen[0], chosen[1], chosen[2])
                        ts.append(newT)
                        clean_chosen()
                    else:
                        print("Wrong amount of selected points")
                elif event.key == pygame.K_l:
                    if len(chosen) == 2:
                        ls.append(Dline(chosen[0], chosen[1]))
                        clean_chosen()
                elif event.key == pygame.K_c:
                    if len(chosen) == 2:
                        cs.append(Dcircle(chosen[0], chosen[1]))
                        clean_chosen()
                    else:
                        print("Wrong amount of selected points")
                elif event.key == pygame.K_k:
                    if len(chosen) == 1 and len(chosenc) == 1:
                        gln = chosenc[0].touching(chosen[0])
                        newP = Dpoint(gln[0])
                        ps.append(newP)
                        l1 = Dline(chosen[0], newP)
                        ls.append(l1)
                        if len(gln) == 2:
                            ps.append(Dpoint(gln[1]))                            
                            l2 = Dline(chosen[0], gln[1])
                            ls.append(l2)
                        clean_chosen()
                        clean_chosenc()
                    else:
                        print("Wrong amount of selected points or circles")
                elif event.key == pygame.K_a:
                    clean_chosen()
                    clean_chosenc()
                    clean_chosenl()
                    clean_chosent()
                elif event.key == pygame.K_p:
                    if len(chosen) == 1 and len(chosenl) == 1:
                        newL = Dline(chosen[0], chosenl[0])
                        newL.p1 = chosen[0]
                        newL.const = chosenl[0]
                        ls.append(newL)
                        clean_chosen()
                        clean_chosenl()
        
    if pressed[pygame.K_DOWN]:
        for x in chosen:
            x.down(fps)
    elif pressed[pygame.K_UP]:
        for x in chosen:
            x.up(fps)
    elif pressed[pygame.K_RIGHT]:
        for x in chosen:
            x.right(fps)
    elif pressed[pygame.K_LEFT]:
        for x in chosen:
            x.left(fps)            
    
    screen.fill(scc)
    for x in ps:
        x.draw()
    for x in ts:
        x.draw()
    for x in ls:
        x.draw()
    clock.tick(fps)
    for x in cs:
        x.draw()
    pygame.display.update()