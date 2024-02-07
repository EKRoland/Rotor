from smithnormalform import matrix, snfproblem, z
import numpy as np

class Matrix(matrix.Matrix):
    
    def __init__(self, obj):
        """
        This class is mainly usefull for the smith normal form problem.
        It also inherits methods from the Matrix class of the smithnormalform module like:
            - determinant
            - addition and multiplication between two matrices
            - equality test between two matrices
        Input:
            - obj: a dict of dicts
        No output
        """
        if isinstance(obj, dict):
            self.dictionnary = obj
            n = len(obj)
            m = len(next(iter(obj.values())))
            values = [z.Z(v) for line in obj.values() for v in line.values()]
            matrix.Matrix.__init__(self, n, m, values)
        elif type(obj).__name__ == "Matrix":
            matrix.Matrix.__init__(self, obj.h, obj.w, obj.elements)
        else:
            raise TypeError("obj has to be a dict or a Matrix")

    def snf_problem(self) -> snfproblem.SNFProblem:
        """
        Compute the smith normal form problem of the matrix
        and return the result as an instance of the class SNFProblem from the module smithnormalform
        The class SNFProblem has multiple attributes:
            - A: The Matrix that we want to find the smith normal form of
            - J: The smith normal form of A
            - S: The complementary unimodular matrix (line operations)
            - T: The complementary unimodular matrix (column operations)
        snfproblem.S * snfproblem.A * snfproblem.T == snfproblem.J
        No input
        Output:
            - instance of the class SNFProblem
        """
        prob = snfproblem.SNFProblem(self)
        prob.computeSNF()
        
        
        for i in range(min(self.h, self.w)):
            if prob.J.get(i,i).a < 0:
                prob.J.set(i,i, prob.J.get(i,i)*z.Z(-1))
                for j in range(self.h):
                    prob.S.set(i,j, prob.S.get(i,j)*z.Z(-1))
        
        if not prob.isValid:
            raise ValueError("Problem is not valid")

        if not (prob.S*self*prob.T == prob.J):
            raise ValueError("J != S*A*T")
        
        return prob
    
    def to_numpy(self) -> np.ndarray:

        """
        Convert Matrix to numpy array
        Input:
            - Matrix 
        Output:
            - Numpy matrix
        """
        Matrice=[]
        for i in range(self.h):
            Matrice.append([])
            for j in range (self.w):
                Matrice[i].append(self.get(i,j).a)  

        return  np.array(Matrice)
            

