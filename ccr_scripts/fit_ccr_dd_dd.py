from pyxmolpp2 import PdbFile
import argparse
import numpy as np
from ccr_scripts.save_utils import fit_and_save_crosscorr_func

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
