from math import *
eps = 1e-10

class Point:
    def __init__(self, x, y=None, polar=False):
        if isinstance(x, Point): # copy 
            self.x = x.x
            self.y = x.y
            self.r = (self.x**2 + self.y**2)**0.5
            self.a = x.a
        elif not polar:
            self.x = x
            self.y = y
            self.r = (self.x**2 + self.y**2)**0.5
            if x == 0:
                if y < 0:
                    self.a = 3 * pi / 2
                else:
                    self.a = pi / 2
            else:
                self.a = atan(y / x)
        else:
            self.x = x * cos(y)
            self.a = y
            self.y = x * sin(y)
            self.r = x
        if self.a < 0:
            self.a += 2 * pi
    
    def polar(self):
        if self.y >= 0:
            return acos(self.x / self.r)
        else:
            return 2 * pi - acos(self.x / self.r)    
            
    def __abs__(self):
        return self.r
    
    def dist(self, p2=None, pn=None):
        if p2 is not None:
            if pn is None:
                xx = p2.x - self.x
                yy = p2.y - self.y
            else:
                xx = p2 - self.x
                yy = pn - self.y
            return (xx**2 + yy**2)**0.5
        else:
            return self.r
        
    def __str__(self):
        return f"{self.x} {self.y}"
    
    def __add__(self, smth):
        return Point(self.x + smth.x, self.y + smth.y)

    def __sub__(self, smth):
        return Point(self.x - smth.x, self.y - smth.y)

    def __truediv__(self, n):
        return Point(self.x / n, self.y / n)

    def is_inside(self, p1, p2):
        x = self.x
        y = self.y
        a1 = p1.x
        a2 = p2.x
        b1 = p1.y
        b2 = p2.y
        v1 = Vector(self, p1)
        v2 = Vector(self, p2)
        if (x, y) == (a1, b1) or (x, y) == (a2, b2):
            return True
        else:
            if abs(v1 ^ v2) < eps and v1 * v2 < 0:
                return True
            else:
                return False
    

class Vector(Point):
    
    def __init__(self, x, y=None, polar=False, useless='f'):
        if polar == 'f':
            m = Vector(x.r, y + x.polar(), True)
            self.x = m.x
            self.y = m.y
            self.a = m.a
            self.r = m.r
        elif useless != 'f':
            p = Vector(Point(x, y), Point(polar, useless))
            self.x = p.x
            self.y = p.y
            self.a = p.a
            self.r = p.r
        elif isinstance(x, Point) and isinstance(y, Point):
            (x, y) = (y, x)
            self.x = x.x - y.x
            self.y = x.y - y.y
            if self.x == 0:
                if self.y < 0:
                    self.a = 3 * pi / 2
                else:
                    self.a = pi / 2
            else:
                self.a = atan(self.y / self.x)
            self.r = (self.x**2 + self.y**2)**0.5
        elif isinstance(x, Point):
            self.x = x.x
            self.y = x.y
            self.r = (self.x**2 + self.y**2)**0.5
            self.a = x.a
        elif not polar:
            self.x = x
            self.y = y
            self.r = (self.x**2 + self.y**2)**0.5
            if x == 0:
                if y < 0:
                    self.a = 3 * pi / 2
                else:
                    self.a = pi / 2
            else:
                self.a = atan(y / x)
        else:
            self.x = x * cos(y)
            self.a = y
            self.y = x * sin(y)
            self.r = x
        if self.a < 0:
            self.a += 2 * pi
        self.a = atan2(self.x, self.y)
            
    def dot_product(self, p2):
        return self.x * p2.x + self.y * p2.y
    
    def __mul__(self, p2):
        return Vector(self.x * p2, self.y * p2)
    
    def cross_product(self, p2):
        return self.x * p2.y - self.y * p2.x
    
    def __xor__(self, p2):
        return self.x * p2.y - self.y * p2.x
        
    def __rmul__(self, p2):
        return Vector(self.x * p2, self.y * p2)
        
    def to_length(self, x):
        k = x / self.r
        return Vector(self.x * k, self.y * k)
    
    def angle(self, v2):
        alpha = self.a
        beta = v2.a
        return min(abs(alpha - beta), 2 * pi - abs(alpha - beta))    
    

