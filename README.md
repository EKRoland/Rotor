# RotorGraph :gear:

## :scroll: Description

A tool box for rotor graph research

## :bookmark: Table of contents
- [Usage](#computer-usage)
- [Dependencies](#construction-dependencies)
- [Content](#file_folder-content)
  - [RotorGraph](#rotorgraphclass)
  - [Results](#resultsclass)
  - [ParticleConfig](#particleconfigclass)
  - [RotorConfig](#rotorconfigclass)
  - [Vector](#vectorclass)
  - [Matrix](#matrixclass)


## :computer: Usage

see `main_examples.py`

## :construction: Dependencies

*Python version used : 3.10.10*

To install the dependences needed:  
`pip install -r requirement.txt`

It will install the following modules:
* networkx
* smithnormalform
* pyunionfind

## :file_folder: Content

### RotorGraph(class)
Simulate a rotor graph from the networkx.MultiDiGraph class
Methods:
* **simple_path(n=5, x=1, y=1)**, create a simple path RotorGraph with **n** nodes, **x** left edges, **y** right edges and 2 sinks (extremities)
* **grid(n: int=3, m: int=3, sinks: str="")**, create a grid RotorGraph with **n** rows and **m** columns, sinks &in; {"borders", "corners", "center"}
* **random_graph(min_nb_nodes:int=5, max_nb_nodes:int=15)**, create a random RotorGraph with n nodes, n &in; [min_nb_nodes..max_nb_nodes]
* **remove_edge(self, *edges: Edge)**, remove given edges (e.g. G.remove_edge(e1, e2, e3) or G.remove_edge(e1))
* **set_sink(self, \*nodes: Node)**, set given nodes as sink
* **remove_sink(self, \*nodes: Node)**, unset given nodes as sink
* **head(self, edge: Edge)**, return head of edge
* **tail(self, edge: Edge)**, return tail of edge
* **set_rotor_order(self, new_order: dict[Node, list(Edge)])**, set the rotor order of the RotorGraph
* **invert_rotor_order(self)**, invert the rotor order
* **check_rotor_config(self, rotor_config: RotorConfig):**, Check if the given rotor configuration is valid for the RotorGraph
* **turn(self, edge: Edge, k: int=1)**, Give the next edge of the given edge in rotor order
* **turn_all(self, rotor_config: RotorConfig, k: int=1, sinks: set=None) -> RotorConfig:**, Turn all edges of the configuration
* **reverse_turn(self, edge: Edge, k: int=1)**, Give the previous edge of the given edge in rotor order
* **reverse_turn_all(self, rotor_config: RotorConfig, k: int=1, sinks: set=None)**, Turn all edges of the configuration in the reverse order
* **step(self, particle_config: object, rotor_config: RotorConfig, node: Node=None, sinks: set=None, turn_and_move: bool=False, info=None) -> (ParticleConfig, RotorConfig)**, Make one step of routing
* **reverse_step(self, particle_config: object, rotor_config: RotorConfig, node:Node=None, sinks: set=None, turn_and_move: bool=False, info=None) -> (ParticleConfig, RotorConfig)**, Make one step of routing in reverse
* **legal_routing(self, particle_config: object, rotor_config: RotorConfig, sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig)**, Route particles to the sinks
* **route_one_particle(self, node: Node, rotor_config: RotorConfig, sinks: set=None, turn_and_move: bool=False) -> RotorConfig**, Route one particule from the given node to a sink
* **complete_routing(self, particle_config: ParticleConfig, rotor_config: RotorConfig, sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig)**, Route particles and antiparticles to the sinks
* **laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]**, Create the laplacian matrix of the graph
* **reduced_laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]**, Create the reduced laplacian matrix of the graph
* **vector_routing(self, particle_config: object, rotor_config: RotorConfig, vector: dict[Node:int], sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig)**, Route the graph according to a given vector optimized with the laplacian matrix
* **enum_configurations(self, sinks:set=None) -> list[RotorConfig]**, Gives a list of all the rotor configuration of the graph
* **enum_acyclic_configurations(self, sinks:set=None) -> list[RotorConfig]**, Gives a list of all the acyclic rotor configuration of the graph where each represents a class
* **recurrent_from_acyclic(self, list_acyclic:list[RotorConfig]) -> list[tuple[RotorConfig, RotorConfig]]**, For all acyclic configuration, gives the corresponding recurrent configuration in the class
* **recurrent_and_acyclic(self, list_acyclic:list[RotorConfig]) -> list[tuple[RotorConfig, RotorConfig]]**, For all acyclic configuration, gives the corresponding recurrent configuration in the class

---

### Results(class)

Keep track of important informations during a routing:
- nb_steps: total number of steps for the routing
- nb_l_edges: number of edges going left (only relevant for simple path graph)
- nb_r_edges: number of edges going right (only relevant for simple path graph)
- edges_counter: a dictionnary, {edge: number of times taken}
- nodes_counter: a dictionnary, {node: number of times taken}
- nb_particles_in_sinks: a dictionnary, {sink: number of particles}
- last_visit: a dictionnary, {node: number of the step when it was last visited (between 0 and nb_steps)}
- configuration_history: the list of the configurations (rotor, particle) from oldest to newest

ℹ️ Possibility to *print* an instance of the class Results

---

### ParticleConfig(class)

 A class to represent the particles configuration. It inherits all methods of the class Vector.
  ParticleConfig contains a dictionnary and act as one, the keys are the nodes and the values are the number of particles ParticleConfig: V -> Z

- **first_node_with_particle:self, sinks: set) -> Node or None**, Find the first (non sink) node which holds at least one particle
- **first_node_with_antiparticle(self, sinks: set) -> Node or None**, find the first (non sink) node which holds at least one antiparticle
- **transfer_particles(self, u: Node, v: Node, k: int=1)**, transfer k particles from node u to node v
- **add_particles(self, node:Node, k:int=1)**, add k on the given node
- **add_all_particles(self, k:int=1)**, add k particles on every nodes
- **remove_particles(self, node:Node, k:int=1)**, remove k particles on the given node
- **remove_all_particles(self, node:Node, k:int=1)**, remove k particles on every nodes
- **set_particles(self, node:Node, k:int=1)**, set k particles on the given node
- **set_all_particles(self, k:int=1)**, set k particles on every nodes

---

### RotorConfig(class)

A class to represent the rotor configuration.  
RotorConfig contains a dictionnary and act as one, the keys are the nodes and the values are the next edge to take.
RotorConfig: V &rarr; A

Methodes:
* main dictionnary methods (items, keys, values...)
* **find_cycles(self, sinks: set[Node]=set()) -> list[list[Edge]]**, Find all cycles from a rotor configuration
* **to_graph(self) -> RotorGraph**, Gives the corresponding RotorGraph of the RotorConfig
* **cycle_push(self, rotor_graph: RotorGraph, cycle: list[Edge])**, Turn all of the given edges in the RotorConfig
* **destination_forest(self, rotor_graph: RotorGraph, sinks: set[Node]=set())**, The configuration obtained by a maximal cycle push sequence on a rotor configuration

---

### Vector(class)

A class to represent a vector.
Vector contains a dictionnary and act as one.

Methods:
* main dictionnary methods (items, keys, values...)

---

### Matrix(class)

This class is mainly usefull for the smith normal form problem.
It also inherits methods from the Matrix class of the smithnormalform module like:
            - determinant
            - addition and multiplication between two matrices
            - equality test between two matrices

* **snf_problem(self) -> snfproblem.SNFProblem**, compute the smith normal form problem of the matrix and return the result as an instance of the class SNFProblem from the module smithnormalform
