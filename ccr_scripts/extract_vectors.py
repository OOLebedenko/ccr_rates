from ccr_scripts.process_utils.select import atom_pairs_from_one_residue, atom_pairs_from_consequent_residues
from ccr_scripts.save_utils import vector_name_to_basename
from pyxmolpp2 import Trajectory, PdbFile, Atom, TrjtoolDatFile, GromacsXtcFile, AmberNetCDF
from pyxmolpp2.pipe import WriteVectorsToCsv, Run
from tqdm import tqdm
import argparse
import functools
import operator
import os
import csv

class XtcFileReaderWrapper:
    def __init__(self, n_frames):
        self.n_frames = n_frames

    def __call__(self, filename):
        return GromacsXtcFile(filename, self.n_frames)

class WriteVectorsToCsvWithMetadata(WriteVectorsToCsv):
    headers = ["rId_1", "aName_1", "rId_2", "aName_2", "filename"]

    def __init__(self, pair_selector, filename_provider: 'OutputFilenameFormatter', meta_filename):
        self.selector = pair_selector
        self.filename_provider = filename_provider
        self.meta_filename = meta_filename
        super().__init__(pair_selector=pair_selector, filename_provider=filename_provider)

    def before_first_iteration(self, frame):
        atom_pairs = self.selector(frame)
        out_dirname = os.path.dirname(self.meta_filename)
        if out_dirname:
            os.makedirs(out_dirname, exist_ok=True)
        with open(os.path.join(self.meta_filename), "w") as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            for a1, a2 in atom_pairs:
                writer.writerow([a1.residue.id, a1.name, a2.residue.id, a2.name, self.filename_provider(a1, a2)])
        super().before_first_iteration(frame)


class OutputFilenameFormatter:
    def __init__(self, output_directory):
        self.output_directory = output_directory

    def __call__(self, atom1: Atom, atom2: Atom):
        os.makedirs(self.output_directory, exist_ok=True)
        return f"{self.output_directory}/" \
               f"{atom1.residue.id.serial:02d}_{atom1.name}-" \
               f"{atom2.residue.id.serial:02d}_{atom2.name}" \
               f".csv"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract vectors')
    parser.add_argument('--path-to-trajectory', required=True)
    parser.add_argument('--path-to-reference-pdb', required=True)
    parser.add_argument('--filetype', choices=["dat", "nc", "xtc"], required=True)
    parser.add_argument('--pattern', default="run%05d")
    parser.add_argument('--trajectory-length', required=True, type=int)
    parser.add_argument('--frames-per-trajectory-file', type=int, default=1000)
    parser.add_argument('--vectors', required=True)
    parser.add_argument('--output-directory', default=".")
    args = parser.parse_args()

    trj_reader_dict = {"dat": TrjtoolDatFile,
                       "nc": AmberNetCDF,
                       "xtc":  XtcFileReaderWrapper(args.frames_per_trajectory_file)}

    traj = Trajectory(PdbFile(args.path_to_reference_pdb).frames()[0])
    for ind in tqdm(range(1, args.trajectory_length + 1), desc="traj_reading"):
        fname = "{pattern}.{filetype}".format(pattern=args.pattern, filetype=args.filetype)
        traj.extend(trj_reader_dict[args.filetype](os.path.join(args.path_to_trajectory, fname % (ind))))

    processes = []
    for vector in args.vectors.split(","):
        atom_1, atom_2 = vector.split("-")
        subdir = vector_name_to_basename(vector)
        processes.append(
            WriteVectorsToCsvWithMetadata(
                atom_pairs_from_one_residue(atom_1.split("|"), atom_2.split("|")),
                OutputFilenameFormatter(os.path.join(args.output_directory, subdir)),
                meta_filename=f"{os.path.join(args.output_directory)}/{subdir}.csv"
            )
        )

    test = functools.reduce(operator.or_, processes)
    tqdm(traj) | test | Run()
