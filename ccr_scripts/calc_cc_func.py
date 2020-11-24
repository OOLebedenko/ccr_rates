import os
import argparse
from glob import glob
from ccr_scripts.process_utils.calc_corrfunc import crosscorr_all_harmonics
from tqdm import tqdm
import pandas as pd
import numpy as np


if __name__ == '__main__':

    def calc_and_save_crosscorr(pairs_vectors_csv_files, dt_ns, out_dir="."):
        index = None
        for path_to_v1_file, path_to_v2_file in tqdm(pairs_vectors_csv_files):

            out_name = os.path.basename(path_to_v1_file).split("_")[0] + "_" + \
                       os.path.basename(path_to_v2_file).split("_")[0] + ".csv"
            vectors_1 = pd.read_csv(path_to_v1_file).values
            vectors_2 = pd.read_csv(path_to_v2_file).values
            cross_corr = crosscorr_all_harmonics(vectors_1, vectors_2)

            if index is None:
                index = len(cross_corr)

            os.makedirs(out_dir, exist_ok=True)
            pd.DataFrame({
                "time_ns": np.linspace(0, index * dt_ns, index, endpoint=False),
                "crosscorr": cross_corr
            }).to_csv(os.path.join(out_dir, out_name), index=False)


    parser = argparse.ArgumentParser(description='Extract vectors')
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
