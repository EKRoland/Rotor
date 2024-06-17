from types_definition import *
import networkx as nx
import vector
from vector import Vector
from rotorconfig import RotorConfig
from particleconfig import ParticleConfig
from arcmonic import Arcmonic
import arcmonic
from rotorgraph import RotorGraph
import rotorgraph



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
            if (edge[0],edge[1]) in cycle_edges and (count !=0):
                cycle_edges_vector += (edge[0], edge[1], edge[2])
                cycle_edges.remove((edge[0],edge[1]))
            elif (edge[1],edge[0]) in cycle_edges and (count !=0):
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
            
    
    
    
    
    def rotoconfig_in_class(self, rotor_graph: RotorGraph) -> RotorConfig:
        """
        Gives the acyclic rotor confuguration of a given graph in the class of a sum of arcs if it exists
        Input:
            - self: sum of arc (edge: int)
            - rotor_graph: a rotor graph
        Output:
            - Acyclic RotorConfig in the class of the sum of arcs, if it exists
            - None if not
        """

        #Compute a list of (order, arcmonic value) of the sum of arcs on the graph
        arcmonic_functions = rotor_graph.arcmonic_functions()
        arcmonic_values = [arcmonic_function.compute_on(self) for arcmonic_function in arcmonic_functions]

        #List of Vector that represent the acyclic configurations of the graph
        list_acyclic_config = [ArcSum(element) for element in rotor_graph.enum_acyclic_configurations()] 
        acyclic_rc_in_class = None

        #Check if an acyclic configuartion give the same list of (order, arcmonic value) as the sum of arcs
        for acyclic_config in list_acyclic_config:
            if [arcmonic_function.compute_on(acyclic_config) for arcmonic_function in arcmonic_functions] == arcmonic_values:
                acyclic_rc_in_class = acyclic_config
                break
        
        return acyclic_rc_in_class
    

    def is_one_edge(self) -> Edge :
        """
        Check if there is only one arc with count 1 in a given sum arc and the other coutn are 0
        Input:
            - self: sum of arc (edge: int)
        Output:
            - Give the edge which only count 1
            - None if not
        """
        number_of_zero = 0
        for edge , count in self.configuration.items():
            if count == 1:
                possible_edge = edge
            elif count == 0:
                number_of_zero +=1
            else:
                return None
        if number_of_zero + 1 == len(self):
            return possible_edge
        else:
            return None
        
    def first_negative_edge(self) -> Edge :
        """
        Gives the first edge which has negative count
        Input:
            - self: sum of arc (edge: int)
        Output:
            - Edges (negative count)
            - None if not
        """
        for edge , count in self.configuration.items():
            if count < 0:
                return edge
        
        return None
    
    
    def arc_per_node(self, rotor_graph: RotorGraph, sinks: set=None) -> tuple[Vector(), ParticleConfig]:
        """
        Gives one positive arc per node and the resulting particule configuration 
        by converting algebraic sum of edges in one edge
        Input:
            - self: sum of arc (edge: int) with deg=1
            - rotor_graph: a rotor graph
        Output:
            - Vector(one arc per node)
            - ParticleConfiguration
        """
        if sinks is None:
            nodes = rotor_graph.nodes - rotor_graph.sinks
        else:
            nodes = rotor_graph.nodes - sinks

        particle_configuartion = ParticleConfig(rotor_graph)
        rotor_config = Vector()

        #Create a dictionnary of sum of egdes per node
        edges_per_nodes = dict()
        for edge,count in self.configuration.items():
            if edge[0] in nodes :
                if edge[0] not in edges_per_nodes.keys():
                    edges_per_nodes[edge[0]]= ArcSum()
                edges_per_nodes[edge[0]] += ArcSum({edge:count})

        for node in edges_per_nodes.keys():
            #while not isinstance( edges_per_nodes[node].is_one_edge(), Edge): 
            edges_on_node = edges_per_nodes[node]
            while not (isinstance(edges_on_node.is_one_edge(),tuple) and len(edges_on_node.is_one_edge()) == 3):
                #When there not exactly one edge with coef 1 at the node
                edge_2 = edges_on_node.first_negative_edge() #Search for the first negative edge
                count_2 = edges_on_node[edge_2]

                edges_on_node += ArcSum({rotor_graph.turn(edge_2):count_2}) - ArcSum({edge_2:count_2})
                particle_configuartion.transfer_particles(edge_2[0],edge_2[1], count_2)
            rotor_config += edges_on_node.is_one_edge()
    
        return rotor_config, particle_configuartion
            

