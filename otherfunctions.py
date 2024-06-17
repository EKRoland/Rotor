import networkx as nx
from types_definition import * 
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph
from particleconfig import ParticleConfig
from arcsum import ArcSum
import numpy as np




def rotorconfig_in_class_by_stabilization(rotor_graph:RotorGraph,arc_sum: ArcSum)-> RotorConfig:
    """
    Gives the rotor confuguration of a given graph in the class of a sum of arcs if it exists
    Using the algorithm (r,0)->(\rho, \sigma) and check if we obtain (\rho', 0)
        Input:
            - rotor_graph: a rotor graph
            - arc_sum: sum of arc (edge: int) with deg=1
        Output:
            - RotorConfig in the class of the sum of arcs, if it exists
            - None if not
    """
    #(r,0)->(\rho, \sigma)
    rotor_config, particle_configuartion = arc_sum.arc_per_node(rotor_graph) 
    rotor_config = RotorConfig(rotor_config)
    particle_configuartion, rotor_config, info = rotor_graph.complete_routing(particle_configuartion, rotor_config)
    
    # creation of the particle config (dict: Node -> int)
    null_particle_config = ParticleConfig(rotor_graph)
    if particle_configuartion == null_particle_config:
        return rotor_config
    else:
        return None



def armonic_from_harmonic(rotor_graph:RotorGraph, rotor_config:RotorConfig, 
                          harmonic_functions: list[tuple[int,list[int]]])->tuple[dict[Edge,list[int]],list[int]]:
    """
    Gives the arcmonic values as a vector on the Edges of a rotor_graph
        Input:
            - rotor_graph: a rotor graph
            - rotor_config: initial rotor configuration
            - harmonic_functions: list of tuple[order, harmonic value on the nodes]]
        Output:
            - arcmonic values as a vector on the Edges of the rotor_graph
            - Vector of order
    """
    #check is the given rotor_config is valid for the rotor graph
    rotor_graph.check_rotor_config(rotor_config)

    arcmonic_values = dict()
    orders = []
    # list of order of harmonic and arcmonic functions
    for element in harmonic_functions:
        orders.append(element[0])

    for node in rotor_graph.nodes:
        if node not in rotor_graph.sinks:
            ro_node = rotor_graph.rotor_order[node]
            pos = ro_node.index(rotor_config[node]) 
            new_ro_node = ro_node[pos:] + ro_node[0:pos] #start the rotor order with the edge in rho_0

            #set the arcmonic value at the edges in rho_0 to null vector
            arcmonic_values[new_ro_node[0]] = []
            for element in harmonic_functions:
                arcmonic_values[new_ro_node[0]].append(0)
           

            for i in range(1,len(new_ro_node)):
                arcmonic_values[new_ro_node[i]] = []
                for j in range(len(arcmonic_values[new_ro_node[i-1]])):
                    if orders[j] !=0:
                        arcmonic_values[new_ro_node[i]].append(
                            (arcmonic_values[new_ro_node[i-1]][j] 
                            + harmonic_functions[j][1][ new_ro_node[i-1][1] ] 
                            - harmonic_functions[j][1][ new_ro_node[i-1][0] ]) % orders[j] 
                        )
                    else:
                        arcmonic_values[new_ro_node[i]].append(
                            (arcmonic_values[new_ro_node[i-1]][j] 
                            + harmonic_functions[j][1][ new_ro_node[i-1][1] ] 
                            - harmonic_functions[j][1][ new_ro_node[i-1][0] ])
                        )
    return arcmonic_values, orders



def arcmonic_per_node(arcmonic_per_edges:dict[Edge,list[int]])-> dict[Node,list[np.array]]:
    """
    Gives the arcmonic values on the outgoing arcs of nodes
        Input:
            - arcmonic_per_edges:dict giving the arcmonic vector for every edge
        Output:
            - dict indexed by node giving the arcmonic value of the outgoing arc of this node
    
    """
    arcmonic_per_node = dict()
    for edge in arcmonic_per_edges.keys():
        if edge[0] not in arcmonic_per_node.keys():
            arcmonic_per_node[edge[0]] = []
        arcmonic_per_node[edge[0]].append(np.array(arcmonic_per_edges[edge]))
    
    return arcmonic_per_node
 



def find_circulation(arc_sum: ArcSum)-> list[ArcSum]:
    """
    Finds directed positive cycles in a sum of arcs 
    Input:
        - self: sum of arc (edge: int)
    Output:
        - Edges that form a directed positive cycle
        - None if no cycle detected

    """

    #Creation of a multigraph assiociated to the vector
    G = RotorGraph()
    for edge, count in arc_sum.configuration.items():
        if count > 0:
            G.add_edge(edge[0], edge[1])
        if count < 0:
            G.add_edge(edge[1], edge[0])
    #list of cycles
    cycles_list = list(G.find_directed_cycles())
    
    cycles = [] 
    [cycles.append(x) for x in cycles_list if set(x) not in [set(y) for y in cycles] ]

    #Return None when no cycle detected
    if not cycles:
        print(None)
    
    list_cycle_edges_vector = []
    for cycle in cycles:
        cycle_edges = list([(cycle[i], cycle[i+1]) for i in range(0,len(cycle)-1)])
        
        #give the edges of the vector which form the cycle with thier orientation
        cycle_edges_vector = ArcSum()
        for edge, count in arc_sum.configuration.items():
            
            if ((edge[0],edge[1]) in cycle_edges) and (count >0):
                for _ in range(count):
                    cycle_edges_vector += (edge[0], edge[1], edge[2])
                cycle_edges.remove((edge[0],edge[1]))


        #find the minimum coefficient for the circulation
        list_coef= list(cycle_edges_vector.values())
        for i in range(len(list_coef)):
            list_coef[i] = abs(list_coef[i])
        if list_coef:    
            coef= min(list_coef)

        for edge, count in cycle_edges_vector.configuration.items():
            if count>0:
                cycle_edges_vector[edge] = coef
        
        list_cycle_edges_vector.append(cycle_edges_vector)        

    return list_cycle_edges_vector






####Zone Test
'''
rotor_graph = RotorGraph.simple_path(n=3, x=2, y=2)
rho = RotorConfig(rotor_graph)

sum1= ArcSum({(1, 0, 0):1, (2, 1, 0):1, (3,4,0):1})
rho = RotorConfig(sum1)

harmonic_functions= [(0,[0,1,2,3,4])]

arcmonicfonc,orders= armonic_from_harmonic(rotor_graph, rho, harmonic_functions)

print(arcmonicfonc)

print(arcmonic_per_node(arcmonicfonc))

'''
