from ccr_scripts.process_utils.fit import bounds_scaled_fit_auto_correlation, estimate_acorr_fitting_limit
from ccr_scripts.process_utils.calc_corrfunc import crosscorr_all_harmonics
from ccr_scripts.process_utils.extract_pas import extract_csa_c_z_axis, extract_csa_c_y_axis, extract_csa_c_x_axis
from ccr_scripts.process_utils.calc_relaxation_rate import calc_remote_ccr_rates
from glob import glob
from tqdm import tqdm
import os
import pandas as pd
import numpy as np
from typing import Dict


def save_csa_c_pas(path_to_CO_vectors,
                   path_to_C_CA_vectors,
                   output_directory
                   ):
    CO_files = sorted(glob(os.path.join(path_to_CO_vectors, "*.csv")))
    C_CA_files = sorted(glob(os.path.join(path_to_C_CA_vectors, "*.csv")))
    assert len(CO_files) == len(C_CA_files)
    os.makedirs(output_directory, exist_ok=True)

    for axis in ["x", "y", "z"]:
        os.makedirs(os.path.join(output_directory, axis), exist_ok=True)

    for path_to_CO, path_to_C_CA in tqdm(zip(CO_files, C_CA_files)):
        r_id = os.path.basename(path_to_CO).split("_")[0]
        CO_vectors = pd.read_csv(path_to_CO).values
        C_CA_vectors = pd.read_csv(path_to_C_CA).values

        csa_c_z_axis = extract_csa_c_z_axis(CO_vectors, C_CA_vectors)
        csa_c_x_axis = extract_csa_c_x_axis(CO_vectors, csa_c_z_axis)
        csa_c_y_axis = extract_csa_c_y_axis(CO_vectors, csa_c_z_axis)
        for csa_axis, axis in zip([csa_c_x_axis, csa_c_y_axis, csa_c_z_axis], ["x", "y", "z"]):
            pd.DataFrame(csa_axis, columns=["x", "y", "z"]).to_csv(
                os.path.join(output_directory, axis, f"{r_id}_CSA_C.csv"), index=False)


def calc_crosscorr(path_to_v1_files,
                   path_to_v2_files,
                   weights=None,
                   bond_length_v1=None,
                   bond_length_v2=None
                   ):
    sum_ccr = []
    for path_to_v1_file in path_to_v1_files:
        for path_to_v2_file in path_to_v2_files:
            vectors_1 = pd.read_csv(path_to_v1_file).values
            vectors_2 = pd.read_csv(path_to_v2_file).values
            sum_ccr.append(crosscorr_all_harmonics(vectors_1, vectors_2, bond_length_v1, bond_length_v2))
    if weights is None:
        weights = np.ones(len(sum_ccr))
    cross_corr = [weight * ccr_func for weight, ccr_func in zip(weights, sum_ccr)]
    return np.array(cross_corr).sum(axis=0)


def calc_and_save_crosscorr(pairs_vectors_csv_files, dt_ns,
                            weights=None,
                            bond_length_v1=None,
                            bond_length_v2=None,
                            out_dir="."
                            ):
    index = None
    for path_to_v1_files, path_to_v2_files in tqdm(pairs_vectors_csv_files):

        cross_corr = calc_crosscorr(path_to_v1_files, path_to_v2_files,
                                    weights=weights,
                                    bond_length_v1=bond_length_v1,
                                    bond_length_v2=bond_length_v2
                                    )

        out_name = f"{os.path.splitext(os.path.basename(path_to_v1_files[0]))[0]}--{os.path.splitext(os.path.basename(path_to_v2_files[0]))[0]}.csv"

        if index is None:
            index = len(cross_corr)

        os.makedirs(out_dir, exist_ok=True)
        pd.DataFrame({
            "time_ns": np.linspace(0, index * dt_ns, index, endpoint=False),
            "crosscorr": cross_corr
        }).to_csv(os.path.join(out_dir, out_name), index=False)


def fit_and_save_crosscorr_func(path_to_cross_corr_files,
                                bounds,
                                scales,
                                residue_name_map: Dict[int, str],
                                output_directory="./",
                                limit=None
                                ):
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
        order = (len(bound[0]) + 1) // 2
        for cross_corr_file in tqdm(sorted(path_to_ccr_csv_files), desc=output_directory):
            name = os.path.splitext(os.path.basename(cross_corr_file))[0]
            df = pd.read_csv(cross_corr_file)[:100 * 1000]
            time_ns, crosscorr = df["time_ns"].values, df["crosscorr"].values

            if limit is None:
                fit_limit = estimate_acorr_fitting_limit(data=crosscorr / crosscorr[0])
            else:
                fit_limit = limit

            popt = fit_one_corr_fucnc(crosscorr[:fit_limit], time_ns[:fit_limit], bound, scales)
            amplitudes = popt[::2]
            taus = popt[1::2]

            vector_1, vector_2 = name.split("--")
            rid_1, rid_2 = int(vector_1.split("_")[0]), int(vector_2.split("_")[0])

            popt_dict = {
                'rId_1': rid_1, 'rName_1': residue_name_map[rid_1], "vect_1": vector_1,
                'rId_2': rid_2, 'rName_2': residue_name_map[rid_2], "vect_2": vector_2,
                'limit': fit_limit
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
        tau_table.to_csv(os.path.join(output_directory, f'tau_{order}_exp.csv'), index=False)


def calc_and_save_remote_ccr_rate(path_to_fit_dir,
                                  interaction_const,
                                  output_directory="./",
                                  out_name='ccr.csv'
                                  ):
    combined_df = pd.DataFrame()
    fits = ["tau_2_exp.csv"]
    for fit in fits:
        path_to_fit_csv = os.path.join(path_to_fit_dir, fit)
        fit_df = pd.read_csv(path_to_fit_csv)
        rate_table = pd.DataFrame()
        for ind, fit_line in fit_df.iterrows():
            amplitude = fit_line.filter(like='-a').values
            taus = fit_line.filter(like='-tau').values
            taus_s = taus * 1e-9
            rate = calc_remote_ccr_rates(interaction_const, amplitude, taus_s)
            D = {'rId_1': fit_line["rId_1"], 'rId_2': fit_line["rId_2"], "relaxation_rate": rate}
            rate_table = pd.concat([rate_table, pd.DataFrame(D, index=[0])])
        if combined_df.empty:
            combined_df = rate_table
        else:
            combined_df = pd.merge(combined_df, rate_table, left_index=False, right_index=False)
    os.makedirs(output_directory, exist_ok=True)
    combined_df.to_csv(os.path.join(output_directory, out_name), index=False)
    return combined_df


def vector_name_to_basename(vector_atom_names_str):
    a1, a2 = vector_atom_names_str.split("-")
    a1 = a1.split("|")[0]
    a2 = a2.split("|")[0]
    return f"{a1}-{a2}"
