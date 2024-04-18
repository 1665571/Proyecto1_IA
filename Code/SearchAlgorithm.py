# This file contains all the required routines to make an A* search algorithm.
#
__author__ = '1665571'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________


from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list=[]
    for key in map.connections[path.last].keys():
        auxPath=Path(list(path.route))
        auxPath.g=path.g
        auxPath.add_route(key)
        path_list.append(auxPath)
        
    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    noCycleList=[]
    for path in path_list:
        cicle=False
        for valor in path.route:
            if path.route.count(valor) > 1:
                cicle=True
        if not cicle:
            noCycleList.append(path)
    return noCycleList


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    stack=[Path([origin_id])]
    while len(stack)>0 and stack[0].last!=destination_id:
            head=stack[0]
            expanded_paths=expand(head, map)
            expanded_paths=remove_cycles(expanded_paths)
            stack.remove(stack[0])
            stack=insert_depth_first_search(expanded_paths, stack)
        
    if len(stack)>0:
        return stack[0]
    else:
        return []


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    queue=[Path([origin_id])]
    while len(queue)>0 and queue[0].last!=destination_id:
            head=queue[0]
            expanded_paths=expand(head, map)
            expanded_paths=remove_cycles(expanded_paths)
            queue.remove(queue[0])
            queue=insert_breadth_first_search(expanded_paths, queue)
            
    if len(queue)>0:
        return queue[0]
    else:
        return []


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    for path in expand_paths:
        if type_preference == 0:
            path.update_g(1)

        if type_preference == 1: #Minimum time
            path.update_g(map.connections[path.penultimate][path.last])
            
        if type_preference == 2:
            transfer = map.stations[path.penultimate]['name'] == map.stations[path.last]['name']
            if not transfer:
                path.update_g(map.connections[path.penultimate][path.last] * map.stations[path.penultimate]['velocity']) #Tiempo * velocidad = Espacio
          
    
        if type_preference == 3:
            transfer = map.stations[path.penultimate]['name'] == map.stations[path.last]['name']
            if transfer:
                path.update_g(1)    

    return expand_paths

def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    auxList=expand_paths+list_of_path
    auxList=sorted(auxList, key=lambda x:(x.g, len(x.route)))
    return auxList

 

def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pathList=[Path([origin_id])]
    while len(pathList)>0 and pathList[0].last!=destination_id:
            head=pathList[0]
            expanded_paths=expand(head, map)
            expanded_paths=remove_cycles(expanded_paths)
            
            expanded_paths=calculate_cost(expanded_paths, map, type_preference)
            
            pathList.remove(pathList[0])
            pathList=insert_cost(expanded_paths, pathList)
        
    if len(pathList)>0:
        return pathList[0]
    else:
        return []


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    for path in expand_paths:
        if type_preference == 0:
            desti = path.last == destination_id 
            if not desti:
                path.update_h(1)
            else:
                path.update_h(0)
            
        if type_preference == 1:
            desti = path.last == destination_id 
            if not desti:
                #Recogemos las cordenadas de la ultima estacion del Path
                lastCoord=[map.stations[path.last]['x'], map.stations[path.last]['y']] 
                #Recogemos las coordenadas de la estación destino
                destinationCoord=[map.stations[destination_id]['x'], map.stations[destination_id]['y']]
                #Calculamos la distancia euclideana entre las dos estaciones y actualizamos la heurística
                #En este caso dividimos la distancia en linea recta desde la estacion hasta el destino entre la velocidad de la linea
                maxVelocityKey=max(map.velocity, key=map.velocity.get)
                path.update_h(euclidean_dist(lastCoord, destinationCoord) / map.velocity[maxVelocityKey])
            else:
                path.update_h(0)

        if type_preference == 2:
            desti = path.last == destination_id 
            if not desti:
                #Recogemos las cordenadas de la ultima estacion del Path
                lastCoord=[map.stations[path.last]['x'], map.stations[path.last]['y']] 
                #Recogemos las coordenadas de la estación destino
                destinationCoord=[map.stations[destination_id]['x'], map.stations[destination_id]['y']]
                #Calculamos la distancia euclideana entre las dos estaciones y actualizamos la heurística
                path.update_h(euclidean_dist(lastCoord, destinationCoord))
            else:
                path.update_h(0)
                
        if type_preference == 3:
            desti = path.last == destination_id 
            transfer = map.stations[path.penultimate]['name'] == map.stations[path.last]['name'] 
            if not desti and transfer:
                path.update_h(1)
            elif desti:
                path.update_h(0)
    return expand_paths
    

