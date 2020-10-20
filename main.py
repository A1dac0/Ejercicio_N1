# Mini-invaders, version 0.03
# (Imagen con teclado e imagen que rebota a la vez)
# Parte de la intro a Pygame, por Nacho Cabanes

from math import trunc
import pygame
import sys
from pygame.locals import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *

from utils_ import *
from utils import *

def world(x,y,width,height):
	Circle8v(x,y,120,255/255,233/255,0/255,10)
	for i in range(1,12):
		Circle8v(x,y,120-10*i,255/255,233/255,0/255,10)

	# vertices = [(-30-x,0-y),(-15-x,30-y),(-15-x,65-y),(-4-x,90-y),(-35-x,95-y),
    #             (-75-x,80-y),(-90-x,55-y),(-70-x,60-y),(-65-x,45-y),(-45-x,45-y)]
	# DrawPolygon(vertices,0/255,0/255,0/255,1)
	# SimpleSeedFill(width,height,1,vertices,-40-x,60-y,0/255,0/255,0/255)

def BarraSalud(x, y, daño ,salud,Colision):
    n,m= 15,150
    xf = x + m - daño
    Bressennham(x,y,xf,y,166/255,230/255,90/255,15)
    set_pixel(x,y,11/255,30/255,48/255,15)

    vertices = [(x+6,y-6),(x+6,y+n-6),(x+m+7,y+n-6),(x+m+7,y-6)]
    DrawPolygon(vertices,0/255,0/255,0/255,2)

    set_pixel(x+m+15,y,11/255,30/255,48/255,15)
    #SimpleSeedFill(width,height,scale,vertices2,0,0,0/255,100/255,0/255)




pygame.init()

# ancho = 800
# alto = 600
# velocidadX = 3
# velocidadY = 3
terminado = False

# pantalla = pygame.display.set_mode( (ancho, alto) )
scale = 1
width, height = 500, 500

pygame.init()
#display_openGL(width, height, scale)
ventana = pygame.display.set_mode((width, height), pygame.OPENGL)
pygame.display.set_caption('C.G. I')

#Colo de fondo
glClearColor(11/255,30/255,48/255,1.0)
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
glScalef(scale, scale, 0)
gluOrtho2D(-1 * width / 2, width / 2, -1 * height / 2, height / 2)
pygame.key.set_repeat(1,25)    # Nuevo en la version 0.03
 
# imagenMarciano = pygame.image.load("spaceinvader.png")
# rectanguloMarciano = imagenMarciano.get_rect()
# rectanguloMarciano.left = 200
# rectanguloMarciano.top = 100

# imagenNave = pygame.image.load("ufo.png")    # Nuevo en 0.03
# rectanguloNave = imagenNave.get_rect()       # Nuevo en 0.03
# rectanguloNave.left = ancho/2                # Nuevo en 0.03
# rectanguloNave.top = alto-50                 # Nuevo en 0.03

#Mundo   
#world(0,-280,width,height) # y = -280
x=-30
y=-170
vertices = [(-30-x,0-y),(-4-x,90-y),(-35-x,95-y),
                (-75-x,80-y),(-90-x,55-y)]

BarraSalud(80,200,145,100,False)
#Personaje Principal
x,y = 0,-100
x, y = MovePersonaje1(x, y, 0, 0, 1,10)
#x , y = ScaledPersonaje1(x,y,2,2,1,0)
#Opstaculos
sizeMeteorito = 1
x2 = random.randint(-200, 200)
y2 = 200
x2, y2 = MoveMeteorito(x2, y2, 0,0, sizeMeteorito,0)
salud = 100
#proyectil
xp =0
yp =0
sxp = 0
syp = 8
daño = 35
LanzoProyectil = False

while not terminado:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: terminado = True

    keys = pygame.key.get_pressed()          # Nuevo en 0.03
    if keys[K_LEFT]:                         # Nuevo en 0.03
        sx = 5
        sy = 0
        x, y = MovePersonaje1(x, y, sx, sy, 1,10)
    if keys[K_RIGHT]:                        # Nuevo en 0.03
        sx = -5
        sy = 0
        x, y = MovePersonaje1(x, y, sx, sy, 1,10)
    if keys[K_SPACE]:
        if(LanzoProyectil == False):
            xp , yp = LanzarProyectil(x+3,y+20,sxp,syp,1)
            LanzoProyectil = True

    #Colision
    x0 = x2-10
    xf = x2 + 10
    y0 = y2-10
    yf = y2 + 10
    yblock = y+10
    if( x >= x0 and x <= xf and yblock == y0 ):

        #despintar(x2,y2,0/255,0/255,0/255,1)
        sy = 0
        MoveMeteorito(x2, y2, 0, 0, sizeMeteorito,0)
        set_pixel(0,0,225/255,100/255,100/255,25)
        break
    else:
        sx = 0
        sy = -1
        x2, y2 = MoveMeteorito(x2, y2, sx, sy, sizeMeteorito,0)
        if(y2 <=  -200):
            x2 = random.randint(-200, 200)
            y2 = 200
            x2, y2 = MoveMeteorito(x2, y2, 0, 0, sizeMeteorito,0)
    #Se lanzo proyectil
    if(LanzoProyectil):
        xp,yp= LanzarProyectil(xp,yp,sxp,syp,1)
        #Existe colision entre proyectil y obstaculo
        if(xp >= x0 and xp<= xf and yp >= y0 and  yp <= yf):
            clearCanvas(11/255,30/255,48/255)
            world(0,-280,width,height)
            x, y = MovePersonaje1(x, y, 0, 0, scale,0)
            if salud > 0:
                salud -= daño
                LanzoProyectil  = False
            else:
                salud = 100
                LanzoProyectil  = False
                #despintar(x2,y2,1)
                #despintarProyectil(xp,yp,1)
                #LanzarProyectil(xp,yp,0,0,1)
                clearCanvas(11/255,30/255,48/255)
                world(0,-280,width,height)
                x, y = MovePersonaje1(x, y, 0, 0, scale,0)
                x2 = -400 #random.randint(-200, 200)
                sy = 0
                x2,y2 = MoveMeteorito(x2, -199, 0, 0, sizeMeteorito,0)
        elif yp >= 200:
            LanzoProyectil = False

    pygame.display.flip()
pygame.quit()