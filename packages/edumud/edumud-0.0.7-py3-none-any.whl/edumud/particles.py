
# from impedance.classes.constants import *  # imports numpy as np
from edumud.file_utils import load_config


class Particle:
    def __init__(self, r, rz, eps, fi=None, hamaker=None):
        """

        Args:
            r:   radius of the colloidal particle (m)
            rz:  zeta potential in kT/e units (i.e. zeta = 25 * rel_zeta mV)
            eps: permittivity latex
            fi:  volume fraction of particles
        """
        self.radius = r
        self.rel_zeta = rz
        self.eps = eps
        self.fi = fi
        self.hamaker = hamaker
        self.beta = None  # = numpy array_like(omega)


    @classmethod
    def from_dict(cls, d):
        """ classmethod to enable constructing an instance from configuration file.
        """
        return cls(r=d["radius"], rz=d["rel_zeta"], eps=d["eps"], fi=d["fraction"], hamaker=d['Hamaker'])


def read_particles(yaml_file):
    """read particle species in colloidal system from yaml file

    Args:
        yaml_file (str):  configuration file name with .yaml extension

    Returns:
        (list): list of Particle objects

    """
    expc = load_config(yaml_file)
    part = expc['particles']        # list of dictionaries

    num_particles = len(part)
    print(f"Number of particle types: {num_particles}")
    assert(num_particles > 0)

    # make list of particles in colloid
    p_in_c = []
    [p_in_c.append(Particle(p['radius'], p['rel_zeta'], p['eps'], p['fraction'])) for p in part]

    return p_in_c


if __name__ == "__main__":
    from pathlib import Path
    DATADIR = Path(__file__).parent.parent.parent.absolute().joinpath("ImpedanceData")
    ps = read_particles(str(DATADIR / "poly.yaml"))
    print(ps[0])
