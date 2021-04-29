#!/usr/bin/env python3
"""Tests based off of solution derived in class."""
import pathlib
import unittest

from src import elements


class InitTest(unittest.TestCase):
    def test_fake_input(self) -> None:
        fake_file = pathlib.Path("fake_file.txt")

        with self.assertRaises(FileNotFoundError):
            elements.Elements(fake_file)

    def test_str_input(self) -> None:
        fake_file = "fake_file.txt"

        with self.assertRaises(TypeError):
            elements.Elements(fake_file)

    def test_elements_construction(self) -> None:
        elements_txt = pathlib.Path("examples/problem1/elements.txt")
        results = {
            1: elements.Element(
                idx=1, node1=1, node2=2, e=1, a=1, stiffnes_matrix=None
            ),
            2: elements.Element(
                idx=2, node1=2, node2=3, e=1, a=1, stiffnes_matrix=None
            ),
            3: elements.Element(
                idx=3, node1=4, node2=3, e=1, a=1, stiffnes_matrix=None
            ),
            4: elements.Element(
                idx=4, node1=1, node2=4, e=1, a=1, stiffnes_matrix=None
            ),
            5: elements.Element(
                idx=5, node1=1, node2=3, e=1, a=1, stiffnes_matrix=None
            ),
            6: elements.Element(
                idx=6, node1=2, node2=4, e=1, a=1, stiffnes_matrix=None
            ),
        }

        element_structure = elements.Elements(elements_txt)
        self.assertEqual(results, element_structure.elements)


if __name__ == "__main__":
    unittest.main()
