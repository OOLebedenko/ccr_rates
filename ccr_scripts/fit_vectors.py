from ccr_scripts.process_utils.fit import bounds_scaled_fit_auto_correlation, estimate_acorr_fitting_limit
from pyxmolpp2 import PdbFile
from glob import glob
from tqdm import tqdm
import argparse
import numpy as np
import os
import pandas as pd


def fit_and_save_crosscorr_func(path_to_cross_corr_files,
                                bounds,
                                scales,
                                rname_list,
                                output_directory="./",
                                limit=None):
    def fit_one_corr_fucnc(corr, time, bounds, scales):
        corr_0 = corr[0]
        popt = bounds_scaled_fit_auto_correlation(time=time,
                                                  corr=corr / corr_0,
                                                  bounds=bounds,
                                                  scales=scales,
                                                  )
        popt[::2] = np.array(popt[::2]) * corr_0

        return popt

    path_to_ccr_csv_files = glob(os.path.join(path_to_cross_corr_files, "*.csv"))
    for bound in bounds:
        tau_table = pd.DataFrame()
        for cross_corr_file in tqdm(sorted(path_to_ccr_csv_files), desc=output_directory):
            df = pd.read_csv(cross_corr_file)[:100 * 1000]
            time_ns, crosscorr = df["time_ns"].values, df["crosscorr"].values

            if limit is None:
                limit = estimate_acorr_fitting_limit(data=crosscorr / crosscorr[0])

            popt = fit_one_corr_fucnc(crosscorr[:limit], time_ns[:limit], bound, scales)
            name = os.path.splitext(os.path.basename(cross_corr_file))[0]
            amplitudes = popt[::2]
            taus = popt[1::2]
            order = (len(bound[0]) + 1) // 2

            rid_1 = int(name.split("_")[0])
            rid_2 = int(name.split("_")[-1].split(".")[0])

            popt_dict = {
                'rId_1': rid_1, 'rName_1': rname_list[rid_1 - 1],
                'rId_2': rid_2, 'rName_2': rname_list[rid_2 - 1],
                'limit': limit
            }

            popt_dict.update(
                {("exp-%d-a%d" % (order, i + 1)): a for i, a in enumerate(amplitudes)}
            )
            popt_dict.update(
                {("exp-%d-tau%d" % (order, i + 1)): tau for i, tau in enumerate(taus)}
            )

            tau_table = pd.concat([tau_table, pd.DataFrame(popt_dict, index=[0])])

        tau_table.sort_values(by=['rId_1'], inplace=True)
        os.makedirs(output_directory, exist_ok=True)
        tau_table.to_csv(os.path.join(output_directory, 'tau_%d_exp.csv' % order), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fit crosscorr')
    parser.add_argument('--path-to-crosscorr-csv', required=True, )
    parser.add_argument('--limit', default=None, type=int)
    parser.add_argument('--path-to-reference-pdb')
    parser.add_argument('--output-directory', default="./")
    args = parser.parse_args()

    bounds = [
        ([[0, 1], [1, 10]]),
        ([[0, 0, 0, 1], [1, 0.1, 1, 10]]),
    ]

    scales = np.linspace(1, 3, 100)

    ref = PdbFile(args.path_to_reference_pdb).frames()[0]
    rname_list = [residue.name for residue in ref.residues]

    fit_and_save_crosscorr_func(args.path_to_crosscorr_csv,
                                bounds=bounds,
                                scales=scales,
                                rname_list=rname_list,
                                limit=args.limit,
                                output_directory=args.output_directory
                                )
