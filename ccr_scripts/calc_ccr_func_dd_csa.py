import os
import argparse
import pandas as pd
import numpy as np
from glob import glob
from ccr_scripts.save_utils import calc_and_save_crosscorr


def extract_pairvect_names_from_metadata_csa(meta_vect, path_to_csa_dir, shift_ind):
    path_to_vect_csv_2 = glob(os.path.join(path_to_csa_dir, "x", "*.csv"))
    rids = [int(os.path.basename(path).split("_")[0]) for path in path_to_vect_csv_2]
    ccr_pairs_csv_files = []
    for rid in sorted(rids):
        fnames_1 = meta_vect[meta_vect["rId_1"] == (rid)]["filename"]
        if not fnames_1.empty:
            fnames_2 = [os.path.join(args.path_to_csa_dir, axis,
                        f"{rid + shift_ind:02d}_{axis}_axis.csv") for axis in ["x", "y", "z"]]
            ccr_pairs_csv_files.append((fnames_1.values, fnames_2))

    return ccr_pairs_csv_files


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Calc DD-CSA ccr func')
    parser.add_argument('--path-to-metadata-vect-1', required=True)
    parser.add_argument('--path-to-csa-dir', required=True)
    parser.add_argument('--shift-ind', default=0, type=int)
    parser.add_argument('--dt-ns', default=0.001, type=float)
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    CSA_C = [244e-6, 178e-6, 90e-6]

    meta_vect = pd.read_csv(args.path_to_metadata_vect_1)

    ccr_pairs_csv_files = extract_pairvect_names_from_metadata_csa(meta_vect, args.path_to_csa_dir, args.shift_ind)

    calc_and_save_crosscorr(ccr_pairs_csv_files,
                            weights=np.array(CSA_C * (len(ccr_pairs_csv_files) // 3)),
                            dt_ns=args.dt_ns,
                            out_dir=args.output_directory)
