import os
from typing import List, Tuple, Optional 
from dataclasses import dataclass 
from parse_obj import Parser
from display import Displayer
from entities import Mesh, Scene, Face, Vertex

def cumulative_average(mean: float, sample: float, n: int) -> float:
    n += 1
    mean += (sample - mean) / n
    return mean

'''@dataclass
class Point:
    x: float
    y: float
    z: float
    x_reprojected: None
    y_reprojected: None
    z_reprojected: None


@dataclass
class Edge:    
    p1: Point
    p2: Point
    mid_point: Point = None
    edge_point: Point = None

    def get_edge_point(self) -> Point:
        if self.edge_point is None:
            f1p = f1.get_face_point()
            f2p = f2.get_face_point()
            if self.mid_point is None:
                self.mid_point = Point( 
                    (p1.x + p2.x)/2, 
                    (p1.y + p2.y)/2,
                    (p1.z + p2.z)/2
                )

            self.edge_point = Point(
                (f1p.x + f2p.x + mid_point.x) / 3
                (f1p.y + f2p.y + mid_point.y) / 3
                (f1p.z + f2p.z + mid_point.z) / 3
            )
        return self.edge_point
        

@dataclass
class Face:
    edges: List[Edge]
    face_point: Point = None

    def get_face_point(self) -> Point:
        
        # get set of points from edges
        points: List[Point] = []
        
        for e in self.edges:
            pointse.p1
        
        mean_x: float = 0.0
        mean_y: float = 0.0
        mean_z: float = 0.0
        if self.face_point is None:
            for i, p in enumerate(points):
                cumulative_average(mean_x, p.x, p)
                cumulative_average(mean_y, p.y, p)
                cumulative_average(mean_z, p.z, p)
                self.face_point = Point(mean_x, mean_y, mean_z)
        return self.face_point

'''
@dataclass
class CatmullClark:   
    """
        For each face define face point
    """    
    scene: Scene
    face_points: Optional[List[Tuple[float]]] = None

    def get_face_point(self, face: Face) -> Tuple[float]:    
        vertices = self.scene.vertices
        mean_x: float = 0.0
        mean_y: float = 0.0
        mean_z: float = 0.0
        for n, vertex_index in enumerate(face):                    
            mean_x = cumulative_average(mean_x, vertices[vertex_index][0], n)
            mean_y = cumulative_average(mean_y, vertices[vertex_index][1], n)
            mean_z = cumulative_average(mean_z, vertices[vertex_index][2], n)        
        '''print(f"mean_x {mean_x}")
        print(f"mean_y {mean_y}")
        print(f"mean_z {mean_z}")'''
        return  Vertex([mean_x, mean_y, mean_z], [255.0, 0.0, 0.0])


    def execute(self, mesh: Mesh):                
        faces = self.scene.get_mesh_faces(mesh)
        if self.face_points is None:
            self.face_points = []
            for f in faces:                        
                self.face_points.append(
                        self.get_face_point(f)
                    )
        
if __name__ == "__main__":
    PATH: str = os.path.join('.', 'resources', 'teapot.obj')
    p = Parser(PATH)
    scene = p()    

    c = CatmullClark(scene)
    for mesh in scene.get_meshes():
        c.execute(mesh)    
        
    d = Displayer()   
    d.display(vertices=c.face_points, scene=scene)   
    