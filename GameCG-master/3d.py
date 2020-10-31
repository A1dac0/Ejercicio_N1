#pip install PyOpenGL PyOpenGL_accelerate

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def Cube(vertices, edges, R, G, B, size):
	glColor3f(R, G, B)
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
			# print(vertices[vertex])
	glEnd()

def set_pixel(x, y, z, R, G, B, size):
	glColor3f(R, G, B)
	glPointSize(size)

	glBegin(GL_POINTS)
	glVertex3f(x, y, z)
	glEnd()
	# pygame.display.flip()
	# pygame.time.wait(100)

def main():
	pygame.init()
	display = (800, 800)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

	glTranslatef(0.0, 0.0, -10)
	# glTranslatef(1, 1, 1)

	# Main
	set_pixel(0, 0, 0, 255/255, 255/255, 255/255, 4)

	vertices = (
		(1, 1, 1),
		(1, 1, -1),
		(1, -1, -1),
		(1, -1, 1),
		(-1, 1, 1),
		(-1, -1, -1),
		(-1, -1, 1),
		(-1, 1, -1)
	)
	edges = (
		(0, 1),
		(0, 3),
		(0, 4),
		(1, 2),
		(1, 7),
		(2, 5),
		(2, 3),
		(3, 6),
		(4, 6),
		(4, 7),
		(5, 6),
		(5, 7)
	)
	Cube(vertices, edges, 255/255, 255/255, 0/255, 1)

	pygame.display.flip()
	
	x = 0
	y = 0
	z = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		glRotatef(1, 1, 1, 1)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Cube(vertices, edges, 255/255, 255/255, 0/255, 1)
		pygame.display.flip()
		pygame.time.wait(10)

if __name__ == "__main__":
	main()
opengl_test3D_.py
Mostrando opengl_test3D_.py.