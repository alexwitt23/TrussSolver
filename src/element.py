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


class Elements:
    def __init__(self, elements_file: pathlib.Path) -> None:
        assert elements_file.is_file(), f"Can't read {elements_file}."

        self.elements = {}

        # Read the elements files
        for idx, text in enumerate(elements_file.read_text().splitlines()):
            # The first line is the number of elements.
            if idx == 0:
                self.num_elements = int(text)
            else:
                # Strip the line of everything and just get the numbers
                self.elements[idx] = Element(
                    *[int(n) for n in text.split() if n.isdigit()]
                )

    def contruct_element_stiffness_matrices(self, node_structure: nodes.Nodes) -> None:
        """Take in the nodes list for the structure and create the element
        stiffness matrices."""
        self.node_structure = node_structure
        for idk, element in self.elements.items():
            # Get the x and y positions of this elements nodes.
            node1 = node_structure[element.node1]
            node2 = node_structure[element.node2]
            element_length = (
                (node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2
            ) ** 0.5

            cos = (node2.x - node1.x) / element_length
            sin = (node2.y - node1.y) / element_length
            constituent_angles = np.array([[cos, sin, -cos, -sin]])
            element.stiffnes_matrix = (
                (constituent_angles.transpose() * constituent_angles)
                * element.e
                * element.a
                / element_length
            )

            print(element.idx, element.stiffnes_matrix)

    def find_internal_forces(self):
        self.internal_forces = []
        for idk, element in self.elements.items():
            # Get the x and y positions of this elements nodes.
            node1 = self.node_structure[element.node1]
            node2 = self.node_structure[element.node2]

            element_length = (
                (node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2
            ) ** 0.5
            cos = (node2.x - node1.x) / element_length
            sin = (node2.y - node1.y) / element_length

            self.internal_forces.append(
                element.a * element.e * ((node2.dx - node1.dx) / element_length) * cos
                + ((node2.dy - node1.dy) / element_length) * sin
            )


if __name__ == "__main__":
    Elements(
        pathlib.Path(
            "/home/alex/Desktop/classes/S2021/COE321K/code/examples/elements.txt"
        )
    )