def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    for path in expand_paths:
        if path.last in visited_stations_cost and path.g > visited_stations_cost[path.last]:
                expand_paths.remove(path)
        else:
            visited_stations_cost[path.last]=path.g
    
    for path in list_of_path:
        if path.last in visited_stations_cost and path.g > visited_stations_cost[path.last]:
                list_of_path.remove(path)
        else:
            visited_stations_cost[path.last]=path.g
    
    return expand_paths, list_of_path, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    auxList=expand_paths+list_of_path
    auxList=sorted(auxList, key=lambda x:(x.f, len(x.route)))
    return auxList


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    auxDict={}
    for key, value in map.stations.items(): #Recorremos los elementos del diccionario
        auxCoord=[value['x'],value['y']]
        distance=euclidean_dist(auxCoord, coord) #Calculamos la distance entre el punto en que nos encontramos y el punto donde esta la estacion, redondeado a las centesimas
        auxDict[key]=distance
    
    auxDict=dict(sorted(auxDict.items(), key=lambda x: (x[1],x[0]))) #Ordenamos el diccionario de menor a mayor valor, y en caso de empate de menor a mayor id de estacion
    return auxDict
    pass


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pathList=[Path([origin_id])]
    stationsCost={}
    while pathList and pathList[0].last!=destination_id:
            head=pathList.pop(0)
            expanded_paths=expand(head, map)
            expanded_paths=remove_cycles(expanded_paths)
            
            expanded_paths=calculate_cost(expanded_paths, map, type_preference)
            expanded_paths=calculate_heuristics(expanded_paths, map, destination_id, type_preference)
            expanded_paths=update_f(expanded_paths)
            expanded_paths, pathList, stationsCost=remove_redundant_paths(expanded_paths, pathList, stationsCost)
            
            pathList=insert_cost_f(expanded_paths, pathList)
        
    if pathList:
        return pathList[0]
    else:
        return []



def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    def Astar_improved(origin_coord:list[int], destination_coord:list[int], map:Map) -> Path:
        visited_stations_cost = {}
        results = []

        minimum_dist = euclidean_dist(origin_coord,destination_coord)/5
        more_prox = distance_to_stations(origin_coord,map)

        for i,j in more_prox.items():
            new_list = []
            list_b = [Path(0)]
            list_b[0].add_route(i)
            list_b[0].g = j/5
            while list_b and list_b[0].route[-1] != -1:
                new_list = expand(list_b[0],map)
                new_list = remove_cycles(new_list)
                for path in new_list:
                    time_train = map.connections[path.penultimate][path.last]
                    time_path_1 = euclidean_dist([map.stations[path.penultimate]['x'],map.stations[path.penultimate]['y']],destination_coord)/5
                    time_path_2 = euclidean_dist([map.stations[path.last]['x'],map.stations[path.last]['y']],destination_coord)/5
                    if time_path_2 + time_train > time_path_1:
                        path.update_g(time_path_1)
                        path.route[-1] = -1
                        path.last = path.route[-1]
                    elif time_path_1 > time_train:
                        path.update_g(time_train)   
                    else:
                        path.update_g(time_path_1)
                        path.route[-1] = -1
                        path.last = path.route[-1]

                for path in new_list:
                    if path.last == -1:
                        path.h = 0
                    else:
                        path.h = euclidean_dist([map.stations[path.last]['x'],map.stations[path.last]['y']],destination_coord)/45
                
                new_list = update_f(new_list)
                new_list,list_b,visited_stations_cost = remove_redundant_paths(new_list,list_b,visited_stations_cost)
                list_b = insert_cost_f(new_list,list_b[1:])

            if list_b:
                results.append(list_b[0])
            
        
        path = Path([0,-1])
        path.f = minimum_dist
        for k in results:
            if k.f == minimum_dist:
                if len(k.route) < len(path.route):
                    path = k
                    minimum_dist = k.f
            elif k.f <= minimum_dist:
                minimum_dist = k.f
                path = k

        return path
    
   

