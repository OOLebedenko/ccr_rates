from ccr_scripts.process_utils.calc_relaxation_rate import calc_dipole_interaction_const, \
    calc_csa_axis_interaction_const
from ccr_scripts.save_utils import calc_and_save_remote_ccr_rate
import argparse
import os
import numpy as np
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fit crosscorr')
    parser.add_argument('--path-to-fit-dir', required=True, )
    parser.add_argument('--nmr-freq', required=True, type=float)
    parser.add_argument('--dipole-1', choices=["NH", "CA_HA"], default=None)
    parser.add_argument('--output-directory', default="./")

    args = parser.parse_args()

    rCAHA = 1.09e-10
    rNH = 1.02e-10
    gyromagnetic_ratio_dict = {"H1": 267.522e6,
                               "N15": -27.126e6,
                               "C13": 67.2828e6}

    CSA_C = {"x": 244e-6,
             "y": 178e-6,
             "z": 90e-6}

    dipole_dict = {"NH": [gyromagnetic_ratio_dict["N15"], gyromagnetic_ratio_dict["H1"], rNH],
                   "CA_HA": [gyromagnetic_ratio_dict["C13"], gyromagnetic_ratio_dict["H1"], rCAHA]}
    
    full_ccr = []
    for axis in ["x", "y", "z"]:
        interaction_const = calc_dipole_interaction_const(*dipole_dict[args.dipole_1])
        interaction_const *= calc_csa_axis_interaction_const(gyromagnetic_ratio_dict["C13"], CSA_C[axis],
                                                             args.nmr_freq)
        path_to_fit_dir = os.path.join(args.path_to_fit_dir, axis)
        df_ccr_axis = calc_and_save_remote_ccr_rate(path_to_fit_dir, interaction_const, out_name="ccr_{}.csv".format(axis),
                                      output_directory=args.output_directory)
        rid_1, rid_2, ccr_rate  = df_ccr_axis.rId_1.values, df_ccr_axis.rId_2.values, df_ccr_axis.relaxation_rate.values
        full_ccr.append(ccr_rate)


    pd.DataFrame({"relaxation_rate": np.array(full_ccr).sum(axis=0), "rId_1" : rid_1, "rId_2": rid_2}).to_csv(os.path.join(args.output_directory, "ccr.csv"), index=False)