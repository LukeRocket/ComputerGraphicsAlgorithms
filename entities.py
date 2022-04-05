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
    faces_list: List[Face]


class Scene(ABC):
    vertices: List[Vertex]

    @abstractmethod
    def get_vertex_from_index(self, index: int):
        pass
    
    @abstractmethod
    def get_mesh_faces(self, mesh: Mesh) -> List[List[Tuple[float]]]:
        pass
    
    @abstractmethod     
    def get_meshes(self):
        pass
