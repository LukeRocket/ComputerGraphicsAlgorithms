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
            if len(vertex) > 4:
                vertices.append(Vertex(coords = vertex[:-3], color=vertex[-3:]))
            elif len(vertex) <= 3:
                vertices.append(Vertex(coords = vertex, color=[255, 255, 255]))
        return WavefrontScene(scene=scene, vertices=vertices)
        

@dataclass
class WavefrontScene(Scene):
    scene:  pywavefront.wavefront.Wavefront    
    vertices: List[Vertex]
    faces: Optional[List[Face]] = None

    def get_mesh_faces(self, mesh: Mesh) -> List[List[Tuple[float]]]:
        if self.faces is None:
            self.faces: List[Face] = []
            for id, f in enumerate(mesh.faces):
                self.faces.append(Face(vertices_index=f, id = id)) 
        return self.faces
    
    def get_meshes(self):      
        return self.scene.mesh_list        

    def get_vertex_from_index(self, index: int) -> Vertex:         
        return self.vertices[index]


def to_obj(file_path: str, vertices: List[Vertex], faces: List[Face]) -> None:
    with open(file_path, 'w') as f:
  
        for i, v in enumerate(vertices):
            c = v.coords
            f.write(f"v {c[0]} {c[1]} {c[2]}\n")
        for face in faces:
            f.write("f")
            for index in face.vertices_index:
                f.write(f" {index}")
            f.write("\n")            