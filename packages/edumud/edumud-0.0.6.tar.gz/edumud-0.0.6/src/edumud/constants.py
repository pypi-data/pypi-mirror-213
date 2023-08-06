
import numpy as np

"""
physical constants for the edumud package.

Use:
    from edumud.constants import *
"""

EPS_WATER = 80.0
"""relative permittivity of water."""
EPS_ZERO = 8.85e-12
"""absolute permittivity of vacuum."""
EPS_ZW = EPS_ZERO * EPS_WATER  # often together
"""absolute permittivity of water EPS_ZERO* EPS_WATER."""
E_CHARGE = 1.6e-19             # elementary charge
"""elementary charge of an electron in Coulomb."""
BOLTZ_T = 1.38e-23 * 298       # Boltzmann constant x temperature
"""kT for T = 298 K."""
N_AVO = 6.0e23                 # Avogadro's number
"""Avogadro's Number (# particles in a mol)."""
ETA_VISC = 0.89e-3             # viscosity water
"""viscosity of water in SI units."""
TWOPI = 2.0 * np.pi
"""convenience constant for conversions from frequency to angular velocity."""
