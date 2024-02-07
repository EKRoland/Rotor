"""import networkx as nx
import matplotlib.pyplot as plt

def has_undirected_cycle(arc_sum):
    G = nx.MultiDiGraph()

    for arc, count in arc_sum.items():
        for _ in range(count):
            G.add_edge(arc[0], arc[1])

    # Convertir le multigraphe en un graphe simple
    simple_G = nx.Graph(G)

    # Vérification de la présence de cycles non orientés
    cycles = list(nx.cycle_basis(simple_G))

    return cycles

# Exemple de vecteur de somme d'arc
arc_sum = {(1, 2, 0): 1, (2, 3, 0): 1, (0, 1, 0): 1, (3, 2, 0): 1, (3, 6, 0): 1, (2, 5, 0): 1, (4, 7, 0): 1, (5, 8, 0): 1}

# Vérification de la présence de cycles non orientés
cycles = has_undirected_cycle(arc_sum)

if cycles:
    print("La somme d'arcs contient un cycle non orienté.")
    print("Cycles détectés:", cycles)
else:
    print("La somme d'arcs ne contient pas de cycle non orienté.")
"""


"""
import networkx as nx

# Création d'un exemple de multigraphe
G = nx.MultiGraph()
G.add_edges_from([(1, 2), (1, 2), (3, 4), (3, 4)])

# Vérification de la présence de cycles
cycles = list(nx.simple_cycles(G))

if cycles:
    print("Le multigraphe contient des cycles.")
    print("Cycles détectés:", cycles)
else:
    print("Le multigraphe ne contient pas de cycle.")
"""

"""
import networkx as nx

# Création d'un exemple de multigraphe
G = nx.MultiGraph()
G.add_edges_from([(0, 1, 0), (0, 3, 0), (0, 3, 1), (1, 2, 0), (1, 4, 0), (3, 6, 0), (2, 5, 0), (4, 7, 0), (5, 8, 0)])

# Vérification de la présence de cycles
print(G.edges)
cycles = list(nx.simple_cycles(G))

print(cycles)



import numpy as np

# Définir une matrice (par exemple, une matrice 3x3)
matrix = np.array([[2, -1, 0, 0], [1, 1, -1, 0], [1, 0, -2, 1], [1, 0, -1, -1]])

# Calculer le déterminant de la matrice
determinant = np.linalg.det(matrix)

print("Déterminant de la matrice :", determinant)

"""
import numpy as np

# Créez une matrice
matrice = np.array([[1, 23, 456],
                    [78, 9, 1011],
                    [12, 1314, 15]])

# Affichez la matrice avec indentation et alignement
#np.set_printoptions(formatter={'int': lambda x: f"{x:5}"})
print(matrice)

matrice1 = np.array([[1,23, 456],
                    [78, -5, 11],
                    [12, 14, 15]])
print(matrice1)


from sympy import Matrix
import numpy as np

# Créez une matrice SymPy
M_sympy = Matrix([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# Convertissez la matrice SymPy en une matrice NumPy
M_numpy = np.array(M_sympy)

# Affichez la matrice NumPy
print(type(M_numpy))
print(M_numpy[:,1])
