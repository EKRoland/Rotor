import networkx as nx
from types_definition import *

class Vector:

    def __init__(self, configuration:dict=None):
        """
        A class to represent a vector.
        Vector contains a dictionnary and act as one.
        Input:
            - configuration:
                - a dictionnary which will become the Vector
                - a RotorConfig, translate the RotorConfig to a Vector {edge: 1 for each edge in the values of the RotorConfig}
                - None (default) which gives an empty dict
        """
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif type(configuration).__name__ == "RotorConfig":
            self.configuration = {edge: 1 for edge in configuration.configuration.values()}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorConfig or nothing")
        

    def __str__(self):
        """dictionnary method"""
        return str(self.configuration)

    def __repr__(self):
        """dictionnary method"""
        return repr(self.configuration)

    def items(self):
        """dictionnary method"""
        return self.configuration.items()
    
    def keys(self):
        """dictionnary method"""
        return self.configuration.keys()

    def values(self):
        """dictionnary method"""
        return self.configuration.values()

    def __add__(self, other: Vector or object) -> Vector:
        """
        Overload the + operator.
        Case: Vector + Vector
            for each key, do the sum of the values in both vectors
        Case: Vector + Object (hashable)
            add one to the vector at the index object
        Input: 
            - self: Vector
            - other: Vector or Object
        Ouput:
            - new vector 
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) + config2.get(n, 0) for n in set(config1) | set(config2)}
        else:
            try:
                res_dic = dict(config1)
                if other in res_dic:
                    res_dic[other] += 1
                else:
                    res_dic[other] = 1
            except TypeError:
                raise TypeError("Second operand must be hashable or a Vector")
        return self.__class__(res_dic)

    def __radd__(self, other: Vector or object) -> Vector:
        """
        Same method as __add__ except that it makes the + operator commutative. 
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) + config2.get(n, 0) for n in set(config1) | set(config2)}
        else:
            try:
                res_dic = dict(config1)
                if other in res_dic:
                    res_dic[other] += 1
                else:
                    res_dic[other] = 1
            except TypeError:
                raise TypeError("Second operand must be hashable or a Vector")
        return Vector(res_dic)

    def __sub__(self, other: Vector or object) -> Vector:
        """
        Overload the - operator.
        Case: Vector - Vector
            for each key, do the substraction of the values in both vectors
        Case: Vector - Object (hashable)
            substract one to the vector at the index object
        Input: 
            - self: Vector
            - other: Vector or Object
        Ouput:
            - new vector 
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) - config2.get(n, 0) for n in set(config1) | set(config2)}
        else:
            try:
                res_dic = dict(config1)
                if other in res_dic:
                    res_dic[other] -= 1
                else:
                    res_dic[other] = -1
            except TypeError:
                raise TypeError("Second operand must be hashable or a Vector")
        return Vector(res_dic)

    def __mul__(self, other: int) -> Vector:
        """
        Overload the * operator.
        Case: Vector * integer
            for each key, multiply the integer to the value
        Input: 
            - self: Vector
            - other: integer
        Ouput:
            - new Vector
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k * other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return Vector(res_dic)

    def __rmul__(self, other: int) -> Vector:
        """
        Same method as __mul__ except that it makes the * operator commutative. 
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k * other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return Vector(res_dic)

    def __truediv__(self, other: int) -> Vector:
        """
        Overload the / operator.
        Case: Vector / integer
            for each key, divide the value by an integer
        Input: 
            - self: vector
            - other: integer
        Ouput:
            - new vector
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k // other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return Vector(res_dic)

    def __floordiv__(self, other: int) -> Vector:
        """
        Overload the // operator.
        Case: Vector // integer
            for each key, divide the values by an integer
        Input: 
            - self: vector
            - other: integer
        Ouput:
            - new vector
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k // other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return Vector(res_dic)

    def __lt__(self, other: object or int) -> bool:
        """
        Overload the < operator.
        Case: Vector < Vector
            for each key, compare the values in both vectors
        Case: Vector < integer
            for each key, compare the integer to the values
        Input: 
            - self: vector
            - other: vector or integer
        Ouput:
            - True if self < object
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) >= config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k >= other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a Vector")

    def __le__(self, other: object or int) -> bool:
        """
        Overload the <= operator.
        Case: Vector <= Vector
            for each key, compare the values in both vectors
        Case: Vector <= integer
            for each key, compare the integer to the values
        Input: 
            - self: vector
            - other: vector or integer
        Ouput:
            - True if self <= object
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) > config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k > other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a Vector")
    
    def __eq__(self, other: object or int) -> bool:
        """
        Overload the == operator.
        Case: Vector == Vector
            for each key, compare the values in both vectors
        Case: Vector == integer
            for each key, compare the integer to the values
        Input: 
            - self: vector
            - other: vector or integer
        Ouput:
            - True if self == object
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) != config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k != other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a Vector")
    
    def __ne__(self, other: object or int) -> bool:
        """
        Overload the != operator.
        Case: Vector != Vector
            for each key, compare the values in both vectors
        Case: Vector != integer
            for each key, compare the integer to the values
        Input: 
            - self: vector
            - other: vector or integer
        Ouput:
            - True if self != object
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) == config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k == other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a Vector")
    
    def __gt__(self, other: object or int) -> bool:
        """
        Overload the > operator.
        Case: Vector > Vector
            for each key, compare the values in both vectors
        Case: Vector > integer
            for each key, compare the integer to the values
        Input: 
            - self: vector
            - other: vector or integer
        Ouput:
            - True if self > object
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) <= config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k <= other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a Vector")

    def __ge__(self, other: object or int) -> bool:
        """
        Overload the >= operator.
        Case: Vector >= Vector
            for each key, compare the values in both vectors
        Case: Vector >= integer
            for each key, compare the integer to the values
        Input: 
            - self: vector
            - other: vector or integer
        Ouput:
            - True if self >= object
        """
        config1 = self.configuration
        if isinstance(other, Vector):
            config2 = other.configuration
            for n in set(config1) | set(config2):
                if config1.get(n, 0) < config2.get(n, 0):
                    return False
            return True
        elif isinstance(other, int):
            for n, k in config1.items():
                if k < other:
                    return False
            return True
        else:
            raise TypeError("Second operand must be an int or a Vector")

        
    def __setitem__(self, index:object, value:object):
        """
        Overload the assignement operator.
        Set the value in dict at the given index.
        Input: 
            - self: vector
            - index: dictionnary key
            - value: value to store
        No ouput
        """
        self.configuration[index] = value

    def __getitem__(self, index: object):
        """
        Overload the getter operator.
        Return the value in dict at the given index.
        Input: 
            - self: vector
            - index: dictionnary key
        Output:
            - the value at the given index
        """
        return self.configuration.get(index, 0)

    def __delitem__(self, index: object):
        """
        Overload the deleter operator.
        Input:
            - self: vector 
            - index: dictinnay key
        No output
        """
        del self.configuration[index]

    def __len__(self) -> int:
        """dictionnary method"""
        return len(self.configuration)
    """
    def to_dict_node(self) -> dict():
        dico= {edge[0]: edge for edge, value in self.configuration.items() if value}
        return dico
    """