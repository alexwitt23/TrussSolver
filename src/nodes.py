import dataclasses
import pathlib

import numpy as np


@dataclasses.dataclass
class Node:
    global_idx: int
    x: float
    y: float
    dx: float = None
    dy: float = None


class Nodes:
    def __init__(
        self, nodes_file: pathlib.Path, displacements_file: pathlib.Path
    ) -> None:
        if not isinstance(nodes_file, pathlib.Path):
            raise TypeError(f"{nodes_file} must be a pathlib.Path.")
        if not isinstance(displacements_file, pathlib.Path):
            raise TypeError(f"{displacements_file} must be a pathlib.Path.")
        if not nodes_file.is_file():
            raise FileNotFoundError(f"Can't read {nodes_file}.")
        if not displacements_file.is_file():
            raise FileNotFoundError(f"Can't read {displacements_file}.")

        # This dictionary will hold keys of global node ids and the values
        # are the corresponding nodes.
        self.nodes = {}

        # Read the nodes files
        for idx, text in enumerate(nodes_file.read_text().splitlines()):
            # The first line is the number of nodes.
            if idx == 0:
                self.num_nodes = int(text)
            else:
                # Strip the line of everything and just get the numbers
                self.nodes[idx] = Node(*[float(n) for n in text.split()])

        # Process the displacement information
        for idx, text in enumerate(displacements_file.read_text().splitlines()):

            # The first line is the number of known displacements.
            if idx == 0:
                continue
    
            data = [float(n) for n in text.split()]
            
            # Displacement in x direction
            if data[1] == 1:
                self.nodes[data[0]].dx = data[2]
            elif data[1] == 2:
                self.nodes[data[0]].dy = data[2]
            else:
                raise ValueError("Unsported direction in displacements file.")

        # Create the displacement vector
        self.displacement_vec = np.zeros((1, 2 * len(self.nodes)))
        for node in self.nodes.values():
            x = int((node.global_idx - 1) * 2)
            if node.dx is not None:
                self.displacement_vec[0, x] = node.dx
            if node.dy is not None:
                self.displacement_vec[0, x + 1] = node.dy

    def get_nodes(self):
        return self.nodes
