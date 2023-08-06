"""
Unit tests for plots.py functions.
"""

import unittest
import matplotlib
import matplotlib.pyplot as plt
from radioactivedecay.plots import (
    _parse_nuclide_label,
    _parse_decay_mode_label,
    _check_fig_ax,
)


class Test(unittest.TestCase):
    """
    Unit tests for plots.py functions.
    """

    def test__parse_nuclide_label(self):
        """
        Test the parsing of nuclide strings for node labels.
        """

        self.assertEqual(_parse_nuclide_label("H-3"), "³H")
        self.assertEqual(_parse_nuclide_label("Be-7"), "⁷Be")
        self.assertEqual(_parse_nuclide_label("C-10"), "¹⁰C")
        self.assertEqual(_parse_nuclide_label("Ne-19"), "¹⁹Ne")
        self.assertEqual(_parse_nuclide_label("I-118"), "¹¹⁸I")
        self.assertEqual(_parse_nuclide_label("Pd-100"), "¹⁰⁰Pd")
        self.assertEqual(_parse_nuclide_label("Cl-34m"), "³⁴ᵐCl")
        self.assertEqual(_parse_nuclide_label("I-118m"), "¹¹⁸ᵐI")
        self.assertEqual(_parse_nuclide_label("Tb-156m"), "¹⁵⁶ᵐTb")
        self.assertEqual(_parse_nuclide_label("Tb-156n"), "¹⁵⁶ⁿTb")
        self.assertEqual(_parse_nuclide_label("SF"), "various")

    def test__parse_decay_mode_label(self):
        """
        Test the parsing of decay mode strings for edge labels.
        """

        self.assertEqual(_parse_decay_mode_label("α"), "α")
        self.assertEqual(_parse_decay_mode_label("β+"), "β⁺")
        self.assertEqual(_parse_decay_mode_label("β+ & EC"), "β⁺ & EC")
        self.assertEqual(_parse_decay_mode_label("β-"), "β⁻")
        self.assertEqual(_parse_decay_mode_label("EC"), "EC")
        self.assertEqual(_parse_decay_mode_label("IT"), "IT")
        self.assertEqual(_parse_decay_mode_label("SF"), "SF")

    def test__check_fig_ax(self):
        """
        Test the parsing of user-defined Matplotlib Figure and Axes objects.
        """

        fig_in, ax_in = plt.subplots()
        fig, ax = _check_fig_ax(fig_in, ax_in)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(ax, matplotlib.axes.Axes)

        fig, ax = _check_fig_ax(fig_in, None)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(ax, matplotlib.axes.Axes)

        fig, ax = _check_fig_ax(None, ax_in)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(ax, matplotlib.axes.Axes)

        fig, ax = _check_fig_ax(None, None)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(ax, matplotlib.axes.Axes)


if __name__ == "__main__":
    unittest.main()
