from edumud.constants import *  # imports numpy
# from impedance.poly.polyutils_oo import complex_perm_full
from edumud.cells import Cell, PlanarCell, CylindricalCell
from edumud.electrolytes import Electrolyte


# from impedance.classes.particles import Particle, read_particles


class Colloid:
    def __init__(self, c: Cell, e: Electrolyte, part: list = None):
        self.c = c
        self.e = e
        self.part = part
        self.Cpol = None
        self.C0 = None
        self.R0 = None
        self.Rseries = None
        self.Lseries = None
        self.Z0 = None
        self.Zeq = None
        self.Keq = None
        self.EPSeq = None
        self.omega_p = None
        self.omega_c = None
        self.omega_zero = None
        self.omega_h = None

    def calc_eq_circuit(self, Rseries=0.0, Lseries=0.0):
        if isinstance(self.c, PlanarCell):
            self.Cpol = EPS_ZW * self.e.kappa * self.c.el_dist / 2.0
            self.C0 = EPS_ZW
            self.R0 = np.reciprocal(self.e.K1)
        elif isinstance(self.c, CylindricalCell):
            self.Cpol = 2.0 * np.pi * self.c.height * EPS_ZW * self.e.kappa
            self.Cpol /= self.c.one_over_inner_plus_one_over_outer

            self.C0 = 2.0 * np.pi * self.c.height * EPS_ZW
            self.C0 /= self.c.log_ratio_radii

            self.R0 = np.reciprocal(2.0 * np.pi * self.c.height)
            self.R0 *= self.c.log_ratio_radii
            self.R0 /= self.e.K1
        else:
            print("calculation of Cpol, C) and R0 not implemented for this type of cell")
        self.Rseries = Rseries  # Ohm
        self.Lseries = Lseries  # nH

        print(f"C_p = {self.Cpol * 1e6:.4g} microF")
        print(f"C_0 = {self.C0 * 1e12:.4g} pF")
        print(f"R_0 = {self.R0 / 1e3:.4g} kOhm")
        print(f"L_series = {self.Lseries * 1e9:.4g} nH")
        print(f"R_series = {self.Rseries:.4g} Ohm")

    def calc_impedance_from_eq_circuit(self, omega):
        if self.C0 is not None:
            self.Z0 = np.reciprocal(1.0 / self.R0 + 1j*self.C0*omega)  # adapt
            self.Zeq = self.Z0 + 1.0 / (1j*self.Cpol*omega)
            # multiply eq circuit with cell constant
            self.Zeq = self.Zeq * self.c.cell_constant
            # add Rseries and Lseries (they do not depend on cell constant!)
            self.Zeq += 1j * self.Lseries * omega + self.Rseries
            self.Keq = np.real(1.0 / self.Zeq)
            self.EPSeq = np.imag(1.0 / self.Zeq) / (EPS_ZERO * omega)

    def calc_omegas(self):
        """calculation of omega_p and omega_zero

        """
        if isinstance(self.c, PlanarCell):
            self.omega_p = 2.0 * self.e.D_zero * self.e.kappa / self.c.el_dist  # ang. vel. (rad/s) associated to cell
            print(f"omega_p = 2*kappa*D/L for omega = {self.omega_p:.3g} rad/s ({self.omega_p / (2 * np.pi):.3g} Hz)")
        elif isinstance(self.c, CylindricalCell):
            self.omega_c = self.e.D_zero * self.e.kappa
            self.omega_c *= self.c.one_over_inner_plus_one_over_outer  # ang. vel. (rad/s) associated to cyl. cell
            print(f"omega_c = {self.omega_c:.3g} rad/s ({self.omega_c / (2 * np.pi):.3g} Hz)")
            self.omega_h = self.e.kappa**3 * self.e.D_zero * self.c.one_over_inner_plus_one_over_outer
            print(f"omega_h = {self.omega_h:.3g} rad/s ({self.omega_h / (2 * np.pi):.3g} Hz)")
        else:
            print("calculation of omega_p not implemented for this type of cell")

        self.omega_zero = self.e.kappa2 * self.e.D_zero  # ang. vel. (rad/s) associated to Debye relaxation
        print(f"omega_0 = kappa^2 * D for omega = {self.omega_zero:.3g} rad/s ({self.omega_zero / (2 * np.pi):.3g} Hz)")


if __name__ == "__main__":
    from pathlib import Path

    DATADIR = Path(__file__).parent.parent.parent.absolute().joinpath("ImpedanceData")

    Cell_1 = PlanarCell(cc=12.5, d=4.0e-3)
    el = Electrolyte(str(DATADIR / "Cell_1_KCl_1mM.yaml"))
    # print(f"kappa^2: {e.kappa2}")
    system = Colloid(Cell_1, el)
    system.calc_omegas()
    system.calc_eq_circuit()

    w = np.logspace(1, 9, 500)
    freq = w / TWOPI
    system.calc_impedance_from_eq_circuit(w)

    # theoretical calculation for Z_e
    K_e, EPS_e, *_ = complex_perm_full(w, el, Cell_1)
