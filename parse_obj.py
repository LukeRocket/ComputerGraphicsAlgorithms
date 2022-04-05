import os
import pywavefront
from dataclasses import dataclass 
from typing import List, Tuple, Optional
from entities import Scene, Mesh, Face, Vertex

@dataclass
class Parser:
    path: str     

    def __call__(self) -> Scene:        
        scene =  pywavefront.Wavefront(self.path, collect_faces=True)
        vertices = []
        for vertex in scene.vertices:
            if len(vertex) == 6:
                vertices.append(Vertex(coords = vertex[:3], color=vertex[3:]))
            elif len(vertex) == 3:
                vertices.append(Vertex(coords = vertex[:3], color=[255, 255, 255]))
        return WavefrontScene(scene, vertices)
        

@dataclass
class WavefrontScene(Scene):
    __scene:  pywavefront.wavefront.Wavefront    
    vertices: List[Vertex]
    faces: Optional[List[Face]] = None

    def get_mesh_faces(self, mesh: Mesh) -> List[List[Tuple[float]]]:
        if self.faces is None:
            self.faces: List[Face] = []
            for f in mesh.faces:
                self.faces.append(Face(vertices_index=f)) 
        return self.faces
    
    def get_meshes(self):        
        return self.__scene.mesh_list        

    def get_vertex_from_index(self, index: int) -> Vertex:         
        return self.vertices[index]
