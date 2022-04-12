import math
from typing import List

INF_VALUE = 1e10

def cumulative_average(mean: float, sample: float, n: int) -> float:
    mean += (sample - mean) / n
    return mean

def euclidean_distance(pt1: List[float], pt2: List[float]):       
    dist = 0
    for dim in range(len(pt1)):
        dist += (pt1[dim]-pt2[dim])**2
    return math.sqrt(dist)        
    
def normalize_node(node:List[float]) -> List[float]:    
    denom = euclidean_distance(node, [0 for i in range(len(node))])
    return [node[0]/denom, node[1]/denom, node[2]/denom]
