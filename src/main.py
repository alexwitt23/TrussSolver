#!/usr/bin/env python3

"""
PYTHONPATH=. src/main.py \
    --displacements_file examples/displacements.txt \
    --elements_file examples/elements.txt \
    --forces_file examples/forces.txt \
    --nodes_file examples/nodes.txt
"""

import argparse
import copy
import pathlib

import numpy as np

from src import element
from src import forces
from src import nodes


def main(
    displacements_file: pathlib.Path,
    elements_file: pathlib.Path,
    forces_file: pathlib.Path,
    nodes_file: pathlib.Path,
) -> None:

    node_structure = nodes.Nodes(nodes_file, displacements_file)
    element_structure = element.Elements(elements_file)
    element_structure.contruct_element_stiffness_matrices(node_structure.get_nodes())
    forces_structure = forces.Forces(forces_file, len(node_structure.get_nodes()))
    node_dict = node_structure.get_nodes()

    k_global = np.zeros(2 * [2 * len(node_structure.get_nodes())])

    global_forces = forces_structure.force_vec
    print("G", global_forces)
    displacement_vec = node_structure.displacement_vec

    for idx, element_ in element_structure.elements.items():
        x = (element_.node1 - 1) * 2
        y = (element_.node2 - 1) * 2
        print(idx, element_)
        print(k_global[x : x + 4, x : x + 2].shape)
        print(element_.stiffnes_matrix[:, :2].shape)
        k_global[x : x + 2, x : x + 2] += element_.stiffnes_matrix[:2, :2]
        k_global[x : x + 2, y : y + 2] += element_.stiffnes_matrix[:2, 2:]
        k_global[y : y + 2, y : y + 2] += element_.stiffnes_matrix[2:, 2:]
        k_global[y : y + 2, x : x + 2] += element_.stiffnes_matrix[2:, :2]

    k_global_unreduced = copy.deepcopy(k_global)

    solved_displacements = []
    rows = []
    for idx, node_ in node_structure.nodes.items():
        x = int((node_.global_idx - 1) * 2)
        y = int((node_.global_idx - 1) * 2 + 1)
        if node_.dx is not None:
            global_forces -= node_.dx * k_global[:, x]
            rows.append(x)
        else:
            solved_displacements.append(x)
        if node_.dy is not None:
            global_forces -= node_.dy * k_global[:, y]
            rows.append(y)
        else:
            solved_displacements.append(y)

    while rows:
        k_global = np.delete(k_global, rows[0], 0)
        k_global = np.delete(k_global, rows[0], 1)
        global_forces = np.delete(global_forces, rows[0], 1)
        displacement_vec = np.delete(displacement_vec, rows[0], 1)
        rows = [r - 1 for r in rows[1:]]
    print("G", global_forces)
    print(k_global_unreduced)
    displacements = np.linalg.solve(k_global, np.transpose(global_forces))

    d = 0
    for idx, node_ in node_structure.nodes.items():
        x = int((node_.global_idx - 1) * 2)
        y = int((node_.global_idx - 1) * 2 + 1)
        if x in solved_displacements:
            node_.dx = displacements[solved_displacements.index(x), 0]
        if y in solved_displacements:
            node_.dy = displacements[solved_displacements.index(y), 0]

    element_structure.find_internal_forces()

    displacement_vec = node_structure.displacement_vec

    print(displacements)
    for solved_d, value in zip(solved_displacements, displacements[:, 0]):
        displacement_vec[0, solved_d] = value

    print(displacement_vec)
    print(np.matmul(k_global_unreduced, np.transpose(displacement_vec)))


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
