import dataclasses
import pathlib

import numpy as np


@dataclasses.dataclass
class Force:
    node_idx: int
    x_component: float = None
    y_component: float = None
    moment_component: float = None


class Forces:
    def __init__(self, forces_file: pathlib.Path, num_nodes: int) -> None:
        assert forces_file.is_file(), f"Can't read {forces_file}."

        self.forces = {}

        # Read the elements files
        for idx, text in enumerate(forces_file.read_text().splitlines()):
            # The first line is the number of elements.
            if idx == 0:
                self.num_forces = int(idx)
            else:
                items = [float(n) for n in text.split()]

                # X-direction
                if items[1] == 1:
                    self.forces[idx] = Force(items[0], x_component=items[2])
                # Y-direction
                elif items[1] == 2:
                    self.forces[idx] = Force(items[0], y_component=items[2])
                # Moment
                elif items[1] == 3:
                    self.forces[idx] = Force(items[0], z_component=items[2])

        self.force_vec = np.zeros((1, 3 * num_nodes))
        for force in self.forces.values():
            idx = (force.node_idx - 1) * 3

            if force.x_component is not None:
                self.force_vec[0, int(idx)] = force.x_component
            if force.y_component is not None:
                self.force_vec[0, int(idx) + 1] = force.y_component
            if force.moment_component is not None:
                self.force_vec[0, int(idx) + 2] = force.moment_component
