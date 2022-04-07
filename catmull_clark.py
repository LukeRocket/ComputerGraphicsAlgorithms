import os
import copy
from numpy import reshape, arange
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

    def collect_vertices(self, face_vertices: List[int], 
                            face_pt: Vertex,
                            new_verteces_locations: List[Vertex],
                            near_points: List[List[List[Vertex]]]):
        face_v_list = []

        # get edges
        edges = []                        
        n_vertices = len(face_vertices)
        for i in range(n_vertices):
            edges.append(self.get_edge_point(
                    face_vertices[i],
                    face_vertices[i+1 - n_vertices*((i+1)//n_vertices)],
                    near_points
                ))
            
        for i in range(n_vertices):
            face_v_list.append(face_pt)
            face_v_list.append(edges[i])
            face_v_list.append(new_verteces_locations[face_vertices[i]])
            face_v_list.append(edges[i-1])

        return face_v_list


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
        vertices_coords: List[Vertex] = []
        faces_v_indices: List[Face] = []
        for f_id, f in enumerate(faces):
            edges = []                        
            n_vertices = len(f.vertices_index)
            for i in range(n_vertices):
                edges.append(self.get_edge_point(
                        f.vertices_index[i],
                        f.vertices_index[i+1 - n_vertices*((i+1)//n_vertices)],
                        near_face_pts_per_vertex
                    ))

            vertices_coords.append(f.get_face_point())                                   # +1
            vertices_coords += edges                                                     # +nvertices
            vertices_coords += [new_verteces_locations[k] for k in f.vertices_index]    # +nvertices

            n = len(vertices_coords)

            temp_v_dict = {'face_pt': n-1-2*n_vertices,
                           'edges': list(range(n-2*n_vertices, n-n_vertices)),
                           'new_v': list(range(n-n_vertices, n))}
                                  
            for i in range(n_vertices):                
                face_indices = []
                face_indices.append(temp_v_dict['face_pt'])
                face_indices.append(temp_v_dict['edges'][i])
                face_indices.append(temp_v_dict['new_v'][i])
                face_indices.append(temp_v_dict['edges'][i-1])                 
                faces_v_indices.append(Face(vertices_index=face_indices, id=i+f_id))

            #final_list += self.collect_vertices(f.vertices_index, f.get_face_point(), new_verteces_locations, near_face_pts_per_vertex)          
        return vertices_coords, faces_v_indices


    def update_scene(self, vertices: List[Vertex], faces: List[Face]):        
        self.scene.faces = faces
        self.scene.vertices = vertices        

    def map_faces_vertices(self, vertices, faces):
        vertices_mapping = []
        for f in faces:
            for index in f.vertices_index:
                vertices_mapping.append(vertices[index])
        return vertices_mapping

if __name__ == "__main__":
    #PATH: str = os.path.join('.', 'resources', 'teapot.obj')
    PATH: str = os.path.join('.', 'resources', 'cube.obj')
    #PATH: str = os.path.join('.', 'resources', 'monsterfrog.obj')
    #PATH: str = os.path.join('.', 'resources', 'test.obj')
    OUTPATH: str = os.path.join('.', 'resources', 'test_obj_writer.obj')
    
    p = Parser(PATH)
    scene = p()    
    c = CatmullClark(scene)
    d = Displayer()       
    vertices_mapping = None
    for i in range(2):             
        for mesh in scene.get_meshes():
            vertices, faces = c.execute(mesh)    

        vertices_mapping = c.map_faces_vertices(vertices, faces)
        print(vertices_mapping)
        # save as obj 
        to_obj(OUTPATH, vertices=vertices, faces=faces)  
        PATH = OUTPATH
        c.update_scene(vertices=vertices, faces=faces)   
    d.display(vertices=vertices_mapping, scene=scene, wireframe=True)       
        