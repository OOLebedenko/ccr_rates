import os
import argparse
from glob import glob
from ccr_scripts.save_utils import calc_and_save_crosscorr

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Calc DD-DD ccr func')
    parser.add_argument('--path-to-vect-csv-1', required=True)
    parser.add_argument('--path-to-vect-csv-2', required=True)
    parser.add_argument('--shift-ind', default=0)
    parser.add_argument('--dt-ns', default=0.001, type=float)
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    vectors_1_csv = glob(os.path.join(args.path_to_vect_csv_1, "*csv"))
    ccr_pairs_csv_files = []

    for path_to_v1 in sorted(vectors_1_csv):
        rid_1 = int(os.path.basename(path_to_v1).split("_")[0])
        path_to_v2 = glob(os.path.join(args.path_to_vect_csv_2, "{rid:02d}_*.csv".format(rid=rid_1 + args.shift_ind)))
        if path_to_v2:
            ccr_pairs_csv_files.append((path_to_v1, path_to_v2[0]))

    os.makedirs(args.output_directory, exist_ok=True)

    calc_and_save_crosscorr(ccr_pairs_csv_files, dt_ns=args.dt_ns,
                            out_dir=args.output_directory)
