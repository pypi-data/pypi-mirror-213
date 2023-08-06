
# import numpy as np

from edumud.constants import *  # imports numpy as np


class Cell:
    """class for general electrolysis cell.

    """
    def __init__(self, cc: float):
        """

        Args:
            cc: cell constant in m^-1
        """
        self.cell_constant = cc


class PlanarCell(Cell):
    """class for electrolysis cell with planar electrodes.

    """
    def __init__(self, cc: float, d: float):
        """

        Args:
            cc: cell constant electrode_distance/electrode surface in m^-1
            d: electrode distance in m
        """
        super().__init__(cc)
        # self.cell_constant = cc
        self.el_dist = d
        self.surface = d/cc


class CylindricalCell(Cell):
    """class for electrolysis cell with cylindrical electrodes.

    """
    def __init__(self, h: float, r_inner: float, r_outer):
        """Note: cell constant 1/(2*pi*h) surface in m^-1 in constructor of parent class "Cell".

        Args:
            h: height of cell
            r_inner: radius of cell
            r_outer: radius of cell
        """
        super().__init__(cc=np.reciprocal(2.0*np.pi*h))
        self.inner_radius = r_inner
        self.outer_radius = r_outer
        self.height = h

        self.log_ratio_radii = np.log(self.outer_radius/self.inner_radius)
        self.one_over_inner_plus_one_over_outer = np.reciprocal(self.inner_radius) + np.reciprocal(self.outer_radius)


if __name__ == "__main__":
    Cell_1 = PlanarCell(cc=12.5, d=4.0e-3)
