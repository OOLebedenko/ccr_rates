from ccr_scripts.process_utils.calc_relaxation_rate import calc_dipole_interaction_const
from ccr_scripts.save_utils import calc_and_save_remote_ccr_rate
import argparse
import numpy as np

if __name__ == '__main__':

    gyromagnetic_ratio_dict = {"H1": 267.522e6,
                               "N15": -27.126e6,
                               "C13": 67.2828e6}

    dipole_dict = {"N-H": [gyromagnetic_ratio_dict["N15"], gyromagnetic_ratio_dict["H1"]],
                   "CA-HA|HA2|HA3": [gyromagnetic_ratio_dict["C13"], gyromagnetic_ratio_dict["H1"]]}

    parser = argparse.ArgumentParser(description='Calc DD-CSA C relaxation rate')
    parser.add_argument('--path-to-fit-dir', required=True, )
    parser.add_argument('--nmr-freq', required=True, type=float)
    parser.add_argument('--dipole-1', choices=dipole_dict.keys(), default=None)
    parser.add_argument('--output-directory', default="./")

    args = parser.parse_args()

    interaction_const = calc_dipole_interaction_const(*dipole_dict[args.dipole_1])
    B0 = args.nmr_freq / (gyromagnetic_ratio_dict["H1"] / 2 / np.pi)
    const = gyromagnetic_ratio_dict["C13"] * 2 * B0 * interaction_const / 3

    df_ccr_axis = calc_and_save_remote_ccr_rate(args.path_to_fit_dir, const, out_name="ccr.csv",
                                                output_directory=args.output_directory)