class Line:
    
    def __init__(self, p1, p2, c=None):
        if isinstance(p2, Vector):
            # point + vector
            luchshaia_pramaia = Line(p1, p1 + p2)
            self.a = luchshaia_pramaia.a
            self.b = luchshaia_pramaia.b
            self.c = luchshaia_pramaia.c
            self.v = p2
        elif isinstance(p2, Line):
            self.const = p2
            luchshaia_pramaia = Line(p1, p2.basement(p1))
            self.a = luchshaia_pramaia.a
            self.b = luchshaia_pramaia.b
            self.c = luchshaia_pramaia.c
            self.v = p2            
        elif c is None:
            # 2 points
            self.p1 = p1
            self.p2 = p2
            self.a = p2.y - p1.y
            self.b = -p2.x + p1.x
            self.c = p1.y * p2.x - p2.y * p1.x
            self.v = Vector(-self.b, self.a)
        else:
            # 3 k
            self.a = p1
            self.b = p2
            self.c = c
            self.v = Vector(-self.b, self.a)
        self.normal = Vector(self.a, self.b)
    def __str__(self):
        return f"{self.a} {self.b} {self.c}"
    
    
    def perp(self, p):
        c = -p.x * self.b + p.y * self.a
        l = Line(self.b, -self.a, c)
        l.p1 = p
        l.p2 = self.basement(p)
        return l
    
    def inline(self, p):
        if abs(self.b) > eps:
            goodP = Point(0, -self.c / self.b)
        else:
            goodP = Point(-self.c / self.a, 0)
        newLine = Line(p, goodP)
        if self.same(newLine):
            return 'YES'
        else:
            return 'NO'


    def same(self, line):
        if abs(line.a) > eps:
            k = self.a / line.a
        elif abs(line.b) > eps:
            k = self.b / line.b
        else:
            return True
        line.a *= k
        line.b *= k
        line.c *= k
        if abs(self.a - line.a) < eps and abs(self.b - line.b) < eps and abs(self.c - line.c) < eps:
            return True
        else:
            return False
        
    def par(self, line):
        if abs(line.a) > eps:
            k = self.a / line.a
        else:
            k = self.b / line.b
        line.a *= k
        line.b *= k
        line.c *= k        
        if abs(self.a - line.a) < eps and abs(self.b - line.b) < eps:
            return True
        else:
            return False
    
    def is_it_perp(self, line):
        if abs(line.a) > eps:
            k = self.a / line.a
        else:
            k = self.b / line.b
        line.a *= k
        line.b *= k
        line.c *= k
        if (abs(self.a + 1 / line.a) < eps and abs(self.b - 1 / line.b) < eps) or (abs(self.b + 1 / line.b) < eps and abs(self.a - 1 / line.a) < eps):
            return True
        else:
            return False
    
    def in_both(self, line):
        if abs(self.a * line.b - self.b * line.a) > eps:
            y = (self.c * line.a - line.c * self.a) / (self.a * line.b - self.b * line.a)
            if abs(self.a) > eps:
                x = (-self.c - self.b * y) / self.a
            else:
                x = (-line.c - line.b * y) / line.a
            return Point(x, y)
        else:
            return None    
    
    def basement(self, p):
        left_lion = Line(-self.b, self.a, self.b * p.x - self.a * p.y)
        fight_point = self.in_both(left_lion)
        return fight_point

    def move(self, x):
        if self.b == 0:
            return f"{self.a} {self.b} {self.c + x * self.a}"
        elif self.a == 0:
            return f"{self.a} {self.b} {self.c + x * self.b}"
        else:
            return f"{self.a} {self.b} {self.c - x * self.b / cos(self.alpha)}"            
    
    
