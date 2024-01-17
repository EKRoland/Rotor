import networkx as nx
from types_definition import * 
from vector import Vector
from rotorconfig import RotorConfig
from rotorgraph import RotorGraph, display_path, all_config_from_recurrent, display_grid
from particleconfig import ParticleConfig
from matrices import Matrix
import random
from itertools import product
import copy

# creation of the path graph with 7+2 nodes and x left arcs and y right arcs
n=4
x=4
y=3
G = RotorGraph.simple_path(n, x, y)


# choice of the rotor config (dict: node -> edge (tuple))
choice_configuration = {}

#exemple
'''
choice_configuration = {
    1: (1,2,4),
    2: (2,3,0),
    3: (3,2,6),
    4: (4,5,0)
}
'''

# random choice

for i in range(1,n):
    head_node = random.choice((i-1, i+1))
    if head_node == i-1:
        number_edge = random.randint(0, x-1)
    else:
        number_edge = random.randint(0, y-1)
    choice_configuration[i]=(i,head_node,number_edge)


# all possible choice

##liste des choix d'arcs sortants possibles sur les sommets 1 à n    
liste_edges=[]   
for i in range(1,n+1):
    liste_edges.append([])
    for head_node in ([i-1,i+1]):
        if head_node == i-1:
            for number_edge in range(0,x):
                liste_edges[i-1].append((i,head_node,number_edge))    
        else:
            for number_edge in range(0,y):
                liste_edges[i-1].append((i,head_node,number_edge))  
                #choice_configuration[i]=(i,head_node,number_edge)



##liste de toutes les configuartions de rotor possibles juste avec les arcs
def generate_combinations(list_of_lists):
    return list(product(*list_of_lists))

liste_preconfig= generate_combinations(liste_edges)


##liste contenant des dictionnaire qui sont les configuartions de rotor
liste_config= []
'''
liste_config= []
for preconfig in liste_preconfig:
    liste_config.append(  {
    1: preconfig[0],
    2: preconfig[1],
    3: preconfig[2],
    4: preconfig[3]
} )
'''    

liste_config2=[]
for preconfig in liste_preconfig:
    dictionnaire = {}
    for i, valeur in enumerate(preconfig, start=1):
        dictionnaire[i] = valeur
    liste_config2.append(dictionnaire)

liste_config = liste_config2



'''
#routage d'une particule

print(liste_config[-1])
choice_configuration=liste_config[-1]

rho= RotorConfig(choice_configuration)
#G.check_rotor_config(rho)
#
#position of the particle
sigma_init=1

#routing to sink
final_rotor_configuration, info = G.route_one_particle(sigma_init, rho)
for rho, sigma in info.configuration_history:
    display_path(rho, sigma)

#print(final_rotor_configuration)

#print(rho_begin)
'''



#fonction supprimant les cycles dans une configuration de rotor pour produire un arbre
def supprime_cycle(choice_configuration: dict, n, compteur_cycle)-> (dict,int):
    for i in range(1,n):
        if (choice_configuration[i][1] == i+1) and (choice_configuration[i+1][1] == i):
            compteur_cycle += 1
            if (y-choice_configuration[i][2])< (x- choice_configuration[i+1][2]):
                choice_configuration[i+1]=(i+1, i, choice_configuration[i+1][2] + y-choice_configuration[i][2])
                choice_configuration[i]=(i,i-1,0)

            elif (y-choice_configuration[i][2]) > (x- choice_configuration[i+1][2]):
                choice_configuration[i]=(i,i+1, choice_configuration[i][2] + x-choice_configuration[i+1][2])
                choice_configuration[i+1]=(i+1,i+2,0)
            else:
                choice_configuration[i]=(i,i-1,0)
                choice_configuration[i+1]=(i+1,i+2,0)
            #print(choice_configuration,compteur_cycle)
            _, compteur_cycle = supprime_cycle(choice_configuration, n, compteur_cycle)
        else: 
            continue
    return (choice_configuration,compteur_cycle)



#cycle_push de l'enseble des configuration de rotor
liste_arbre=[]
for choice_configuration in liste_config:
    configuration1 = copy.deepcopy(choice_configuration)
    arbre, nombre_cycle = supprime_cycle(configuration1,n,0)
    liste_arbre.append((arbre, nombre_cycle))


#liste de nombre de cycle pusher dans les configuration de rotor

liste_nombre_cycle = []
for arbre_push in liste_arbre:
    liste_nombre_cycle.append(arbre_push[1])


print(n,x,y)
print("maximum de push", max(liste_nombre_cycle))
print("moyenne de push", sum(liste_nombre_cycle) / len(liste_nombre_cycle))


'''
k = random.randint(0, len(liste_config) - 1)



print(liste_config[k])
print(liste_arbre[k][0])
print(liste_arbre[k][1])
#print(supprime_cycle(liste_config[k],n,0))


'''

#print(choice_configuration)    
#arbre, nombre_cycle = supprime_cycle(choice_configuration,n,0)
#print(arbre, nombre_cycle)


'''
#puits de sortie utilisant la configuration acyclique équivalente
print(arbre)
if arbre[sigma_init][1]<sigma_init:
    print("puits de sortie: 0")
else:
    print("puits de sortie: ", n+1)
'''
