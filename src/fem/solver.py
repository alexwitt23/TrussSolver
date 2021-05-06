import copy

import matplotlib.pyplot as plt
import numpy as np

from src.fem import elements
from src.fem import forces
from src.fem import nodes


class Solver:
    def __init__(
        self,
        node_structure: nodes.Nodes,
        elements_structure: elements.Elements,
        forces_structure: forces.Forces,
    ) -> None:
        self.node_structure = node_structure
        self.element_structure = elements_structure
        self.forces_structure = forces_structure

    def solve(self):
        k_global = np.zeros(2 * [2 * len(self.node_structure.get_nodes())])
        global_forces = self.forces_structure.force_vec
        displacement_vec = self.node_structure.displacement_vec
        print(k_global.shape, global_forces.shape, displacement_vec.shape)

        for idx, element_ in self.element_structure.elements.items():
            a = int((element_.node1 - 1) * 2)
            b = int((element_.node2 - 1) * 2)
            c = int((element_.node3 - 1) * 2)

            for idx_row, row in enumerate([a, b, c]):
                for idx_col, col in enumerate([a, b, c]):
                    k_global[row : row + 2, col : col + 2] += element_.stiffnes_matrix[
                        idx_row : idx_row + 2, idx_col : idx_col + 2
                    ]

        k_global_unreduced = copy.deepcopy(k_global)
        solved_displacements = []
        rows = []
        for idx, node_ in self.node_structure.nodes.items():
            a = int((node_.global_idx - 1) * 2)
            b = int((node_.global_idx - 1) * 2 + 1)
            if node_.dx is not None:
                global_forces -= node_.dx * k_global[:, a]
                rows.append(a)
            else:
                solved_displacements.append(a)

            if node_.dy is not None:
                global_forces -= node_.dy * k_global[:, b]
                rows.append(b)
            else:
                solved_displacements.append(b)

        print(k_global.shape, "A")
        while rows:
            k_global = np.delete(k_global, rows[0], 0)
            k_global = np.delete(k_global, rows[0], 1)
            global_forces = np.delete(global_forces, rows[0], 1)
            displacement_vec = np.delete(displacement_vec, rows[0], 1)
            rows = [r - 1 for r in rows[1:]]
        print(k_global.shape, "B")

        displacements = np.linalg.solve(k_global, np.transpose(global_forces))

        for idx, node_ in self.node_structure.nodes.items():
            a = int((node_.global_idx - 1) * 2)
            b = int((node_.global_idx - 1) * 2 + 1)
            if a in solved_displacements:
                node_.dx = displacements[solved_displacements.index(a), 0]
            if b in solved_displacements:
                node_.dy = displacements[solved_displacements.index(b), 0]
            self.node_structure.nodes[idx] = node_

        self.element_structure.find_internal_forces()

        displacement_vec = self.node_structure.displacement_vec

        for solved_d, value in zip(solved_displacements, displacements[:, 0]):
            displacement_vec[0, solved_d] = value

        print(">> Displacement vector:")
        for idx, item in enumerate(displacement_vec[0]):
            print(f"Node_{idx // 2 + 1} displacement, DOF {idx % 2}: {item:.5E}")

        print(displacement_vec[0].shape, len(list(self.node_structure.nodes.values())))
        for node in self.node_structure.nodes.values():
            plt.plot([node.x], [node.y], 'o', color='black')
            x = int((node.global_idx - 1) * 2)
            dx = displacement_vec[0, x]
            dy = displacement_vec[0, x+1]
            plt.plot([node.x + dx], [node.y + dy], 'o', color='green')
            print(node, [node.x + dx], [node.y + dy])

        plt.show()

        print(">> Internal Forces:")
        internal_forces = self.element_structure.internal_forces
        for idx, item in enumerate(internal_forces):
            print(f"Element_{idx + 1} Internal Force: {item:.5E}")

        print(">> External Forces:")
        print(k_global.shape, displacement_vec.shape)
        internal_forces = np.matmul(k_global_unreduced, np.transpose(displacement_vec))
        for idx, item in enumerate(internal_forces[:, 0]):
            print(f"Node_{idx // 2 + 1} External Force, DOF {idx % 2}: {item:.5E}")

        print(">> Element Strains:")
        element_strains = self.element_structure.find_element_strain()
        for idx, item in enumerate(element_strains):
            print(f"Element_{idx + 1} Strain: {item:.5E}")

        print(">> Element Stresses:")
        element_stresses = self.element_structure.find_element_stress()
        for idx, item in enumerate(element_stresses):
            print(f"Element_{idx + 1} Stress: {item:.5E}")