class Circle:
    
    def __init__(self, x, y, r):
        if r is None:
            self.x = x.x
            self.y = x.y
            self.p = x
            self.r = Vector(self.p, y).r
            self.ponc = y
            print('y', type(y))
        else:
            self.x = x
            self.y = y
            self.r = r  
            self.p = Point(self.x, self.y)
            self.ponc = Point(self.x, self.y + r)
    def touching(self, p):
        gpt = Vector(p, self.p)
        if gpt.r < self.r:
            return []
        else:
            alpha = asin(self.r / gpt.r)
            t1 = Vector(gpt, alpha, 'f')
            t2 = Vector(gpt, -alpha, 'f')
            l1 = Line(p, t1)
            l2 = Line(p, t2)
            pp1 = l1.basement(self.p)
            pp2 = l2.basement(self.p)
            if Vector(pp1, pp2).r > eps:
                return [pp1, pp2]
            else:
                return [pp1]
            
    def cross(self, line):
        s = Vector(self.p, line.basement(self.p))
        if s.r > self.r:
            return []
        elif abs(s.r - self.r) < eps:
            return [line.basement(self.p)]
        else:
            if s.r > eps:
                delta = acos(s.r / self.r)
                k = self.r / s.r
                p1 = Vector(s, delta, 'f') * k
                p1 += self.p
                p2 = Vector(s, -delta, 'f') * k + self.p
                return [p1, p2]
            else:
                u = line.v.to_length(self.r)
                p1 = self.p + u
                p2 = self.p - u
                return [p1, p2]
    
    def __str__(self):
        return f"{self.x} {self.y} {self.r}"
            
            
class Triangle:
    
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        
    def addS(self):
        self.s1 = Vector(self.p2, self.p3)
        self.s2 = Vector(self.p3, self.p1)
        self.s3 = Vector(self.p1, self.p2)
        
    def addSide(self):
        self.addS()
        self.side1 = Line(self.p2, self.s1)
        self.side2 = Line(self.p3, self.s2)
        self.side3 = Line(self.p1, self.s3)
        self.delS()
        
    def addM(self):
        self.addS()
        self.m1 = Vector(self.p1, self.p2 + self.s1 / 2)
        self.m2 = Vector(self.p2, self.p3 + self.s2 / 2)
        self.m3 = Vector(self.p3, self.p3 + self.s3 / 2)
        self.mbase1 = self.p1 + self.m1
        self.mbase2 = self.p2 + self.m2
        self.mbase3 = self.p3 + self.m3
        self.delS()
        
    def addH(self):
        self.addSide()
        self.h1 = self.side1.basement(self.p1)
        self.h2 = self.side2.basement(self.p2)
        self.h3 = self.side3.basement(self.p3)
        self.delSide()
    
    def addA(self):
        self.addS()
        self.a1 = self.s3.angle(-1 * self.s2)
        self.a2 = self.s1.angle(-1 * self.s3)
        self.a3 = self.s2.angle(-1 * self.s1)
        self.delS()
        
    def delS(self):
        del self.s1
        del self.s2
        del self.s3
    
    def delSide(self):
        del self.side1
        del self.side2
        del self.side3
    
    def delM(self):
        del self.m1
        del self.m2
        del self.m3
        del self.mbase1
        del self.mbase2
        del self.mbase3
    
    def delH(self):
        del self.h1
        del self.h2
        del self.h3
        
    def delA(self):
        del self.a1
        del self.a2
        del self.a3
        
    def medcros(self):
        self.addM()
        med1 = Line(self.p1, self.m1)
        med2 = Line(self.p2, self.m2)
        self.delM()
        return med1.in_both(med2)
    
    def hcros(self):
        self.addH()
        x = Line(self.p1, self.h1).in_both(Line(self.p2, self.h2))
        self.delH()
        return x

    def mpercros(self):
        self.addM()
        self.addSide()
        prp1 = self.side1.perp(self.mbase1)
        prp2 = self.side2.perp(self.mbase2)
        x = prp1.in_both(prp2)
        self.delM()
        self.delSide()
        return x
    
    def bigC(self):
        p = self.mpercros()
        r = Vector(p, self.p1).r
        return Circle(p.x, p.y, r)
    
    def bis(self, x):
        if x == 1:
            v1 = Vector(self.p1, self.p2)
            v2 = Vector(self.p1, self.p3)
            pp = self.p1
        elif x == 2:
            v1 = Vector(self.p2, self.p1)
            v2 = Vector(self.p2, self.p3)
            pp = self.p2
        elif x == 3:
            v1 = Vector(self.p3, self.p1)
            v2 = Vector(self.p3, self.p2)
            pp = self.p3
        a = v1.angle(v2)
        b = Vector(v1, a / 2, 'f')
        if b.angle(v2) > v1.angle(v2):
            b = Vector(v1, -a / 2, 'f')
        return Line(pp, b)
    
    def biscros(self):
        return self.bis(3).in_both(self.bis(1))
    
    def smalestC(self):
        self.addA()
        if self.a1 < pi / 2 and self.a2 < pi / 2 and self.a3 < pi / 2:
            x = self.bigC()
        else:
            self.addS()
            if self.s1.r == max(self.s1.r, self.s2.r, self.s3.r):
                p = self.p2 + self.s1 / 2
                r = self.s1.r / 2
            elif self.s2.r == max(self.s1.r, self.s2.r, self.s3.r):
                p = self.p3 + self.s2 / 2
                r = self.s2.r / 2
            else:
                p = self.p1 + self.s3 / 2
                r = self.s3.r / 2
            x = Circle(p.x, p.y, r)
        self.delA()
        return x
        
    def inC(self):
        self.addSide()
        p = self.biscros()
        r = Vector(p, self.side1.basement(p)).r
        self.delSide()
        return Circle(p.x, p.y, r)
    
    def inT(self, p):
        if abs(p - p1) < eps or abs(p - p2) < eps or abs(p - p3) < eps:
            return True
        else:
            self.addSide()
            l1 = Line(p, self.p1)
            l2 = Line(p, self.p2)
            l3 = Line(p, self.p3)
            i1 = l1.in_both(self.side1)
            i2 = l2.in_both(self.side2)
            i3 = l3.in_both(self.side3)
            if i1 is not None and i2 is not None and i3 is not None:
                if i1.is_inside(p3, p2) and i2.is_inside(p1, p3) and i3.is_inside(p1, p2):
                    x = True
                else:
                    x = False
                self.delSide()
                return x
            else:
                return False
    
