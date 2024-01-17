import networkx as nx
from types_definition import * 
from unionfind import UnionFind
from copy import deepcopy
import rotorconfig
import particleconfig
from random import randint
from results import Results
import matrices

class RotorGraph(nx.MultiDiGraph):

    def __init__(self, incoming_graph_data=None, multigraph_input=None, **attr):
        """
        A class which represent a Multi Directed Rotor Graph.
        Inherit all methods from MultiDiGraph of the networkx module
        """
        self._sinks = set() # active sinks (setted manually)
        self.sinks = set() # all sinks (manually and automatically)
        self.rotor_order = dict() # {node: list[edge]}
        self.edge_index = dict() # {edge: index in the rotor order list}
        nx.MultiDiGraph.__init__(self, incoming_graph_data, multigraph_input, **attr)


    def simple_path(n:int=5, x:int=1, y:int=1) -> RotorGraph:
        """
        Create a simple path rotor graph with n nodes and two sinks at the extremities (so n+2 nodes in total)
        Input:
            - n: the number of nodes in the graph (default : five nodes)
            - x: number of left edges (default=1)
            - y: number of right edges (default=1)
        Output:
            - a simple path rotor graph
        """
        graph = RotorGraph()
        for i in range(n+2): graph.add_node(i)
        for i in range(1, n+1):
            for _ in range(y):
                graph.add_edge(i, i+1)
            for _ in range(x):
                graph.add_edge(i, i-1)
        graph.set_sink(0, n+1)

        return graph


    def grid(n: int=3, m: int=3, sinks: str="") -> RotorGraph:
        """
        Create a grid rotor graph n*m nodes
        Input:
            - n: number of rows 
            - m: number of columns
            - sinks: a string describing where the sinks should be (optional, default is no sinks)
                borders, corners or center
        Output:
            - a grid rotor graph
        """
        graph = RotorGraph()
        total_nodes = n*m
        for i in range(total_nodes): graph.add_node(i)
        for i in range(n):
            for j in range(m):
                node = i*m + j
                if (node-m) in range(total_nodes): graph.add_edge(node, node-m)
                if (j+1) in range(m): graph.add_edge(node, node+1)
                if (node+m) in range(total_nodes): graph.add_edge(node, node+m)
                if (j-1) in range(m): graph.add_edge(node, node-1)

        sinks = sinks.lower()
        if sinks in {"border", "borders"}:
            for i in range(n):
                graph.set_sink(i*n, i*n + m-1 )  # graph.set_sink()
            for i in range(m):
                graph.set_sink(i, (n-1)*m+i) #graph.set_sink(i, i*m, i*m + m-1, (n-1)*m+i)
        elif sinks in {"corner", "corners"}:
            graph.set_sink(0, m-1, m*(n-1), m*n-1) #graph.set_sink(0, m-1, n*m, m*(n-1), m*n-1)
        elif sinks in {"center"}:
            graph.set_sink((n*m) // 2)

        return graph
    
    def random_graph(min_nb_nodes:int=5, max_nb_nodes:int=15) -> RotorGraph:
        """
        Create a random connected rotor graph with a random number of sinks.
        Input:
            - min_nb_nodes: the minimum number of nodes
            - max_nb_nodes : the maximum number of nodes
        Output:
            - the rotor graph
        """
        G = RotorGraph()
        nb_nodes = randint(min_nb_nodes, max_nb_nodes)
        for i in range(nb_nodes):
            G.add_edge(i, i+1)
            #G.add_edge(i+1, i)

        for _ in range(randint(nb_nodes//2, 2*nb_nodes+1)):
            u = randint(0, nb_nodes)
            v = randint(0, nb_nodes+1)
            G.add_edge(u, v)

        
        G.add_edge(nb_nodes, nb_nodes+1)
        G.set_sink(nb_nodes+1)
        for i in range(3):
            G.set_sink(randint(0, nb_nodes))
        

        return G


    def add_edge(self, u_for_edge: Node, v_for_edge: Node, key=None, **attr) -> object:
        """
        Add an edge to the graph with MultiDiGraph method and update the rotor order
        Input:
            - u_for_edge: tail node
            - v_for_edge: head node
            - key: identifier (default=lowest unused integer)
            - attr: keyword arguments, optional
        Output:
            The edge key assigned to the edge.
        """
        key = nx.MultiDiGraph.add_edge(self, u_for_edge, v_for_edge, key=None, **attr)
        edge = (u_for_edge, v_for_edge, key)
        if u_for_edge in self.rotor_order.keys():
            self.rotor_order[u_for_edge].append(edge)
            self.edge_index[edge] = len(self.rotor_order[u_for_edge]) - 1
        else:
            if u_for_edge not in self._sinks and u_for_edge in self.sinks:
                self.sinks.remove(u_for_edge)
            self.rotor_order[u_for_edge] = [edge]
            self.edge_index[edge] = 0
        return key

    def remove_edge(self, *edges: Edge) -> object:
        """
        Remove an edge to the graph with MultiDiGraph method and update the rotor order
        Input:
            - edges: multiple Edge to remove
        No output
        """
        for edge in edges:
            nx.MultiDiGraph.remove_edge(self, edge[0], edge[1], edge[2])
            self.rotor_order[edge[0]].remove(edge)
            del self.edge_index[edge]
            if len(self.rotor_order[edge[0]]) == 0:
                self.sinks.add(edge[0])


    def set_sink(self, *nodes: Node):
        """
        Set the given nodes as a sink
        Input:
            - nodes: multiple Node to set as sink
        No output
        """
        self.sinks.update(nodes)
        self._sinks.update(nodes)

    def remove_sink(self, *nodes: Node):
        """
        Unset the given nodes as a sink
        Input:
            - nodes: multiple Node to unset
        No output
        """
        for node in nodes:
            if len(self.rotor_order[node]) == 0:
                self.sinks.remove(node)
        self._sinks -= set(nodes)



    def head(self, edge: Edge) -> Node:
        """
        Return the head's value of an edge if it exist
        else return None
        Input:
            - edge: tuple identifying an edge
        Output:
            - head's value of the edge
        """
        if edge in self.edges:
            return edge[1]
        else: return None


    def tail(self, edge: Edge) -> Node:
        """
        Return the tail's value of an edge if it exist
        else return None
        Input:
            - edge: tuple identifying an edge
        Output:
            - tail's value of the edge
        """
        if edge in self.edges:
            return edge[0]
        else: return None


    def set_rotor_order(self, new_order: dict[Node, list[Edge]]):
        """
        Define the rotor order to consider.
        The new order will override the old one of the given nodes.
        Each node needs all its outgoing edges.
        Input:
            - new_order: dict of the form {node: [edges]}
        No output
        """
        for node, edges in new_order.items():
            if node not in self.nodes:
                raise KeyError(f"Invalid node '{node}'")

            for edge in edges:
                if edge not in self.edges:
                    raise ValueError(f"Invalid edge {edge}")
                
                if node != self.tail(edge):
                    raise ValueError(f"The node '{node}' does not correspond to the tail of the edge {edge}")
            
            if self.out_degree(node) != len(set(edges)):
                raise ValueError(f"Not all edges of the node '{node}' are given")

        self.rotor_order.update(new_order)
        self.edge_index = rotor_order2edge_index(self.rotor_order)

    def invert_rotor_order(self):
        """
        Invert the rotor order of the graph.
        No input
        No output
        """
        for node in self.rotor_order:
            self.rotor_order[node].reverse()
        self.edge_index = rotor_order2edge_index(self.rotor_order)


    def check_rotor_config(self, rotor_config: RotorConfig):
        """
        Check if the given rotor configuration is valid for the RotorGraph
        Input:
            - rotor_config: Dict containg the rotor configuration to check
        No output but raises en error if the configuration is not valid.
        """
        for node, edge in rotor_config.configuration.items():
            if node not in self.nodes:
                raise KeyError(f"Invalid node '{node}'")

            if edge not in self.edges:
                raise ValueError(f"Invalid edge {edge}")
                
            if node != self.tail(edge):
                raise ValueError(f"The node '{node}' does not correspond to the tail of the edge {edge}")


    def turn(self, edge: Edge, k: int=1) -> Edge:
        """
        Give the next edge of the given edge in rotor order
        Input:
            - edge: Edge to turn k times
            - k: number of times to turn (default: one time)
        Output:
            - Resulting Edge after the turn
        """
        if edge not in self.edges:
            raise ValueError(f"Invalid edge {edge}")

        order = self.rotor_order[edge[0]]
        n = len(order)
        if (n == 1) or (k%n == 0):
            return edge
        
        current_idx = self.edge_index[edge]
        next_idx = (current_idx + k) % n
        
        return order[next_idx]

    def turn_all(self, rotor_config: RotorConfig, k: int=1, sinks: set=None) -> RotorConfig:
        """
        Turn all edges of the configuration
        Input:
            - rotor_config: the rotor configuration to turn
            - k: number of times to turn (default: one time)
        Output:
            - new resulting Config after the turn
        """
        if sinks == None:
            if self.sinks:
                sinks = self.sinks

        res_config = deepcopy(rotor_config)
        for node in rotor_config.configuration.keys():
            res_config.configuration[node] = self.turn(rotor_config.configuration[node], k=k)

        return res_config

    
    def reverse_turn(self, edge: Edge, k: int=1) -> Edge:
        """
        Give the previous edge of the given edge in rotor order
        Input:
            - edge: Edge to turn k times
            - k: number of times to turn (default: one time)
        Output:
            - resulting Edge after the turn
        """
        if edge not in self.edges:
            raise ValueError(f"Invalid edge {edge}")

        order = self.rotor_order[edge[0]]
        n = len(order)
        if (n == 1) or (k%n == 0):
            return edge
        
        current_idx = self.edge_index[edge]
        previous_idx = (current_idx - k) % n
        
        return order[previous_idx]

    def reverse_turn_all(self, rotor_config: RotorConfig, k: int=1, sinks: set=None) -> RotorConfig:
        """
        Turn all edges of the configuration in the reverse order 
        Input:
            - rotor_config: the rotor configuration to turn
            - k: number of times to turn (default: one time)
        Output:
            - new resulting Config after the turn
        """
        if sinks == None:
            if self.sinks:
                sinks = self.sinks

        res_config = deepcopy(rotor_config)
        for node in rotor_config.configuration.keys():
            res_config.configuration[node] = self.reverse_turn(rotor_config.configuration[node], k=k)

        return res_config
            

    def step(self, particle_config: object, rotor_config: RotorConfig, node: Node=None, sinks: set=None,
             turn_and_move: bool=False, info=None) -> (ParticleConfig, RotorConfig):
        """
        Make one step of routing
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - node: the node where to make a step (default: the first non sink node with a particle)
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then move
            - info: Results to update (optional)
        Output:
            - new particle configuration
            - new rotor configuration
        """
        particle_config = deepcopy(particle_config)
        rotor_config = deepcopy(rotor_config)

        # retrieve sinks
        if sinks == None: sinks = self.sinks
 
        # get node
        if node == None:
            # try to find the fist non sink node with a particle
            node = particle_config.first_node_with_particle(sinks)

            # if no node given or found: nothing changes
            if node == None: return particle_config, rotor_config

        if turn_and_move:
            # turn
            rotor_config.configuration[node] = self.turn(edge)

            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(node, succ)

        else: # move and turn
            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(node, succ)

            # turn
            rotor_config.configuration[node] = self.turn(edge)

        if info != None:
            info.edges_counter[edge] += 1
            info.nodes_counter[succ] += 1
            info.last_visit[node] = info.nb_steps
            info.nb_steps += 1
            info.last_visit[succ] = info.nb_steps
            info.configuration_history.append((rotor_config, particle_config))
            
        return particle_config, rotor_config

    def reverse_step(self, particle_config: object, rotor_config: RotorConfig, node:Node=None, sinks: set=None,
             turn_and_move: bool=False, info=None) -> (ParticleConfig, RotorConfig):
        """
        Make one step of routing in reverse
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - node: the node where to make a reverse step (default: the first non sink node with a particle)
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then move
            - info: Results to update (optional)
        Output:
            - new particle configuration
            - new rotor configuration
        """
        particle_config = deepcopy(particle_config)
        rotor_config = deepcopy(rotor_config)

        # retrieve sinks
        if sinks == None: sinks = self.sinks
 
        # get node
        if node == None:
            # try to find the fist non sink node with a particle
            node = particle_config.first_node_with_antiparticle(sinks)

            # if no node given or found: nothing changes
            if node == None: return particle_config, rotor_config

        if turn_and_move:
            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(succ, node)

            # turn
            rotor_config.configuration[node] = self.turn(edge)

        else: # move and turn
            # turn
            edge = rotor_config.configuration[node]
            edge = self.turn(edge)
            rotor_config.configuration[node] = edge

            # move
            succ = self.head(edge)
            particle_config.transfer_particles(succ, node)

        if info != None:
            info.edges_counter[edge] += 1
            info.nodes_counter[succ] += 1
            info.last_visit[node] = info.nb_steps
            info.nb_steps += 1
            info.last_visit[succ] = info.nb_steps
            info.configuration_history.append((rotor_config, particle_config))
        return particle_config, rotor_config

    def legal_routing(self, particle_config: object, rotor_config: RotorConfig, sinks: set=None,
                      turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
        """
        Route particles to the sinks
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then turn
        Output:
            - new particle configuration
            - new rotor configuration
        """

        if sinks is None and len(self.sinks) == 0:
            print("Infinite loop")
            return

        if sinks == None:
            sinks = self.sinks

        
        info = Results(self, particle_config, rotor_config)
        while (node := particle_config.first_node_with_particle(sinks)) != None:
            particle_config, rotor_config = self.step(particle_config, rotor_config, node, sinks,
                                                      turn_and_move, info)
        info.orientation_edges(rotor_config)
        info.particles_in_sinks(particle_config)

        return particle_config, rotor_config, info



    def route_one_particle(self, node: Node, rotor_config: RotorConfig, sinks: set=None,
                           turn_and_move: bool=False) -> RotorConfig:
        """
        Route one particule from the given node to a sink.
        Input:
            - node: the node where the routed particle starts
            - rotor_config: the rotor configuration of the graph
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False)
                if True: turn first then move
                else (False): move first then turn
        Output:
            - new rotor configuration
        """
        sigma = particleconfig.ParticleConfig(self) + node
        particle_config, rotor_config, info = self.legal_routing(sigma, rotor_config, sinks, turn_and_move)
        return rotor_config, info


    def complete_routing(self, particle_config: ParticleConfig, rotor_config: RotorConfig, sinks: set=None,
                      turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
        """
        Route particles and antiparticles to the sinks
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then turn
        Output:
            - new particle configuration
            - new rotor configuration
        """

        if sinks is None and len(self.sinks) == 0:
            print("Infinite loop")
            return

        if sinks == None:
            sinks = self.sinks

        
        info = Results(self, particle_config, rotor_config)
        while (node := particle_config.first_node_with_particle(sinks)) != None:
            particle_config, rotor_config = self.step(particle_config, rotor_config, node, sinks, turn_and_move, info)
        while (node := particle_config.first_node_with_antiparticle(sinks)) != None:
            particle_config, rotor_config = self.reverse_step(particle_config, rotor_config, node, sinks, turn_and_move, info)

        info.orientation_edges(rotor_config)
        info.particles_in_sinks(particle_config)

        return particle_config, rotor_config, info

    def laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]:
        """
        Create the laplacian matrix of the graph
        Input:
            - sinks: set of nodes that are considered as sinks (optional)
        Output : 
            - the laplacian matrix of the graph (dict of dict)
        """
        if sinks is None:
            non_sink_nodes = self.nodes - self.sinks
        else:
            non_sink_nodes = self.nodes - sinks

        matrix = dict()
        for u in self.nodes:
            if u in non_sink_nodes:
                matrix[u] = dict()
                for v in self.nodes:
                    if u == v:
                        matrix[u][v] = self.out_degree(u) - self.number_of_edges(u, v)
                    else:
                        matrix[u][v] = -self.number_of_edges(u, v)
            else:
                matrix[u] = {v: 0 for v in self.nodes}

        return matrices.Matrix(matrix)

    def reduced_laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]:
        """
        Create the reduced laplacian matrix of the graph
        Input:
            - sinks: set of nodes that are considered as sinks (optional)
        Output : 
            - the reduced laplacian matrix of the graph (dict of dict)
        """
        if sinks is None:
            nodes = self.nodes - self.sinks
        else:
            nodes = self.nodes - sinks

        matrix = dict()
        for u in nodes:
            matrix[u] = dict()
            for v in nodes:
                if u == v:
                    matrix[u][v] = self.out_degree(u) - self.number_of_edges(u, v)
                else:
                    matrix[u][v] = -self.number_of_edges(u, v)

        return matrices.Matrix(matrix)



    def vector_routing(self, particle_config: object, rotor_config: RotorConfig, vector:
                       dict[Node:int], sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
        """
        Route the graph according to a given vector optimized with the laplacian matrix
        Input:
            - particle_config : the particle configuration of the graph
            - rotor_config : the rotor configuration of the graph
            - vector : dict[Node:int]
            - sinks : set of nodes that are considered as sinks
            - turn_and_move : boolean (default=False)
                if True: turn first then move
                else (False): move first then turn
        Output:
            - the new particle configuration
            - the new rotor configuration
        """
        matrix = self.laplacian_matrix(sinks)
        for u, k in vector.items():
            if u not in matrix: continue

            c = k // matrix[u][u]

            for v, p in matrix[u].items():
                particle_config.configuration[v] -= c*p

            for _ in range(k % matrix[u][u]):
                self.step(particle_config, rotor_config, node=u, sinks=sinks, turn_and_move=turn_and_move)

        return particle_config, rotor_config

    def enum_configurations(self, sinks:set=None) -> list[RotorConfig]: 
        """
        Gives a list of all the rotor configuration of the graph
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - list of configurations (set of edges)
        """
        if sinks == None:
            if self.sinks:
                sinks = self.sinks
            #else: raise Exception("No sink in the graph: cannot find an acyclic configuration.") 

        nodes = [node for node in self.rotor_order.keys() if node not in sinks]
        i = 0 # index of the node where to chose the next edge
        # config_list = list() # resulting list
        rotor_configuration = [0 for _ in range(len(nodes))] # take first edges of all nodes

        while rotor_configuration[0] < self.out_degree(nodes[0]):
            if i == len(nodes)-1: # last node
                if rotor_configuration[i] < self.out_degree(nodes[i]): # not his last edge
                    dic = {nodes[i]: self.rotor_order[nodes[i]][rotor_configuration[i]] for i in range(len(nodes))}
                    rc = rotorconfig.RotorConfig(dic)
                    # config_list.append(rc)
                    yield rc
                    rotor_configuration[i] += 1
                else:
                    rotor_configuration[i] = 0
                    i -= 1
                    rotor_configuration[i] += 1

            else:
                if rotor_configuration[i] < self.out_degree(nodes[i]):
                    i += 1
                else:
                    rotor_configuration[i] = 0
                    i -= 1
                    rotor_configuration[i] += 1
        # return config_list         


    def enum_acyclic_configurations(self, sinks:set=None) -> list[RotorConfig]:
        """
        Gives a list of all the acyclic rotor configuration of the graph where each represents a
        class
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - list of acyclic configurations (set of edges)
        """
        if sinks == None:
            if self.sinks:
                sinks = self.sinks
            else:
                raise Exception("No sink in the graph: cannot find an acyclic configuration.")

        nodes = [node for node in self.rotor_order.keys() if node not in sinks]
        i = 0 # index of the node where to chose the next edge
        acyclic_config = list() # resulting list
        rotor_configuration = [0 for _ in range(len(nodes))] # take first edges of all nodes
        uf_list = [None for _ in range(len(nodes))] # set unionfind list
        uf_list[0] = UnionFind(list(self.nodes)) # create the first unionfind

        while rotor_configuration[0] < self.out_degree(nodes[0]):
            if i == len(nodes)-1: # last node
                if rotor_configuration[i] < self.out_degree(nodes[i]): # not his last edge
                    # check if adding the edge will not create a cycle
                    edge = self.rotor_order[nodes[i]][rotor_configuration[i]]
                    if not uf_list[i].connected(edge[0], edge[1]):
                        dic = {nodes[i]: self.rotor_order[nodes[i]][rotor_configuration[i]] for i in range(len(nodes))}
                        rc = rotorconfig.RotorConfig(dic)
                        acyclic_config.append(rc)
                    rotor_configuration[i] += 1
                else:
                    rotor_configuration[i] = 0
                    i -= 1
                    rotor_configuration[i] += 1

            else:
                if rotor_configuration[i] < self.out_degree(nodes[i]):
                    edge = self.rotor_order[nodes[i]][rotor_configuration[i]]
                    if not uf_list[i].connected(edge[0], edge[1]):
                        uf_list[i+1] = deepcopy(uf_list[i])
                        uf_list[i+1].union(edge[0], edge[1])
                        i += 1
                    else:
                        rotor_configuration[i] += 1
                else:
                    rotor_configuration[i] = 0
                    i -= 1
                    rotor_configuration[i] += 1
        return acyclic_config


    def recurrent_from_acyclic(self, list_acyclic:list[RotorConfig]) -> list[RotorConfig]:
    #list[tuple[RotorConfig, RotorConfig]]:
        """
        For all acyclic configuration, gives the corresponding recurrent configuration in the class
        Input:
            - list_acyclic: the list of all acyclic configuration of the graph
        Output:
            - list of recurrent configuration
        """  
        rec = list()
        for config in list_acyclic:
            rec.append(self.turn_all(config))

        return rec

    def recurrent_and_acyclic(self, list_acyclic:list[RotorConfig]) -> list[tuple[RotorConfig, RotorConfig]]:
        """
        For all acyclic configuration, gives the corresponding recurrent configuration in the class
        Input:
            - list_acyclic: the list of all acyclic configuration of the graph
        Output:
            - list of tuples (recurrent configuration, acyclic configuration)
        """
        rec_acyclic = list()
        for config in list_acyclic:
            rec = self.turn_all(config)
            acy = deepcopy(rec)
            acy.destination_forest(self)
            rec_acyclic.append((rec, acy))

        return rec_acyclic


def all_config_from_recurrent(rotor_graph: RotorGraph, rotor_config: RotorConfig, sinks:set=None,
                              set_config: set[RotorConfig]=None) -> set[RotorConfig]:
    """
    Gives all the configuration in the class of the given recurrent configuration
    Input:
        - rotor_graph: the RotorGraph of the recurrent configuration
        - rotor_config: the recurrent RotorConfig of the class
        - sinks: a set of Node to consider as sink
        - set_config: the set where to store the RotorConfig
    Output:
        - set of all the RotorConfig of the class
    """
    if set_config is None:
        set_config = [rotor_config]
        if sinks == None:
            if rotor_graph.sinks:
                sinks = rotor_graph.sinks

    if cycles := rotor_config.find_cycles(sinks):
        for cycle in cycles:
            next_config = deepcopy(rotor_config)
            next_config.cycle_push(rotor_graph, cycle)
            if next_config not in set_config:
                set_config.append(next_config)
            all_config_from_recurrent(rotor_graph, next_config, sinks, set_config)
    return set_config



def display_path(rotor_config: RotorConfig, particle_config: ParticleConfig=None):
    """
    Give a graphical representation in the terminal of a simple path graph configuration.
    Examples,
    if no ParticleConfig given:
        x<- x<- x - x
    if ParticleConfig given:
        3 - 5<->2 - 0
    Input:
        - rotor_config: the rotor configuration of the graph
        - particle_config: the particule configuration of the graph (optional)
    No output
    """
    if particle_config is None:
        n = len(rotor_config.configuration) + 2
        particle_config = particleconfig.ParticleConfig({i:"x" for i in range(n)})

    for i in range(len(particle_config.configuration)-1):
        print(particle_config.configuration[i],end='')
        if (i+1, i, 0) in rotor_config.configuration.values():
            print('<',end='')
        else: print(' ',end='')
        print('-',end='')
        if (i, i+1, 0) in rotor_config.configuration.values():
            print('>',end='')
        else: print(' ',end='')
    print(particle_config.configuration[len(particle_config.configuration)-1])


def display_grid(rotor_config: RotorConfig, n, m, particle_config: ParticleConfig=None):
    """
    Give a graphical representation in the terminal of a simple grid graph configuration.
    Input:
        - particle_config: the particule configuration of the graph
        - rotor_config: the rotor configuration of the graph
    No output
    """
    if particle_config == None:
        particle_config = particleconfig.ParticleConfig({i:"x" for i in range(n*m)})

    for j in range(n):
        for i in range(j*m, j*m+m-1):
            print(particle_config.configuration[i],end='')
            if (i+1, i, 0) in rotor_config.configuration.values():
                print('<',end='')
            else: print(' ',end='')
            print('-',end='')
            if (i, i+1, 0) in rotor_config.configuration.values():
                print('>',end='')
            else: print(' ',end='')
        print(particle_config.configuration[j*m+m-1], end='')
        print()
        if j < n-1:
            for i in range(j*m, j*m+m-1):
                if (i+m, i, 0) in rotor_config.configuration.values():
                    print('^',end='')
                else: print(' ',end='')
                print('   ',end='')
            if (i+m, i, 0) in rotor_config.configuration.values():
                print('^',end='')
            else: print(' ',end='')
            print()
            for i in range(j*m, j*m+m-1):
                print("|   ", end='')
            print('|', end='')
            print()
            for i in range(j*m, j*m+m-1):
                if (i, i+m, 0) in rotor_config.configuration.values():
                    print('v',end='')
                else: print(' ',end='')
                print('   ',end='')
            if (i, i+m, 0) in rotor_config.configuration.values():
                print('v',end='')
            else: print(' ',end='')
            print()


def rotor_order2edge_index(rotor_order: dict[Node, list[Edge]]) -> dict[Edge, int]:
    """
    Give the position of the edges in the given rotor order  
    Input :
        - rotor_order: the rotor order to convert
    Output:
        - dict[Edge: index in rotor order]
    """
    dic = dict()
    for node, edges in rotor_order.items():
        for edge in edges:
            dic[edge] = edges.index(edge)

    return dic
