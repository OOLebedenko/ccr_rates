import argparse
import pandas as pd
from ccr_scripts.save_utils import calc_and_save_crosscorr


def extract_pairvect_names_from_metadata(meta_vect_1, meta_vect_2, shift_ind):
    ccr_pairs_csv_files = []
    for rid_1 in meta_vect_1["rId_1"].unique():
        fnames_1 = meta_vect_1[meta_vect_1["rId_1"] == (rid_1)]["filename"]
        fnames_2 = meta_vect_2[meta_vect_2["rId_1"] == (rid_1 + shift_ind)]["filename"]
        if not fnames_2.empty:
            ccr_pairs_csv_files.append((fnames_1.values, fnames_2.values))
    return ccr_pairs_csv_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calc DD-DD ccr func')
    parser.add_argument('--path-to-metadata-vect-1', required=True)
    parser.add_argument('--path-to-metadata-vect-2', required=True)
    parser.add_argument('--shift-ind', default=0, type=int)
    parser.add_argument('--dt-ns', default=0.001, type=float)
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    ccr_pairs_csv_files = []
    meta_vect_1 = pd.read_csv(args.path_to_metadata_vect_1)
    meta_vect_2 = pd.read_csv(args.path_to_metadata_vect_2)

    calc_and_save_crosscorr(extract_pairvect_names_from_metadata(meta_vect_1, meta_vect_2, args.shift_ind),
                            dt_ns=args.dt_ns,
                            out_dir=args.output_directory)
