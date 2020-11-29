from pyxmolpp2 import PdbFile, Trajectory, TrjtoolDatFile, GromacsXtcFile, AmberNetCDF
from tqdm import tqdm
import argparse
import functools
import operator
import os
from ccr_scripts.process_utils.select import get_CA_HA_selection, get_NH_selection, get_HA_HN_selection, \
    get_CO_selection, get_C_CA_selection, SelectionShifter
from ccr_scripts.process_utils.extract import WriteVectorsToCsv, Run


class XtcFileReaderWrapper:
    def __init__(self, n_frames):
        self.n_frames = n_frames

    def __call__(self, filename):
        return GromacsXtcFile(filename, self.n_frames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract vectors')
    parser.add_argument('--path-to-trajectory', required=True)
    parser.add_argument('--path-to-reference-pdb', required=True)
    parser.add_argument('--filetype', choices=["dat", "nc", "xtc"], required=True)
    parser.add_argument('--pattern', default="run%05d")
    parser.add_argument('--trajectory-length', required=True, type=int)
    parser.add_argument('--frames-per-trajectory-file', type=int, default=1000)
    parser.add_argument('--vectors')
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    trj_reader_dict = {"dat": TrjtoolDatFile,
                       "nc": AmberNetCDF,
                       "xtc": XtcFileReaderWrapper(args.frames_per_trajectory_file)}

    traj = Trajectory(PdbFile(args.path_to_reference_pdb).frames()[0])
    for ind in tqdm(range(1, args.trajectory_length + 1), desc="traj_reading"):
        fname = "{pattern}.{filetype}".format(pattern=args.pattern, filetype=args.filetype)
        traj.extend(trj_reader_dict[args.filetype](os.path.join(args.path_to_trajectory, fname % (ind))))

    selections_dict = {
        "CA_HA": get_CA_HA_selection,
        "NH": get_NH_selection,
        "HA_HN": get_HA_HN_selection,
        "CO": get_CO_selection,
        "C_CA": get_C_CA_selection,
        "HA_HNp1": SelectionShifter(select_func=get_HA_HN_selection, shift_ind=1)
    }

    extractors = []
    for vector_name in args.vectors.split(","):
        out_dir = os.path.join(args.output_directory, vector_name)
        os.makedirs(out_dir, exist_ok=True)
        extractors.append(WriteVectorsToCsv(selections_dict[vector_name], output_directory=out_dir))

    extract_vectors = functools.reduce(operator.or_, extractors)

    tqdm(traj) | extract_vectors | Run()
