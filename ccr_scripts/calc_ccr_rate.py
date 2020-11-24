from ccr_scripts.process_utils.calc_relaxation_rate import calc_dipole_interaction_const, \
     calc_csa_axis_interaction_const, calc_remote_ccr_rates
import argparse
import os
import pandas as pd


def get_remote_ccr_rate(path_to_fit_dir, interaction_const, output_directory="./"):
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
    combined_df.to_csv(os.path.join(output_directory, "{rate}.csv".format(rate="ccr")), index=False)
    return combined_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fit crosscorr')
    parser.add_argument('--path-to-fit-dir', required=True, )
    parser.add_argument('--nmr-freq', required=True, type=float)
    parser.add_argument('--ccr-type', choices=["DD-DD", "DD-CSA"])
    parser.add_argument('--dipole-1', choices=["NH", "CAHA"], default=None)
    parser.add_argument('--dipole-2', choices=["NH", "CA_HA"], default=None)
    parser.add_argument('--csa-atoms', choices=["C"], default=None)
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

    dipole_dict = {"NH": [(gyromagnetic_ratio_dict["N15"], gyromagnetic_ratio_dict["H1"]), rNH],
                   "CA_HA": [(gyromagnetic_ratio_dict["C13"], gyromagnetic_ratio_dict["H1"]), rCAHA]}

    if args.ccr_type == "DD-DD":
        interaction_const = calc_dipole_interaction_const(dipole_dict[args.dipole_1][0][0],
                                                          dipole_dict[args.dipole_1][0][1],
                                                          dipole_dict[args.dipole_1][1])
        interaction_const *= calc_dipole_interaction_const(dipole_dict[args.dipole_2][0][0],
                                                           dipole_dict[args.dipole_2][0][1],
                                                           dipole_dict[args.dipole_2][1])

        get_remote_ccr_rate(args.path_to_fit_dir, interaction_const, output_directory=args.output_directory)

    if args.ccr_type == "DD-CSA":

        CSA_C = {"x": 244e-6,
                 "y": 178e-6,
                 "z": 90e-6}

        for axis in ["x", "y", "z"]:
            if args.dipole_1:
                interaction_const = calc_dipole_interaction_const(dipole_dict[args.dipole_1][0][0],
                                                                  dipole_dict[args.dipole_1][0][1],
                                                                  dipole_dict[args.dipole_1][1])
            elif args.dipole_2:
                interaction_const = calc_dipole_interaction_const(dipole_dict[args.dipole_2][0][0],
                                                                  dipole_dict[args.dipole_2][0][1],
                                                                  dipole_dict[args.dipole_2][1])
            interaction_const *= calc_csa_axis_interaction_const(gyromagnetic_ratio_dict["C13"], CSA_C[axis],
                                                                 args.nmr_freq)
            path_to_fit_dir = os.path.join(args.path_to_fit_dir, axis)
            get_remote_ccr_rate(path_to_fit_dir, interaction_const, out_name="ccr_{}.csv".format(axis),
                                output_directory=args.output_directory)
