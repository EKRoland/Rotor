import networkx as nx
from types_definition import * 
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig
from matrices import Matrix
from arcsum import ArcSum
from arcmonic import Arcmonic
import numpy as np
from smithnormalform import matrix, snfproblem, z



def particle_configuration():
    """
    An example of particle configuration manipulations
    """
    # creation of the simple path graph (n = 5 by default)
    G = RotorGraph.simple_path()

    # creation of the particle config (dict: Node -> int)
    s1 = ParticleConfig(G)
    # set 5 particles on every node
    s1.set_all_particles(5)

    print("s1:", s1)
    # Double all particles 
    s1 *= 2
    print("s1:", s1)

    s2 = ParticleConfig()
    # set 12 particles on the node 2
    s2[2] = 12
    print("s2:", s2)

    # add the particle configurations s1 and s2
    s3 = s1 + s2
    print("s3=s1+s2: ", s3)

    print("s1:", s1)
    print("s2:", s2)

    # add 1 particle on the node 2
    print("s2 + 2:", s2 + 2)

def rotor_configuration():
    """
    An example of rotor configuration manipulations
    """
    #creation of the simple path graph (n = 5 by default)
    G = RotorGraph.simple_path()
    # creation of the rotor config (dict: node -> edge (tuple))
    rho = RotorConfig(G)
    # visual representation of the simple path 
    display_path(rho)
    ##print(rho)
    edge = (1, 0, 0)

    # set the edge (1, 0, 0) in the rotor config for the node 1
    rho[1] = edge
    #display_path(rho)

    # translate the rotor config into a vector
    vec = Vector(rho)
    print(vec)

    # set the next edge according to the rotor order 
    vec = vec - edge + G.turn(edge)
    print(vec)


    # tranlaste the vector into a rotor config 
    rho2 = RotorConfig(vec)
    print(rho2)

    #display_path(rho2)


def simple_path_graph():
    """
    Example of legal routing and complete routing
    """
    # creation of the simple path graph with 7 nodes (n = number of nodes that are not considered as sink)
    G = simple_path(n=7, x=2, y=2)
    # create the rotor config (dict: node -> edge (tuple))
    rho = RotorConfig(G)
    G.check_rotor_config(rho)
    # create the particle configuration (dict: Node -> int)
    sigma = ParticleConfig(G)
    # set 3 particles on every nodes including sinks
    sigma.set_all_particles(3)

    display_path(rho, sigma)


    # legal routing : only routes particles (no antiparticles) to the sinks 
    sigma, rho, info = G.legal_routing(sigma, rho)
    display_path(rho, sigma)

    # display informations about the routing
    #print("info", info)
    

    # equivalent to sigma.set_particles(3, -4)
    # set 4 antiparticles on the node 3
    ##sigma[3] = -4
    ##display_path(rho, sigma)

    # complete routing : first routes particles, then routes antiparticles to the sinks
    sigma, rho, info = G.complete_routing(sigma, rho)
    
    # display informations about the routing
    ##print("info", info)
    display_path(rho, sigma)

    #p=G.enum_configurations()
    #print(list(p))
    


def laplacian_matrices():
    """
    Example of using methods to calculate laplacian matrices and reduced laplacian matrices
    """
    G = RotorGraph.simple_path()
    L = G.laplacian_matrix()
    rL = G.reduced_laplacian_matrix()
    print(L)
    print(rL)


def smith_normal_form():
    """
    Example of resolving the smith normal form problem
    """
    G = RotorGraph.simple_path(n=2, x=2, y=6)
    matrix = G.laplacian_matrix()
    print(matrix)
    # compute the snf problem
    prob = matrix.snf_problem()

    # J is the diagonalized matrix
    print(prob.J)
    # S and T are complementary unimodular matrices
    print(prob.S)
    print(prob.T)
    
    print(prob.S * prob.A * prob.T)
    #A==matrix

def acyclic_recurrents():
    """
    Example of obtaining acyclic and recurrent configurations
    """
    # creation of the 3x3 grid 
    G = RotorGraph.grid(3, 3, "corner")
    # list all acyclic configurations (acy : list[RotorConfig])
    acy = G.enum_acyclic_configurations()
    
    for config in acy:
        # visual representation of the grid 
        display_grid(config, 3, 3)
        print("###########################")
    # dislay the determinant
    print("det =", G.reduced_laplacian_matrix().determinant())
    # display the number of acyclic configurations
    print("nb of acyclic =", len(acy))

    #  for all acyclic configuration, gives the corresponding recurrent configuration
    rec = G.recurrent_from_acyclic(acy)

    #print(rec)

    # give the tuple (rec, acy) for each class
    rec_acy = G.recurrent_and_acyclic(acy)
    for tupl in rec_acy: print(tupl)


if __name__ == "__main__":
    #acyclic_recurrents()
    #particle_configuration()
    rotor_configuration()
    #simple_path_graph()
    #smith_normal_form()
    