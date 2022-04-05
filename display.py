from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

import pygame
from pygame.locals import *
import pywavefront 
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from entities import Scene, Vertex


@dataclass
class Displayer:

    def display_vertices(self, vertices: List[Vertex], mode: Enum = GL_POINTS):
        glBegin(mode)
        for v in vertices:            
            glColor(*v.color)
            glVertex3f(*v.coords)
        glEnd()

    def display_scene(self, scene: Scene, mode: Enum = GL_POINTS):
        for mesh in scene.get_meshes():
            glBegin(mode)
            faces = scene.get_mesh_faces(mesh)                                    
            for face in faces:
                for vertex_index in face.vertices_index:
                    glColor(*scene.get_vertex_from_index(vertex_index).color)
                    glVertex3f(*scene.get_vertex_from_index(vertex_index).coords)
        glEnd()
        
    def exit(self):
        pygame.quit()
        quit()

    def translate_scene(self, event):
        # mesh translation        
        if event.key == pygame.K_LEFT:
            glTranslatef(-0.5,0,0)
        if event.key == pygame.K_RIGHT:
            glTranslatef(0.5,0,0)
        if event.key == pygame.K_UP:
            glTranslatef(0,1,0)
        if event.key == pygame.K_DOWN:
            glTranslatef(0,-1,0)

    def zoom(self, event):
        if event.y > 0:
            glTranslatef(0,0,1)
        if event.y < 0:
            glTranslatef(0,0,-1)        

    def view_rotation(self, event, rot_x: float, rot_y: float):
        mouse_buttons = pygame.mouse.get_pressed()
        button_down = mouse_buttons[0] == 1
        if button_down:
            rot_x += event.rel[1]
            rot_y += event.rel[0]
        glRotatef(rot_x, 1, 0, 0)    
        glRotatef(rot_y, 0, 1, 0)  

    def display(self, scene: Optional[Scene] = None, vertices: Optional[List[Vertex]] = None):
        window_w: float = 1280
        window_h: float = 720

        pygame.init()
        pygame.display.set_mode((window_w, window_h), DOUBLEBUF | OPENGL)
        gluPerspective(45, (window_w / window_h), 1, 500.0)
        z_offset: float = 1.0
        glTranslatef(0.0, 0.0, -z_offset) 
        rot_x, rot_y = 0, 0
        while True:
            # get pygame events 
            for event in pygame.event.get():                                                 
                # quit event management
                if event.type == pygame.QUIT: 
                    self.exit()                    
                if event.type == pygame.KEYDOWN:
                    self.translate_scene(event=event)
                if event.type == pygame.MOUSEWHEEL:
                    self.zoom(event=event)
                elif event.type == pygame.MOUSEMOTION:
                    self.view_rotation(event=event, rot_x=rot_x, rot_y=rot_y)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            glPushMatrix()
   
            if scene is not None:
                self.display_scene(scene=scene, mode=GL_TRIANGLES)                
            if vertices is not None:
                self.display_vertices(vertices=vertices, mode=GL_TRIANGLES)                                     
            glPopMatrix()

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            pygame.display.flip()
            pygame.time.wait(10)
