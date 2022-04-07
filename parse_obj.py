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
            for id, f in enumerate(mesh.faces):
                self.faces.append(Face(vertices_index=f, id = id)) 
        return self.faces
    
    def get_meshes(self):        
        return self.__scene.mesh_list        

    def get_vertex_from_index(self, index: int) -> Vertex:         
        return self.vertices[index]



def to_obj(file_path: str, vertices: List[Vertex]) -> None:
    with open(file_path, 'w') as f:
        face = []
        for i, v in enumerate(vertices):
            c = v.coords
            f.write(f"v {c[0]} {c[1]} {c[2]}\n")
            face.append(i+1)
            if len(face) == 3:
                f.write(f"f {face[0]} {face[1]} {face[2]}\n")
                face = []    