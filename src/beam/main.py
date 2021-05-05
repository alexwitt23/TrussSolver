#!/usr/bin/env python3

"""The main script used to solve a simple 2D truss problem.
PYTHONPATH=. src/main.py \
    --displacements_file examples/displacements.txt \
    --elements_file examples/elements.txt \
    --forces_file examples/forces.txt \
    --nodes_file examples/nodes.txt

PYTHONPATH=. src/main.py \
    --displacements_file /home/alex/Desktop/classes/S2021/COE321K/hw4/displacements.txt \
    --elements_file /home/alex/Desktop/classes/S2021/COE321K/hw4/elements.txt \
    --forces_file /home/alex/Desktop/classes/S2021/COE321K/hw4/forces.txt \
    --nodes_file /home/alex/Desktop/classes/S2021/COE321K/hw4/nodes.txt


PYTHONPATH=. src/main.py \
    --displacements_file examples/hw2/displacements.txt \
    --elements_file examples/hw2/elements.txt \
    --forces_file examples/hw2/forces.txt \
    --nodes_file examples/hw2/nodes.txt

PYTHONPATH=. src/main.py \
    --displacements_file examples/hw4/displacements.txt \
    --elements_file examples/hw4/elements.txt \
    --forces_file examples/hw4/forces.txt \
    --nodes_file examples/hw4/nodes.txt


PYTHONPATH=. src/main.py \
    --displacements_file ../hw3_input_files/displacements.txt \
    --elements_file ../hw3_input_files/elements.txt \
    --forces_file ../hw3_input_files/forces.txt \
    --nodes_file ../hw3_input_files/nodes.txt

PYTHONPATH=. src/main.py \
    --displacements_file ../hw5/displacements.txt \
    --elements_file ../hw5/elements.txt \
    --forces_file ../hw5/forces.txt \
    --nodes_file ../hw5/nodes.txt

PYTHONPATH=. src/beam/main.py \
    --displacements_file examples/hw5/displacements.txt \
    --elements_file examples/hw5/elements.txt \
    --forces_file examples/hw5/forces.txt \
    --nodes_file examples/hw5/nodes.txt

"""

import argparse
import copy
import pathlib

import numpy as np

from src.beam import elements
from src.beam import forces
from src.beam import nodes
from src.beam import solver


def main(
    displacements_file: pathlib.Path,
    elements_file: pathlib.Path,
    forces_file: pathlib.Path,
    nodes_file: pathlib.Path,
) -> None:

    node_structure = nodes.Nodes(nodes_file, displacements_file)
    element_structure = elements.Elements(elements_file)
    element_structure.contruct_element_stiffness_matrices(node_structure.get_nodes())
    forces_structure = forces.Forces(forces_file, len(node_structure.get_nodes()))
    truss_solver = solver.Solver(node_structure, element_structure, forces_structure)
    truss_solver.solve()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--displacements_file", type=pathlib.Path, required=True)
    parser.add_argument("--elements_file", type=pathlib.Path, required=True)
    parser.add_argument("--forces_file", type=pathlib.Path, required=True)
    parser.add_argument("--nodes_file", type=pathlib.Path, required=True)
    args = parser.parse_args()

    main(
        args.displacements_file.expanduser(),
        args.elements_file.expanduser(),
        args.forces_file.expanduser(),
        args.nodes_file.expanduser(),
    )
