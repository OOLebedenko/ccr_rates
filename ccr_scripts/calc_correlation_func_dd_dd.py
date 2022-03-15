import argparse
import pandas as pd
import os
from ccr_scripts.save_utils import calc_and_save_crosscorr, vector_name_to_basename


def extract_pairvect_names_from_metadata(meta_vect_1, meta_vect_2, shift_ind):
    ccr_pairs_csv_files = []
    for rid_1 in meta_vect_1["rId_1"].unique():
        fnames_1 = meta_vect_1[meta_vect_1["rId_1"] == (rid_1)]["filename"]
        fnames_2 = meta_vect_2[meta_vect_2["rId_1"] == (rid_1 + shift_ind)]["filename"]
        if not fnames_2.empty:
            ccr_pairs_csv_files.append((fnames_1.values, fnames_2.values))
    return ccr_pairs_csv_files


if __name__ == '__main__':
    rCAHA = 1.09  # angstrom
    rNH = 1.02  # angstrom

    bond_length_dict = {"N-H": rNH,
                        "CA-HA|HA2|HA3": rCAHA,
                        "H-HA|HA2|HA3": None
                        }

    parser = argparse.ArgumentParser(description='Calc DD-DD ccr func')
    parser.add_argument('--path-to-metadata', required=True)
    parser.add_argument('--dipole-1', required=True, choices=bond_length_dict.keys())
    parser.add_argument('--dipole-2', required=True, choices=bond_length_dict.keys())
    parser.add_argument('--shift-ind', default=0, type=int)
    parser.add_argument('--dt-ns', default=0.001, type=float)
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    ccr_pairs_csv_files = []
    meta_vect_1 = pd.read_csv(os.path.join(args.path_to_metadata, f"{vector_name_to_basename(args.dipole_1)}.csv"))
    meta_vect_2 = pd.read_csv(os.path.join(args.path_to_metadata, f"{vector_name_to_basename(args.dipole_2)}.csv"))

    calc_and_save_crosscorr(extract_pairvect_names_from_metadata(meta_vect_1, meta_vect_2, args.shift_ind),
                            dt_ns=args.dt_ns,
                            out_dir=args.output_directory)
