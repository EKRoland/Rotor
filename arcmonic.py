from types_definition import *
import rotorgraph
from vector import Vector


class Arcmonic:
    def __init__(self, arcmonic:tuple[int, Vector]):
        """
        A class to represent a arcmonic function.
        Attribut: order and arcmonic values of the edges
        
        Input:
            - a tuple[int, dict[Edge, int]], the int will become the order and the Vector will give the arcmonic value of each edge
            - None (default) which gives order 0 and empty vector
        """
        if isinstance(arcmonic, tuple):
            self.order = arcmonic[0]
            self.arcmonic_values = arcmonic[1]
        
        elif arcmonic is None:
            self.order = 0
            self.arcmonic_values = Vector()
        else:
            raise TypeError("configuration has to be a tuple of integer and vector or nothing")
        
    def compute_on(self,  sum_of_arcs:ArcSum)-> tuple:
        """
        Gives the arcmonic value of a sum of arcs 
        Input:
            - Sum_of_arcs which armonic value will be computed 
        Output:
            - tuple = (order:int, armonic value:int)
        """
        arcmonic_value = 0
        for  edge, count in sum_of_arcs.items():
            if edge not in self.arcmonic_values.keys():
                raise ValueError(f"No arcmonic value for edge {edge}")
            else:
                arcmonic_value += count * self.arcmonic_values[edge]

        if self.order != 0:
            arcmonic_value = arcmonic_value % self.order

        return self.order, arcmonic_value
