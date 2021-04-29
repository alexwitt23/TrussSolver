import dataclasses
import pathlib

import numpy as np

from src import nodes


@dataclasses.dataclass
class Element:
    idx: int
    node1: int
    node2: int
    e: int
    a: int
    stiffnes_matrix: np.ndarray = None
    length: float = None


class Elements:
    def __init__(self, elements_file: pathlib.Path) -> None:
        self.node_structure = None
        if not isinstance(elements_file, pathlib.Path):
            raise TypeError(f"{elements_file} must be a `pathlib.Path`.")

        if not elements_file.is_file():
            raise FileNotFoundError(f"Can't read {elements_file}.")

        self.elements = {}

        # Read the elements files
        for idx, text in enumerate(elements_file.read_text().splitlines()):
            # The first line is the number of elements.
            if idx == 0:
                self.num_elements = int(text)
            else:
                # Strip the line of everything and just get the numbers
                self.elements[idx] = Element(*[float(n) for n in text.split()])

    def contruct_element_stiffness_matrices(self, node_structure: nodes.Nodes) -> None:
        """Take in the nodes list for the structure and create the element
        stiffness matrices."""
        self.node_structure = node_structure
        for element in self.elements.values():
            # Get the x and y positions of this elements nodes.
            node1 = node_structure[element.node1]
            node2 = node_structure[element.node2]

            k_local = np.zeros((6, 6))
            k_local[0, 0] = 1
            k_local[3, 0] = -1
            k_local[0, 3] = -1
            k_local[3, 3] = 1

            # Form rotation matrix

            element_length = (
                (node1.x - node2.x) ** 2
                + (node1.y - node2.y) ** 2
                + (node1.z - node2.z) ** 2
            ) ** 0.5
            theta1x = (node2.x - node1.x) / element_length
            theta1y = (node2.y - node1.y) / element_length
            theta1z = (node2.z - node1.z) / element_length

            rotation = np.zeros((6, 6))
            rotation[0, 0] = theta1x
            rotation[0, 1] = theta1y
            rotation[0, 2] = theta1z
            rotation[3, 3] = theta1x
            rotation[3, 4] = theta1y
            rotation[3, 5] = theta1z

            element.stiffnes_matrix = (
                np.matmul(np.matmul(rotation.transpose(), k_local), rotation)
                * element.e
                * element.a
                / element_length
            )
            element.length = element_length

    def find_internal_forces(self):
        self.internal_forces = []
        for idk, element in self.elements.items():
            # Get the x and y positions of this elements nodes.
            node1 = self.node_structure[element.node1]
            node2 = self.node_structure[element.node2]

            element_length = element.length
            theta1x = (node2.x - node1.x) / element_length
            theta1y = (node2.y - node1.y) / element_length
            theta1z = (node2.z - node1.z) / element_length
            eps = (
                ((node2.dx - node1.dx) / element_length) * theta1x
                + ((node2.dy - node1.dy) / element_length) * theta1y
                + ((node2.dy - node1.dy) / element_length) * theta1z
            )
            self.internal_forces.append(element.a * element.e * eps)

    def find_element_strain(self):
        self.element_strains = []
        for idk, element in self.elements.items():
            # Get the x and y positions of this elements nodes.
            node1 = self.node_structure[element.node1]
            node2 = self.node_structure[element.node2]

            element_length = element.length
            element_length_new = (
                (node1.x - node2.x + node1.dx - node2.dx) ** 2
                + (node1.y - node2.y + node1.dy - node2.dy) ** 2
                + (node1.z - node2.z + node1.dz - node2.dz) ** 2
            ) ** 0.5

            self.element_strains.append(
                (element_length_new - element_length) / element_length
            )
        return self.element_strains

    def find_element_stress(self):
        self.element_stress = []
        for force, element in zip(self.internal_forces, self.elements.values()):
            self.element_stress.append(force / element.a)

        return self.element_stress
