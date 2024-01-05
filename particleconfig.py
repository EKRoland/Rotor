from types_definition import *
import vector

class ParticleConfig(vector.Vector):

    def __init__(self, configuration:dict=None):
        """
        A class to represent the particles configuration.
        It inherits all methods of the class Vector.
        ParticleConfig contains a dictionnary and act as one, 
        the keys are the nodes and the values are the number of particles
        ParticleConfig: V -> Z
        Input:
            - configuration:
                - a dictionnary which will become the ParticleConfig
                - a graph, every nodes of the graph will be initialized with zero particle
                - None (default) which gives an empty dict
        """
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif type(configuration).__name__ == "RotorGraph":
            self.configuration = {node: 0 for node in configuration}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorGraph or nothing")


    def first_node_with_particle(self, sinks: set) -> Node or None:
        """
        Find the first (non sink) node which holds at least one particle
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - the first non sink node with at least one particle if there is one
            else None
        """
        for node, k in self.configuration.items():
            if k > 0 and node not in sinks:
                return node
        return None

    def first_node_with_antiparticle(self, sinks: set) -> Node or None:
        """
        Find the first (non sink) node which holds at least one antiparticle
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - the first non sink node with at least antiparticle if there is one
            else None
        """
        for node, k in self.configuration.items():
            if k < 0 and node not in sinks:
                return node
        return None

    def transfer_particles(self, u: Node, v: Node, k: int=1):
        """
        Transfer k particles from node u to node v
        Input:
            - u: node giving the k particles
            - v: node receiving the k particles
            - k: the number of particles to transfer (default: one particle)
        No output
        """
        self.remove_particles(u, k)
        self.add_particles(v, k)

    def add_particles(self, node:Node, k:int=1):
        """
        Add k on the given node
        Input:
            - node: the node where to add k particles 
            - k: the number of particles (default: one particle)
        No output
        """
        if node in self.configuration:
            self.configuration[node] += k
        else: self.configuration[node] = k

    def add_all_particles(self, k:int=1):
        """
        Add k particles on every nodes
        Input:
            - k: the number of particles (default: one particle)
        No output
        """
        for node in self.configuration:
            self.configuration[node] += k

    def remove_particles(self, node:Node, k:int=1):
        """
        Remove k particles on the given node
        Input:
            - node: the node where to remove k particles 
            - k: the number of particles (default: one particle)
        No output
        """
        if node in self.configuration:
            self.configuration[node] -= k
        else: self.configuration[node] = -k

    def remove_all_particles(self, node:Node, k:int=1):
        """
        Remove k particles on every nodes
        Input:
            - k: the number of particles (default: one particle)
        No output
        """
        if node in self.configuration:
            self.configuration[node] -= k
        else: self.configuration[node] = -k

    def set_particles(self, node:Node, k:int=1):
        """
        Set k particles on the given node
        Input:
            - node: the node where to set k particles 
            - k: the number of particles (default: one particle)
        No output
        """
        self.configuration[node] = k

    def set_all_particles(self, k:int=1):
        """
        Set k particles on every nodes
        Input:
            - k: the number of particles (default: one particle)
        No output
        """
        for node in self.configuration:
            self.configuration[node] = k

