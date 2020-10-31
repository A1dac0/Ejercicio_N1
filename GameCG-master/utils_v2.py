# pip install PyOpenGL
# pip install pygame
# pip install pygame==2.0.0.dev6 (for python 3.8.x)
# pip install numpy
# Python 3.8

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import math
import random as rdn
import numpy as np

### Algorithm ###
def floodfill(matrix, x, y):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
    if matrix[x][y] == "a":
        matrix[x][y] = "c"
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            floodfill(matrix,x-1,y)
        if x < len(matrix[y]) - 1:
            floodfill(matrix,x+1,y)
        if y > 0:
            floodfill(matrix,x,y-1)
        if y < len(matrix) - 1:
            floodfill(matrix,x,y+1)

def set_pixel2(x, y, r, g, b,alfa, size):
	glColor4f(r, g, b,alfa)
	glPointSize(size)

	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()
def set_pixel(x, y, r, g, b, size):
	glColor3f(r, g, b)
	glPointSize(size)

	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()

	# print("{}\t{}".format(x, y))
	# pygame.time.wait(100)

	# option 1 (ok)
	# pygame.display.flip()

	# option 2
	# glFlush()

def color_pixel(width, height, x, y, size):
	rgb = glReadPixels(width / 2 + x , height / 2 + y, size ,size , 
						GL_RGB, GL_UNSIGNED_BYTE, None)
	return list(rgb)

def clearCanvas():
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def Traslate(vertices, tx, ty):
	T = [
		[1, 0, tx],
		[0, 1, ty],
		[0, 0, 1]
	]
	result = []
	for item in vertices:
		point = np.dot(T, item)
		result.append(point)
	return result
def Rotation(vertices, angle):
	angle = math.radians(angle)
	R = [
		[math.cos(angle), -math.sin(angle), 0],
		[math.sin(angle), math.cos(angle), 0],
		[0, 0, 1]
	]
	result = []
	for item in vertices:
		point = np.dot(R, item)
		result.append(point)
	return result
def Scaled(vertices,sx,sy):
	R=[
		[sx,0,0],
		[0,sy,0],
		[0,0,1]
	]
	result = []
	for item in vertices:
		point = np.dot(R,item)
		result.append(point)
	return result
