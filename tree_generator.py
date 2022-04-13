"""
    3D Tree generation through space colonization algorithm
    based on 
    http://algorithmicbotany.org/papers/colonization.egwnp2007.large.pdf


    generation of a set of attraction points.
    given the set of points the generation starts 
    from a single point at the base of the tree.


"""
import random
from typing import List, Dict, Union
from dataclasses import dataclass 
from entities import Vertex
from display import Displayer
import utils


@dataclass 
class ColonizationAlgorithm:
    attraction_pts: List[Vertex]
    tree_nodes: List[Vertex]
    attr_radius: float
    kill_distance: float     

    def filter_points(self) -> Dict[int,  Dict[str, Union[List[Vertex], List[float]]]]:
        # TODO: optimize this!!

        dists_list: List[Dict[int, float]] = []
        for tree_n in self.tree_nodes:
            node_dict: Dict[int, float] = {}
            for attr_p in self.attraction_pts:
                distance = utils.euclidean_distance(tree_n.coords, attr_p.coords)
                if distance <= self.attr_radius:
                    node_dict[attr_p.id] = distance
            dists_list.append(node_dict)

        # associate pts
        vert_relations: Dict[int, Dict[str, Union[List[Vertex], List[float]]]] = {}
        killed_nodes = []
        for attr_p in self.attraction_pts:
            min_dist = utils.INF_VALUE
            min_key: int = 0
            for loop_index, k in enumerate(dists_list):    
                if attr_p.id in k.keys():
                    new_dist = k[attr_p.id]                            
                    if new_dist < min_dist:
                        min_dist =  new_dist
                        min_key = loop_index   
            
            if min_dist <= self.kill_distance:
                killed_nodes.append(attr_p)
                break # do not include this attraction point anymore 

            if min_dist != utils.INF_VALUE:
                if min_key in vert_relations.keys():
                    vert_relations[min_key]['attr_pts'].append(attr_p)
                    vert_relations[min_key]['dists'].append(min_dist)
                else:
                    vert_relations[min_key] = {'attr_pts': [attr_p], 'dists': [min_dist]}                    
        
        # remove killed attraction pts 
        self.attraction_pts = [pt for pt in self.attraction_pts if pt not in killed_nodes]

        return vert_relations

    def calculate_branch_direction(self, tree_node: Vertex, vertices: Dict[str, Union[List[Vertex], List[float]]], color:List[float]):
        dir_node = Vertex(coords=[0, 0, 0], color=color)        
        for v in range(len(vertices['attr_pts'])):                    
            dir_node.coords[0] += (vertices['attr_pts'][v].coords[0] - tree_node.coords[0]) / vertices['dists'][v]
            dir_node.coords[1] += (vertices['attr_pts'][v].coords[1] - tree_node.coords[1]) / vertices['dists'][v]
            dir_node.coords[2] += (vertices['attr_pts'][v].coords[2] - tree_node.coords[2]) / vertices['dists'][v]        
        dir_node.coords = utils.normalize_node(dir_node.coords)        
        D = 0.1
        dir_node.coords[0] = tree_node.coords[0] + D*dir_node.coords[0]
        dir_node.coords[1] = tree_node.coords[1] + D*dir_node.coords[1]
        dir_node.coords[2] = tree_node.coords[2] + D*dir_node.coords[2]
        return dir_node

    def get_new_tree_nodes(self, relations_dict: Dict[int, Dict[str, Union[List[Vertex], List[float]]]], color:List[float]) -> List[Vertex]:                     
        new_tree_nodes: List[Vertex] = []  
        for k in relations_dict.keys():
            if len(relations_dict[k]['attr_pts']) > 0:
                new_tree_nodes.append(self.calculate_branch_direction(tree_node=self.tree_nodes[k], vertices=relations_dict[k], color=color))
        return new_tree_nodes


@dataclass
class AttractionPtsGenerator:
    n_points: int
    expasion_magnitudes: List[float]
    root_position: List[float]

    def generate(self) -> List[Vertex]:        
        vertices = []
        for i in range(self.n_points):
            coords = [
                random.choice([-1,1])*(self.root_position[0] + random.random()*self.expasion_magnitudes[0]), 
                self.root_position[1] + random.random()*self.expasion_magnitudes[1], 
                random.choice([-1,1])*(self.root_position[2] + random.random()*self.expasion_magnitudes[2]) 
            ]            
            vertices.append(Vertex(coords=coords, color=[255, 255, 255], id=i+1))
        return vertices

if __name__ == '__main__':
    # create tree trunk 
    root_node = Vertex(coords=[0, 0, 0], color=[0, 255, 0], id=0)
    ap_g = AttractionPtsGenerator(n_points = 100, expasion_magnitudes=[.5, 5.0, .5], root_position=root_node.coords)    
    a_pts = ap_g.generate()
    
    tree_nodes = [root_node]    
    c = ColonizationAlgorithm(attraction_pts=a_pts, tree_nodes=tree_nodes, attr_radius=3, kill_distance=0.5)    
    for i in range(50):        
        c.tree_nodes += c.get_new_tree_nodes(relations_dict=c.filter_points(), color=[255, 0, 0])

    # create branches
    ap_g = AttractionPtsGenerator(n_points = 200, expasion_magnitudes=[5.0, 8.0, 5.0], root_position=c.tree_nodes[-len(c.tree_nodes)//2].coords)    
    a_pts = ap_g.generate()
    c.attraction_pts = a_pts
    for i in range(300):        
            c.tree_nodes += c.get_new_tree_nodes(relations_dict=c.filter_points(), color=[0, 255, 0])


    d = Displayer()    
    d.display(vertices=tree_nodes)
