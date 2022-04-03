from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Tuple , Optional      


@dataclass
class Face(ABC):
    vertices_index: List[int]    


@dataclass
class Mesh(ABC):
    faces_list: List[Face]


@dataclass
class Vertex(ABC):
    coords: List[float]
    color: Optional[List[float]] = None


class Scene(ABC):
    vertices: List[Tuple[float]]

    @abstractmethod
    def get_vertex_from_index(self, index: int):
        pass
    
    @abstractmethod
    def get_mesh_faces(self, mesh: Mesh) -> List[List[Tuple[float]]]:
        pass
    
    @abstractmethod     
    def get_meshes(self):
        pass