def proyectil(x, y, size):
	matrix =   [[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 0, 5, 0, 1, 1, 1, 1],
				[1, 1, 1, 0, 5, 5, 5, 0, 1, 1, 1],
				[1, 1, 1, 0, 5, 5, 5, 0, 1, 1, 1],
				[1, 1, 1, 0, 6, 6, 6, 0, 1, 1, 1],
				[1, 1, 1, 0, 6, 6, 6, 0, 1, 1, 1],
				[1, 1, 1, 0, 6, 6, 6, 0, 1, 1, 1],
				[1, 1, 1, 0, 6, 6, 6, 0, 1, 1, 1],
				[1, 1, 0, 0, 6, 6, 6, 0, 0, 1, 1],
				[1, 0, 5, 0, 6, 6, 6, 0, 5, 0, 1],
				[0, 5, 5, 0, 6, 6, 6, 0, 5, 5, 0],
				[0, 5, 5, 0, 6, 6, 6, 0, 5, 5, 0],
				[0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
				[1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
				[1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1],
				[1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1],
				[1, 1, 1, 2, 4, 4, 3, 2, 1, 1, 1],
				[1, 1, 1, 2, 4, 4, 4, 2, 1, 1, 1],
				[1, 1, 1, 1, 2, 4, 2, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]]

	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == 0:
				set_pixel(y - j, x - i, 44/255, 44/255, 44/255, size)
			if matrix[i][j] == 2:
				set_pixel(y - j, x - i, 82/255, 16/255, 8/255, size)
			if matrix[i][j] == 3:
				set_pixel(y - j, x - i, 235/255, 94/255, 40/255, size)
			if matrix[i][j] == 4:
				set_pixel(y - j, x - i, 224/255, 220/255, 1/255, size)
			if matrix[i][j] == 5:
				set_pixel(y - j, x - i, 107/255, 107/255, 107/255, size)
			if matrix[i][j] == 6:
				set_pixel(y - j, x - i, 140/255, 137/255, 140/255, size)

def Meteorito(x, y, size):
	matrix = [
		[0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 4, 4, 5, 0, 4, 4, 5, 0, 0, 0, 4, 5, 0, 0, 0],
		[0, 0, 0, 0, 4, 4, 5, 0, 4, 4, 5, 0, 0, 0, 4, 4, 5, 0, 0, 0],
		[0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 0, 0, 0],
		[0, 0, 0, 4, 1, 1, 1, 2, 2, 2, 4, 4, 2, 2, 2, 4, 4, 5, 0, 0],
		[0, 0, 4, 1, 1, 1, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 4, 5, 0, 0],
		[0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 4, 0, 0],
		[0, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 3, 2, 2, 2, 2, 2, 0, 0],
		[0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
		[0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
		[0, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 0],
		[0, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 0],
		[0, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 0],
		[0, 1, 1, 2, 1, 1, 1, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 0],
		[0, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
		[0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 0],
		[0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 2, 2, 2, 0, 0],
		[0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 0, 0, 0],
		[0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
	]

	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == 1:
				set_pixel(y - j, x - i, 90/255, 105/255, 136/255, size)
			if matrix[i][j] == 2:
				set_pixel(y - j, x - i, 139/255, 155/255, 180/255, size)
			if matrix[i][j] == 3:
				set_pixel(y - j, x - i, 192/255, 204/255, 220/255, size)
			if matrix[i][j] == 4:
				set_pixel(y - j, x - i, 254/255, 174/255, 53/255, size)
			if matrix[i][j] == 5:
				set_pixel(y - j, x - i, 247/255, 118/255, 34/255, size)
def Personaje1(x, y, size):
	matrix =   [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 0, 2, 1, 3, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 0, 2, 3, 3, 3, 2, 0, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 0, 2, 3, 3, 3, 2, 0, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 0, 2, 3, 3, 3, 2, 0, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 0, 2, 2, 3, 3, 3, 2, 2, 0, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 1, 1, 1, 1, 1],
				[1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1],
				[1, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1],
				[1, 0, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1],
				[1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1],
				[1, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 1, 1],
				[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 5, 4, 4, 4, 5, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 5, 1, 5, 5, 5, 1, 5, 1, 1, 1, 1, 1, 1, 1]]

	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == 0:
				set_pixel(y - j, x - i, 0/255, 0/255, 0/255, size)
			if matrix[i][j] == 2:
				set_pixel(y - j, x - i, 178/255, 178/255, 178/255, size)
			if matrix[i][j] == 3:
				set_pixel(y - j, x - i, 255/255, 255/255, 255/255, size)
			if matrix[i][j] == 4:
				set_pixel(y - j, x - i, 140/255, 137/255, 140/255, size)
			if matrix[i][j] == 5:
				set_pixel(y - j, x - i, 235/255, 82/255, 0/255, size)

def despintar(x,y,size):
	matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == 1:
				set_pixel(y - j, x - i, 11/255,30/255,48/255, size)
def despintarProyectil(x,y,size):
	matrix =   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			if matrix[i][j] == 0:
				set_pixel(y - j, x - i,11/255,30/255,48/255, size)


def MovePersonaje1(x, y, sx, sy, size,time):
	#clearCanvas()
	despintar(y,-x,size)
	vertices = Traslate([[x, y, 1]], sx, sy)
	x = vertices[0][0]
	y = vertices[0][1]
	Personaje1(y, -x, size)
	#pygame.display.flip()
	pygame.time.wait(time)
	glFlush()
	return x, y

def MoveMeteorito(x, y, sx, sy, size,time):
	#clearCanvas()
	despintar(y,-x,size)
	vertices = Traslate([[x, y, 1]], sx, sy)
	x = vertices[0][0]
	y = vertices[0][1]
	Meteorito(y, -x, size)
	pygame.display.flip()
	glFlush()
	return x, y

def LanzarProyectil(x, y, sx, sy, size):
	despintarProyectil(y,-x,size)
	vertices = Traslate([[x, y, 1]], sx, sy)
	x = vertices[0][0]
	y = vertices[0][1]
	proyectil(y, -x, size)
	pygame.display.flip()
	glFlush()
	return x, y

def ScaledPersonaje1(x, y, sx, sy, size,time):
	#clearCanvas()
	despintar(y,-x,size)
	vertices = Scaled([[x, y, 1]], sx, sy)
	x = vertices[0][0]
	y = vertices[0][1]
	Personaje1(y, -x, size)
	#pygame.display.flip()
	pygame.time.wait(time)
	glFlush()
	return x, y

def RotarDefender(x, y, angle, r, g, b, size):
	#clearCanvas()
	despintar(x,y,size)
	vertices = Rotation([[x, y, 1]], angle)
	x = vertices[0][0]
	y = vertices[0][1]
	Defender(y, -x, r, g, 1, size)
	pygame.display.flip()
	glFlush()
	return x, y
def RotarPersonaje1(x, y, angle, r, g, b, size):
	#clearCanvas()
	despintar(x,y,size)
	vertices = Rotation([[x, y, 1]], angle)
	x = vertices[0][0]
	y = vertices[0][1]
	Personaje1(y, -x, r, g, 1, size)
	pygame.display.flip()
	glFlush()
	return x, y
### Draw
def display_openGL(width, height, scale):
	pygame.display.set_mode((width, height), pygame.OPENGL)

	glClearColor(0.0, 0.0, 0.0, 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	# glScalef(scale, scale, 0)

	gluOrtho2D(-1 * width / 2, width / 2, -1 * height / 2, height / 2)


def MoveDefender2(x, y, sx, sy):
	set_pixel( x, y, 0/255, 0/255, 0/255, 50)

	if( sx == 50 ):
		if( (abs(y)%100 == 50) and ( x < 450) ):
			x = x + sx
	if( sx == -50 ):
		if( (abs(y)%100 == 50) and ( x > -450) ):
			x = x + sx
	if( sy == 50 ):
		if( (abs(x)%100 == 50) and ( y < 250) ):
			y = y + sy
	if( sy == -50 ):
		if( (abs(x)%100 == 50) and ( y > -250) ):
			y = y + sy
	glFlush()
	return x, y