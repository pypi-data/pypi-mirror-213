
from edumud.constants import *  # imports numpy as np
from edumud.file_utils import load_config


class Electrolyte:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.C_salt = None
        self.diff_plus = None
        self.z_plus = None
        self.nu_plus = None
        self.diff_minus = None
        self.z_minus = None
        self.nu_minus = None
        self.kappa_zero2 = None
        self.kappa2 = None
        self.kappa = None
        self.D_zero = None
        self.K1 = None
        self.lambda_c2 = None
        self.lambda_n2 = None
        self.read(self.config_file)

    def calc_kappa(self):
        """calculation of kappa_zero^2
           calculation of kappa (inverse of Debije length) and kappa^2.

        """
        # calculate kappa2 / kappa: inverse of the Debye length (squared)
        self.kappa_zero2 = np.square(E_CHARGE) * self.C_salt * N_AVO
        self.kappa_zero2 /= EPS_ZW * BOLTZ_T
        kappa2 = self.kappa_zero2 * (self.nu_plus * np.square(self.z_plus) + self.nu_minus * np.square(self.z_minus))
        self.kappa2 = kappa2
        self.kappa = np.sqrt(kappa2)  # inverse of the Debije length

    def calc_D_zero(self):
        """calculate parameter D0.

        """
        self.D_zero = np.reciprocal((self.z_plus - self.z_minus) /
                                    (self.z_plus * self.diff_plus - self.z_minus * self.diff_minus))

    def calc_K1(self):
        """calculate limiting conductivity value K1.

        """
        self.K1 = EPS_ZW * self.kappa2 * self.D_zero  # limiting conductivity value

    def read(self, yaml_file: str):
        """read elektrolyte ionic species from yaml file.

        Args:
            yaml_file (str):  configuration file name with .yaml extension

        """
        expc = load_config(yaml_file)

        self.C_salt = expc['electrolyte'][0]['conc']

        self.diff_plus = expc['electrolyte'][0]['ions'][0]['D']  # ionic diff. coeff. for ion 1 ("+" ion)in m^2/s
        self.z_plus = expc['electrolyte'][0]['ions'][0]['z']  # valence ion 1 ("+" ion)
        self.nu_plus = expc['electrolyte'][0]['ions'][0]['nu']  # stoechiometric coef. ion 1 ("+" ion)

        self.diff_minus = expc['electrolyte'][0]['ions'][1]['D']  # ionic diff. coeff. for ion 2 ("-" ion)in m^2/s
        self.z_minus = expc['electrolyte'][0]['ions'][1]['z']  # valence ion 2 ("-" ion)
        self.nu_minus = expc['electrolyte'][0]['ions'][1]['nu']  # stoechiometric coef. ion 2 ("-" ion)

        neutrality = self.z_plus * self.nu_plus + self.z_minus * self.nu_minus
        print(f"Electroneutrality: {neutrality} (check if equals 0)")

        self.calc_kappa()
        self.calc_D_zero()
        self.calc_K1()           # limiting conductivity value


if __name__ == "__main__":
    from pathlib import Path
    DATADIR = Path(__file__).parent.parent.parent.absolute().joinpath("ImpedanceData")

    e = Electrolyte(str(DATADIR / "Cell_1_KCl_1mM.yaml"))
    print(f"kappa^2: {e.kappa2}")
