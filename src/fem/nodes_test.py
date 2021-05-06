#!/usr/bin/env python3
"""Tests based off of solution derived in class."""
import pathlib
import unittest

import numpy as np

from src.fem import nodes


class NodesInit(unittest.TestCase):
    def test_fake_input(self) -> None:
        fake_nodes_file = pathlib.Path("fake_nodes_file.txt")
        fake_disp_file = pathlib.Path("fake_disp_file.txt")

        with self.assertRaises(FileNotFoundError):
            nodes.Nodes(fake_nodes_file, fake_disp_file)

    def test_str_input(self) -> None:
        fake_nodes_file = "fake_nodes_file.txt"
        fake_disp_file = "fake_disp_file.txt"

        with self.assertRaises(TypeError):
            nodes.Nodes(fake_nodes_file, fake_disp_file)

    def test_node_construction(self) -> None:
        nodes_txt = pathlib.Path("examples/problem1/nodes.txt")
        disp_txt = pathlib.Path("examples/problem1/displacements.txt")
        results = {
            1: nodes.Node(global_idx=1.0, x=0.0, y=0.0, dx=0.0, dy=None),
            2: nodes.Node(global_idx=2.0, x=0.0, y=1.0, dx=0.0, dy=0.0),
            3: nodes.Node(global_idx=3.0, x=1.0, y=1.0, dx=None, dy=None),
            4: nodes.Node(global_idx=4.0, x=1.0, y=0.0, dx=None, dy=None),
        }

        node_structure = nodes.Nodes(nodes_txt, disp_txt)
        self.assertEqual(results, node_structure.nodes)

    def test_node_construction(self) -> None:
        nodes_txt = pathlib.Path("examples/problem1/nodes.txt")
        disp_txt = pathlib.Path("examples/problem1/displacements.txt")
        results = {
            1: nodes.Node(global_idx=1.0, x=0.0, y=0.0, dx=0.0, dy=None),
            2: nodes.Node(global_idx=2.0, x=0.0, y=1.0, dx=0.0, dy=0.0),
            3: nodes.Node(global_idx=3.0, x=1.0, y=1.0, dx=None, dy=None),
            4: nodes.Node(global_idx=4.0, x=1.0, y=0.0, dx=None, dy=None),
        }

        node_structure = nodes.Nodes(nodes_txt, disp_txt)
        self.assertTrue(
            np.array_equal(
                np.array([[0, 0, 0, 0, 0, 0, 0, 0,]]), node_structure.displacement_vec
            )
        )


if __name__ == "__main__":
    unittest.main()
