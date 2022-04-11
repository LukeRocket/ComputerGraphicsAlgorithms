from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional      

from utils import cumulative_average


@dataclass
class Vertex:
    coords: List[float]
    color: Optional[List[float]] = None
    id: int = 9999

    def __hash__(self):
        return hash(str(self.id))


@dataclass
class Face:
    vertices_index: List[int]    
    __face_point: Optional[Vertex] = None
    id: int = 9999
    
    def set_face_point(self, vertices: List[Vertex]) -> Vertex:            
        if self.__face_point is None:
            mean_x: float = 0.0
            mean_y: float = 0.0
            mean_z: float = 0.0
            for n, v in enumerate(self.vertices_index):                    
                mean_x = cumulative_average(mean_x, vertices[v].coords[0], n+1)
                mean_y = cumulative_average(mean_y, vertices[v].coords[1], n+1)
                mean_z = cumulative_average(mean_z, vertices[v].coords[2], n+1)        
            self.__face_point = Vertex([mean_x, mean_y, mean_z],  [255, 0, 0], id=self.id)

    def get_face_point(self) -> Vertex:
        if self.__face_point is None:
            raise Exception ("Set Face point")
        return self.__face_point    
        

@dataclass
class Mesh:
    faces: List[Face]    

    def get_faces(self) -> List[Face]:
        return self.faces
    
    def update_mesh(self,
                    vertices: List[Vertex],
                    faces: List[Face]) -> None:        
        self.faces = faces
        self.vertices = vertices        


class Scene:
    def __init__(self, meshes: List[Mesh], vertices: List[Vertex]):
        self.__meshes: List[Mesh] = meshes
        self.__vertices: List[Vertex] = vertices

    def update_scene(self, meshes: List[Mesh], vertices: List[Vertex]) -> None:        
        self.__meshes = meshes
        self.__vertices = vertices

    def get_mesh_by_index(self, index: int) -> Mesh:
        assert index <= len(self.__meshes)-1, 'Index outside scene meshes list'
        return self.__meshes[index]
    
    def get_meshes(self) -> List[Mesh]:
        return self.__meshes

    def get_vertex_from_index(self, index: int) -> Vertex:
        return self.__vertices[index]

    def get_vertices(self) -> List[Vertex]:
        return self.__vertices

    def get_faces_vertices_map(self, mesh_index: Optional[int]= None) -> List[Vertex]:
        vertices_mapping = []        
        if mesh_index is not None:
            meshes = [self.get_mesh_by_index(mesh_index)]
        else:
            meshes = self.get_meshes()

        for mesh in meshes:
            faces = mesh.get_faces()
            for f in faces:
                for index in f.vertices_index:
                    vertices_mapping.append(self.__vertices[index])
        return vertices_mapping
