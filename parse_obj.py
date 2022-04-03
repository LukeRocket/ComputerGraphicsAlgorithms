import os
import pywavefront
from dataclasses import dataclass 
from typing import List, Tuple
from entities import Scene, Mesh

@dataclass
class Parser:
    path: str     

    def __call__(self) -> Scene:        
        scene =  pywavefront.Wavefront(self.path, collect_faces=True)
        return WavefrontScene(scene, scene.vertices)
        

@dataclass
class WavefrontScene(Scene):
    __scene:  pywavefront.wavefront.Wavefront    
    vertices: List[Tuple[int]]

    def get_mesh_faces(self, mesh: Mesh) -> List[List[Tuple[float]]]:
        return mesh.faces

     
    def get_meshes(self):        
        return self.__scene.mesh_list        

    def get_vertex_from_index(self, index: int) -> Tuple[float]:         
        return self.vertices[index]
