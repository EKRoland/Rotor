from types_definition import *
import rotorgraph
import vector

class ArcConfig(vector.Vector):

    def __init__(self, configuration:dict=None):
        """
        A class to represent sum of arcs.
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

