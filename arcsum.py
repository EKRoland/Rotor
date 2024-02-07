from types_definition import *
import networkx as nx
import rotorgraph
import vector
from vector import Vector
from rotorconfig import RotorConfig



class ArcSum(vector.Vector):

    def __init__(self, configuration:dict=None):
        """
        A class to represent sum of arcs.
        It inherits all methods of the class Vector.
        ArcSum contains a dictionnary and act as one, 
        the keys are the edges and the values are the coefficient of arc in the sum
        ArcSum: E -> Z
        Input:
            - configuration:
                - a dictionnary or a vector which will become the ArcSum
                - a RotorConfig, translate the RotorConfig to a ArcSum {edge: 1 for each edge in the values of the RotorConfig}
                - None (default) which gives an empty dict
        """
        if isinstance(configuration, dict) or type(configuration).__name__ == "Vector":
            self.configuration = configuration
        elif type(configuration).__name__ == "RotorConfig":
            self.configuration = {edge: 1 for edge in configuration.configuration.values()}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, a Vector, a RotorConfig or nothing")
        
    ### Find cycle method
    def find_cycle(self)-> ArcSum:
        """
        Finds cycles in a sum of arcs 
        Input:
            - self: sum of arc (edge: int)
        Output:
            - Edges that form a directed cycle with coefficients of 1 and -1, according to the orientation of the cycle
            - None if no cycle detected

        """

        #Creation of a multigraph assiociated to the vector
        G = nx.MultiGraph()
        for edge, count in self.configuration.items():
            if count != 0:
                G.add_edge(edge[0], edge[1])
        #list of cycles
        cycles = list(nx.simple_cycles(G))
        
        #Return None when no cycle detected
        if not cycles:
            return None
        
        #list of edges in the first cycle
        cycle = cycles[0]
        cycle_edges = list([(cycle[i], cycle[i+1]) for i in range(-1,len(cycle)-1)])
        
        

        #give the edges of the vector which form the cycle with thier orientation
        cycle_edges_vector = ArcSum()
        for edge, count in self.configuration.items():
            if (edge[0],edge[1]) in cycle_edges:
                cycle_edges_vector += (edge[0], edge[1], edge[2])
                cycle_edges.remove((edge[0],edge[1]))
            elif (edge[1],edge[0]) in cycle_edges:
                cycle_edges_vector -= (edge[0], edge[1], edge[2])
                cycle_edges.remove((edge[1],edge[0]))
        
        return cycle_edges_vector
    
     ### methode: is a rotor config
    
    
   
    def is_rotorconfig_of(self, rotor_graph: RotorGraph, sinks: set=None) -> RotorConfig:
        """
        Check if the sum of arcs is a rotor configuration of a given graph 
        Input:
            - self: sum of arc (edge: int)
            - rotor_graph: a rotor graph
            - sinks: set of nodes that are considered as sinks
        Output:
            - RotorConfig if the sum is a rotor config of the given grpah
            - None if not
        """
    
        if sinks is None:
            nodes = rotor_graph.nodes - rotor_graph.sinks
        else:
            nodes = rotor_graph.nodes - sinks

        
        present_node = list()
        possible_rotor_config = dict() 
        for edge, count in self.configuration.items():
            if count == 1:
                present_node.append(edge[0])
                possible_rotor_config[edge[0]] = edge
        
        if len(present_node) == len(nodes) and set(nodes) == set(present_node):
            return possible_rotor_config
        else:
            return None
            
    ##### 
    
    def rotoconfig_in_class(self, rotor_graph: RotorGraph) -> RotorConfig:
        """
        Gives the acyclic rotor confuguration of a given graph in the class of a sum of arcs if it exists
        Input:
            - self: sum of arc (edge: int)
            - rotor_graph: a rotor graph
        Output:
            - Acyclic RotorConfig if the the class of the sum of arcs, if it exists
            - None if not
        """

        arcmonic_functions = rotor_graph.arcmonic_functions()
        arcmonic_values = rotor_graph.compute_arcmonic_functions(arcmonic_functions, self)

        list_acyclic_config = [Vector(element) for element in rotor_graph.enum_acyclic_configurations()] 
        acyclic_rc_in_class = None

        
        for acyclic_config in list_acyclic_config:
            if rotor_graph.compute_arcmonic_functions(arcmonic_functions, acyclic_config) == arcmonic_values:
                acyclic_rc_in_class = acyclic_config
                break
        
        return acyclic_rc_in_class



    
        

                
                






  
        
    
