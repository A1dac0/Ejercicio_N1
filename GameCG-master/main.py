from math import trunc
import pygame
import sys
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *

from utils_v2 import *
from utils import *

#Pintar Planeta
def world(x,y,width,height):
	Circle8v(x,y,120,255/255,233/255,0/255,10)
	for i in range(1,12):
		Circle8v(x,y,120-10*i,255/255,233/255,0/255,10)
#Pintar Barra de salud del planeta
def BarraSaludPlaneta(daño , salud = 150, x = 80, y= 235):
    n,m= 15,150
    xf = x + m - daño
    Bressennham(x,y,xf,y,166/255,230/255,90/255,15)
    set_pixel(x,y,11/255,30/255,48/255,15)

    vertices = [(x+6,y-6),(x+6,y+n-6),(x+m+7,y+n-6),(x+m+7,y-6)]
    DrawPolygon(vertices,0/255,0/255,0/255,2)

    set_pixel(x+m+15,y,11/255,30/255,48/255,15)

    salud -=daño
    return salud
#Pintar Barra Salud de la Nave
def BarraSaludNave(daño,salud = 150,x = 80, y = 210):
    n,m= 15,150
    xf = x + m - daño
    Bressennham_(x,y,xf,y,247/255,255/255,255/255,15)
    set_pixel(x,y,11/255,30/255,48/255,15)

    vertices = [(x+6,y-6),(x+6,y+n-6),(x+m+7,y+n-6),(x+m+7,y-6)]
    DrawPolygon(vertices,0/255,0/255,0/255,2)

    set_pixel(x+m+15,y,11/255,30/255,48/255,15)

    salud -=daño
    return salud

#Pintar estrellas en el canvas aleatoriamente
def Estrellas(n):
    for k in range(n):
        x = random.randint(-200, 200)
        y = random.randint(-150, 200)
        set_pixel(x,y,255/255,255/255,255/255,2)

#Detecta colision entre meteorito y el planeta
def Colision_MT(x,y,x0,xf,h):
    if(x >= x0 and x <= xf):
        if(y <= h):
            return True
        else:
            return False
    else:
        return False
def Repintar(k,k_nave,x_nave,y_nave,x_meteorito,y_meteorito):
    clearCanvas(11/255,30/255,48/255)
    world(0,-280,width,height)
    Estrellas(40)
    vidaPlaneta = BarraSaludPlaneta(10*k)
    vidaNave = BarraSaludNave(20*k_nave)
    x, y = MovePersonaje1(x_nave, y_nave, 0, 0, scale,0)
    x2, y2 = MoveMeteorito(x_meteorito, y_meteorito, 0, 0, sizeMeteorito,0)
    return x,y,x2,y2,vidaPlaneta,vidaNave

#Iniciar
terminado = False
scale = 1
width, height = 500, 500

pygame.init()

ventana = pygame.display.set_mode((width, height), pygame.OPENGL)
pygame.display.set_caption('C.G. I')
#pygame.mixer.music.load("musicadefondo.ogg")
#pygame.mixer.music.play(-1)

#Colo de fondo
glClearColor(11/255,30/255,48/255,1.0)
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
glScalef(scale, scale, 0)
gluOrtho2D(-1 * width / 2, width / 2, -1 * height / 2, height / 2)
pygame.key.set_repeat(1,25)

#Planeta
radio = 120
world(0,-280,width,height)
Estrellas(40)

#Barras de Salud
vidaPlaneta = BarraSaludPlaneta(0)
vidaNave = BarraSaludNave(0)

#Personaje Principal
x,y = 0,-100    #Posicion inicial
x, y = MovePersonaje1(x, y, 0, 0, 1,10)

#Meteoritos
sizeMeteorito = 1
x2 = random.randint(-200, 200)  #Coordenada aleatoria
y2 = 200
x2, y2 = MoveMeteorito(x2, y2, 0,0, sizeMeteorito,0)
salud = 100

