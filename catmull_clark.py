import os
import copy
from typing import List, Tuple, Optional 
from dataclasses import dataclass 
from collections import Counter

from parse_obj import Parser, to_obj
from display import Displayer
from entities import Mesh, Scene, Face, Vertex
from utils import cumulative_average


@dataclass
class CatmullClark:   
    """
        For each face define face point
    """    
    scene: Scene

    def get_edge_point(self, p1_index: int, p2_index: int, near_points: List[List[List[Vertex]]]):
        v1, v2 = self.scene.vertices[p1_index], self.scene.vertices[p2_index]

        x = (v1.coords[0] + v2.coords[0]) / 2 
        y = (v1.coords[1] + v2.coords[1]) / 2
        z = (v1.coords[2] + v2.coords[2]) / 2
    
        mean_x = 0.0
        mean_y = 0.0
        mean_z = 0.0
        coutNears = 0

                        
        face_pts = [k for k,v in Counter(near_points[p1_index][0] + near_points[p2_index][0]).items() if v>1]
        
        for f_point in face_pts:
            coutNears += 1
            mean_x = cumulative_average(mean_x, f_point.coords[0], coutNears)
            mean_y = cumulative_average(mean_y, f_point.coords[1], coutNears)
            mean_z = cumulative_average(mean_z, f_point.coords[2], coutNears)

        return Vertex(coords=[(x+mean_x)/2,(y+mean_y)/2,(z+mean_z)/2], color=[255, 0, 0])

    def get_new_vertex_point(self, near_points: List[List[List[Vertex]]]):
        new_locations = []
        for v in range(len(self.scene.vertices)):                              
            # face point
            mean_x_fp = 0.0
            mean_y_fp = 0.0
            mean_z_fp = 0.0
            # edge midpoints    
            mean_x_em = 0.0
            mean_y_em = 0.0
            mean_z_em = 0.0
            # mean face point
            coutNears = 0
            for f_point in near_points[v][0]:
                coutNears += 1
                mean_x_fp = cumulative_average(mean_x_fp, f_point.coords[0], coutNears)
                mean_y_fp = cumulative_average(mean_y_fp, f_point.coords[1], coutNears)
                mean_z_fp = cumulative_average(mean_z_fp, f_point.coords[2], coutNears)

            # old coords
            c = self.scene.vertices[v].coords
            coutNears = 0
            for f_point in near_points[v][1]:
                coutNears += 1
                mean_x_em = cumulative_average(mean_x_em, (f_point.coords[0] + c[0]) / 2, coutNears)
                mean_y_em = cumulative_average(mean_y_em, (f_point.coords[1] + c[1]) / 2, coutNears)
                mean_z_em = cumulative_average(mean_z_em, (f_point.coords[2] + c[2]) / 2, coutNears)
                    
            n = len(near_points[v][0])
            
            new_locations.append(Vertex(
                coords=[
                    (mean_x_fp + 2*mean_x_em + (n - 3)*c[0]) / n,
                    (mean_y_fp + 2*mean_y_em + (n - 3)*c[1]) / n,
                    (mean_z_fp + 2*mean_z_em + (n - 3)*c[2]) / n
                ], color=[255, 0, 0]
            ))
        return new_locations


    def get_construction_point_list(self, faces: List[Face]) -> List[List[Vertex]]:
        near_face_pts_per_vertex = []
        for v in range(len(self.scene.vertices)):                        
            neighbor_vertex_pts = []
            edge_other_extreme = []
            for f in faces:
                if v in f.vertices_index:                    
                    indices = copy.copy(f.vertices_index)
                    indices.remove(v)
                    for extreme_index in indices:
                        edge_other_extreme.append(self.scene.vertices[extreme_index])

                    neighbor_vertex_pts.append(f.get_face_point())     

            near_face_pts_per_vertex.append([neighbor_vertex_pts, edge_other_extreme])   
        return near_face_pts_per_vertex

    def execute(self, mesh: Mesh):                
   
        faces = self.scene.get_mesh_faces(mesh)
        # set face points        
        for f in faces:
            f.set_face_point(vertices=self.scene.vertices) 

        # get construction points        
        near_face_pts_per_vertex = self.get_construction_point_list(faces=faces)
        
        face_points = [f.get_face_point() for f in faces]        

        final_list = []
        # get new vertex point
        new_verteces_locations = self.get_new_vertex_point(near_face_pts_per_vertex)

        for f in faces:
            # get edge points
            edge_0 = self.get_edge_point(f.vertices_index[0], f.vertices_index[1], near_face_pts_per_vertex)
            edge_1 = self.get_edge_point(f.vertices_index[1], f.vertices_index[2], near_face_pts_per_vertex)
            edge_2 = self.get_edge_point(f.vertices_index[2], f.vertices_index[0], near_face_pts_per_vertex)        

            # get face point
            face_pt = f.get_face_point()

            #collect edges
            final_list.append(face_pt)   
            final_list.append(new_verteces_locations[f.vertices_index[0]])
            final_list.append(edge_0)            

            final_list.append(face_pt)   
            final_list.append(new_verteces_locations[f.vertices_index[1]])
            final_list.append(edge_0)

            final_list.append(face_pt)   
            final_list.append(new_verteces_locations[f.vertices_index[2]])
            final_list.append(edge_2)

            final_list.append(face_pt)   
            final_list.append(new_verteces_locations[f.vertices_index[0]])
            final_list.append(edge_2)
            
            final_list.append(face_pt)   
            final_list.append(new_verteces_locations[f.vertices_index[2]])
            final_list.append(edge_1)

            final_list.append(face_pt)   
            final_list.append(new_verteces_locations[f.vertices_index[1]])
            final_list.append(edge_1)
                                
        return final_list



if __name__ == "__main__":
    #PATH: str = os.path.join('.', 'resources', 'teapot.obj')
    PATH: str = os.path.join('.', 'resources', 'cube.obj')
    #PATH: str = os.path.join('.', 'resources', 'monsterfrog.obj')
    #PATH: str = os.path.join('.', 'resources', 'test.obj')
    OUTPATH: str = os.path.join('.', 'resources', 'test_obj_writer.obj')

    p = Parser(PATH)
    scene = p()    
    c = CatmullClark(scene)
    for mesh in scene.get_meshes():
        vertices = c.execute(mesh)    
    
    d = Displayer()       
    # save as obj 
    to_obj(OUTPATH, vertices=vertices)  
    d.display(vertices=vertices, scene=scene, wireframe=False)       
    