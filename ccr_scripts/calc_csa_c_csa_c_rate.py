from ccr_scripts.save_utils import calc_and_save_remote_ccr_rate
import argparse
import numpy as np

if __name__ == '__main__':

    gyromagnetic_ratio_dict = {"H1": 267.522e6,
                               "N15": -27.126e6,
                               "C13": 67.2828e6}


    parser = argparse.ArgumentParser(description='Calc DD-CSA C relaxation rate')
    parser.add_argument('--path-to-fit-dir', required=True, )
    parser.add_argument('--nmr-freq', required=True, type=float)
    parser.add_argument('--output-directory', default="./")

    args = parser.parse_args()

    B0 = args.nmr_freq / (gyromagnetic_ratio_dict["H1"] / 2 / np.pi)
    const = (gyromagnetic_ratio_dict["C13"] * 2 * B0 / 3) ** 2

    df_ccr_axis = calc_and_save_remote_ccr_rate(args.path_to_fit_dir, const, out_name="ccr.csv",
                                                output_directory=args.output_directory)