#Proyectil
xp =0   #Posicion Incial
yp =0   #Posicion inicial
sxp = 0
syp = 8
daño = 35   #Daño proyectil
LanzoProyectil = False
score = 0
K_Nave = 0
K = 0
sonidodisparo=pygame.mixer.Sound("shoot.ogg")
impacto=pygame.mixer.Sound("explosion.ogg")
destruirmete=pygame.mixer.Sound("invaderkilled.ogg")
destruirplaneta=pygame.mixer.Sound("planetaexpl.ogg")
while not terminado and vidaPlaneta >= 0 and vidaNave >= 0 and score < 20:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminado = True
    
    keys = pygame.key.get_pressed()          # Nuevo en 0.03
    if keys[K_LEFT]:                         # Nuevo en 0.03
        sx = 5
        sy = 0
        x, y = MovePersonaje1(x, y, sx, sy, 1,10)
    if keys[K_RIGHT]:                        # Nuevo en 0.03
        sx = -5
        sy = 0
        x, y = MovePersonaje1(x, y, sx, sy, 1,10)
    if keys[K_UP]:
        sx = 0
        sy = 5
        x, y = MovePersonaje1(x, y, sx, sy, 1,10)
    if keys[K_DOWN]:
        sx = 0
        sy = -5
        x, y = MovePersonaje1(x, y, sx, sy, 1,10)
    #Tecla Espacio para Lanzar proyectiles
    if keys[K_SPACE]:
        if(LanzoProyectil == False):
            xp , yp = LanzarProyectil(x+3,y+20,sxp,syp,1)
            LanzoProyectil = True
            sonidodisparo.play()

    #Colision
    x0 = x2-10
    xf = x2 + 10
    y0 = y2-10
    yf = y2 + 10
    yblock = y+10
    #Meteorito impacta con la nave
    if( x >= x0 and x <= xf and yblock == y0 ):
        K_Nave += 1
        impacto.play()
        #Nuevas coordenada para el meteorito
        x2 = random.randint(-200, 200)
        y2 = 200
        #Repintamos todos los elementos y recuperamos sus posiciones
        x,y,x2,y2,vidaPlaneta,vidaNave =  Repintar(K,K_Nave,x,y,x2,y2)
    else:
        sx = 0
        sy = -1
        x2, y2 = MoveMeteorito(x2, y2, sx, sy, sizeMeteorito,0)

        #Colision del Meteorito con el Planeta
        if(Colision_MT(x2,y2,-radio,radio,radio-256)):
            K+=1
            destruirplaneta.play()
            #Pintar Nave y Meteorito
            x2 = random.randint(-200, 200)
            y2 = 200
            x,y,x2,y2,vidaPlaneta,vidaNave =  Repintar(K,K_Nave,x,y,x2,y2)
        #Meteorito reinicia su recorrido
        if(y2 <=  -250 ):
            x2 = random.randint(-200, 200)
            y2 = 200
            x2, y2 = MoveMeteorito(x2, y2, 0, 0, sizeMeteorito,0)

    #Se lanzo proyectil
    if(LanzoProyectil):
        xp,yp= LanzarProyectil(xp,yp,sxp,syp,1)
        #Existe colision entre proyectil y obstaculo
        if(xp >= x0 and xp<= xf and yp >= y0 and  yp <= yf):
            destruirmete.play()
            clearCanvas(11/255,30/255,48/255)
            Estrellas(40)
            vidaPlaneta =  BarraSaludPlaneta(10*K)
            vidaNave = BarraSaludNave(20*K_Nave)
            world(0,-280,width,height)
            x, y = MovePersonaje1(x, y, 0, 0, scale,0)

            if salud > 0:
                salud -= daño
                LanzoProyectil  = False
            else:
                score += 1
                salud = 100
                LanzoProyectil  = False

                clearCanvas(11/255,30/255,48/255)
                Estrellas(40)
                vidaPlaneta =  BarraSaludPlaneta(10*K)
                vidaNave = BarraSaludNave(20*K_Nave)
                world(0,-280,width,height)
                x, y = MovePersonaje1(x, y, 0, 0, scale,0)
                x2 = random.randint(-200, 200)
                x2,y2 = MoveMeteorito(x2, -249, 0, 0, sizeMeteorito,0)

        elif yp >= 260:
            LanzoProyectil = False
            vidaPlaneta =  BarraSaludPlaneta(10*K)
            vidaNave = BarraSaludNave(20*K_Nave)
    pygame.display.flip()
pygame.quit()