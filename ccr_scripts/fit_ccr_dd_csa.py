from ccr_scripts.save_utils import fit_and_save_crosscorr_func
from pyxmolpp2 import PdbFile
import argparse
import os
import numpy as np

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

    for axis in ["x", "y", "z"]:

        path_to_crosscorr_csv = os.path.join(args.path_to_crosscorr_csv, axis)
        output_directory = os.path.join(args.output_directory, axis)
        os.makedirs(output_directory, exist_ok=True)

        fit_and_save_crosscorr_func(path_to_crosscorr_csv,
                                    bounds=bounds,
                                    scales=scales,
                                    rname_list=rname_list,
                                    limit=args.limit,
                                    output_directory=output_directory
                                    )