def closest(p, ps):
    r = Vector(p, ps[0]).r
    clp = ps[0]
    for x in ps:
        newr = Vector(p, x).r
        if newr < r:
            r = newr
            clp = x
    return clp

def closestl(p, ls):
    d = Vector(ls[0].basement(p), p).r
    cll = ls[0]
    for x in ls:
        newd = Vector(x.basement(p), p).r
        if newd < d:
            d = newd
            cll = x
    return cll

def closestc(p, cs):
    d = abs(Vector(p, cs[0].p).r - cs[0].r)
    clc = cs[0]
    for x in cs:
        newd = abs(Vector(p, x.p).r - x.r)
        if newd < d:
            d = newd
            clc = x
    return clc

def closestt(p, ts):
    clt = ts[0]
    x = clt
    d = Vector(p, x.p1).r + Vector(p, x.p2).r + Vector(p, x.p3).r
    for x in ts:
        s = Vector(p, x.p1).r + Vector(p, x.p2).r + Vector(p, x.p3).r
        x.addS()
        s /= (x.s1.r + x.s2.r + x.s3.r)
        x.delS()
        if s < d:
            d = s
            clt = x
    return clt

def sideps(p1, p2):
    l = Line(p1, p2)
    if l.a == 0:
        p1 = Point(1500, -l.c / l.b)
        p2 = Point(-1500, -l.c / l.b)
    else:
        p1 = Point((-l.c - 1500 * l.b) / l.a, 1500)
        p2 = Point((-l.c + 1500 * l.b) / l.a, -1500)
    return [p1, p2]
