
import copy

import numpy as np

from src import elements
from src import forces
from src import nodes


class Solver:

    def __init__(
        self,
        node_structure: nodes.Nodes,
        elements_structure: elements.Elements,
        forces_structure: forces.Forces
    ) -> None:
        self.node_structure = node_structure
        self.element_structure = elements_structure
        self.forces_structure = forces_structure

    
    def solve(self):
        k_global = np.zeros(2 * [2 * len(self.node_structure.get_nodes())])

        global_forces = self.forces_structure.force_vec
        displacement_vec = self.node_structure.displacement_vec

        for idx, element_ in self.element_structure.elements.items():
            x = int((element_.node1 - 1) * 2)
            y = int((element_.node2 - 1) * 2)
            k_global[x : x + 2, x : x + 2] += element_.stiffnes_matrix[:2, :2]
            k_global[x : x + 2, y : y + 2] += element_.stiffnes_matrix[:2, 2:]
            k_global[y : y + 2, y : y + 2] += element_.stiffnes_matrix[2:, 2:]
            k_global[y : y + 2, x : x + 2] += element_.stiffnes_matrix[2:, :2]

        k_global_unreduced = copy.deepcopy(k_global)

        solved_displacements = []
        rows = []
        for idx, node_ in self.node_structure.nodes.items():
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

        displacements = np.linalg.solve(k_global, np.transpose(global_forces))

        d = 0
        for idx, node_ in self.node_structure.nodes.items():
            x = int((node_.global_idx - 1) * 2)
            y = int((node_.global_idx - 1) * 2 + 1)
            if x in solved_displacements:
                node_.dx = displacements[solved_displacements.index(x), 0]
            if y in solved_displacements:
                node_.dy = displacements[solved_displacements.index(y), 0]

        self.element_structure.find_internal_forces()

        displacement_vec = self.node_structure.displacement_vec

        for solved_d, value in zip(solved_displacements, displacements[:, 0]):
            displacement_vec[0, solved_d] = value

        print(f">> Displacement vector:\n{displacement_vec}")
        print(f">> Internal Forces:\n{np.matmul(k_global_unreduced, np.transpose(displacement_vec))}")

