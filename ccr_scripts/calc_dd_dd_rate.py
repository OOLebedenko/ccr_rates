from ccr_scripts.process_utils.calc_relaxation_rate import calc_dipole_interaction_const
from ccr_scripts.save_utils import calc_and_save_remote_ccr_rate
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calc DD-DD relaxation rate')
    parser.add_argument('--path-to-fit-dir', required=True, )
    parser.add_argument('--dipole-1', choices=["N_H", "CA_HA/HA2/HA3"], default=None)
    parser.add_argument('--dipole-2', choices=["N_H", "CA_HA/HA2/HA3"], default=None)
    parser.add_argument('--output-directory', default="./")

    args = parser.parse_args()

    rCAHA = 1.09e-10
    rNH = 1.02e-10
    gyromagnetic_ratio_dict = {"H1": 267.522e6,
                               "N15": -27.126e6,
                               "C13": 67.2828e6}

    dipole_dict = {"N_H": [gyromagnetic_ratio_dict["N15"], gyromagnetic_ratio_dict["H1"], rNH],
                   "CA_HA/HA2/HA3": [gyromagnetic_ratio_dict["C13"], gyromagnetic_ratio_dict["H1"], rCAHA]}

    interaction_const = calc_dipole_interaction_const(*dipole_dict[args.dipole_1])
    interaction_const *= calc_dipole_interaction_const(*dipole_dict[args.dipole_2])

    calc_and_save_remote_ccr_rate(args.path_to_fit_dir, interaction_const, output_directory=args.output_directory)
