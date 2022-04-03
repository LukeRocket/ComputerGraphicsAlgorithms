from dataclasses import dataclass

import pygame
from pygame.locals import *
import pywavefront 
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from entities import Scene

@dataclass
class Displayer:
    #scene: pywavefront.wavefront.Wavefront
    scene: Scene

    def display(self):
        window_w: float = 1280
        window_h: float = 720

        pygame.init()
        pygame.display.set_mode((window_w, window_h), DOUBLEBUF | OPENGL)
        gluPerspective(45, (window_w / window_h), 1, 500.0)
        z_offset: float = 10.0
        glTranslatef(0.0, 0.0, -z_offset) 
        while True:
            # get pygame events 
            for event in pygame.event.get():                     
                
                # quit event management
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    quit()
                    
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            glPushMatrix()
            for mesh in self.scene.get_meshes():
                glBegin(GL_TRIANGLES)
                faces = self.scene.get_mesh_faces(mesh)
                for face in faces:
                    for vertex_index in face:
                        glVertex3f(*self.scene.get_vertex_from_index(vertex_index)[:3])
                glEnd()
            glPopMatrix()

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            pygame.display.flip()
            pygame.time.wait(10)
