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
        return WavefrontScene(wf_scene=scene)
        

class WavefrontScene(Scene):
    def __init__(self, 
                 wf_scene:pywavefront.wavefront.Wavefront):  
        self.wf_scene = wf_scene                       
        meshes: List[Mesh] = self.__extract_meshes()
        vertices: List[Vertex] = self.__extract_vertices()
        
        super(WavefrontScene, self).__init__(meshes=meshes, vertices=vertices)
                               
    def __extract_meshes(self) -> List[Mesh]:
        meshes: List[Mesh] = []
        for mesh in self.wf_scene.mesh_list:            
            faces: List[Face] = []
            for id, f in enumerate(mesh.faces):
                faces.append(Face(vertices_index=f, id=id))
            meshes.append(Mesh(faces = faces))
        return meshes
        
    def __extract_vertices(self) -> List[Mesh]:
        vertices: List[Vertex] = []
        for vertex in self.wf_scene.vertices:
            if len(vertex) > 4:
                vertices.append(Vertex(coords = vertex[:-3], color=vertex[-3:]))
            elif len(vertex) <= 3:
                vertices.append(Vertex(coords = vertex, color=[255, 255, 255]))
        return vertices 
       

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