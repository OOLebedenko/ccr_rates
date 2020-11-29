from typing import Sequence, Tuple, Callable
from pyxmolpp2 import Frame
from pyxmolpp2 import AtomSelection
from pyxmolpp2.pipe import TrajectoryProcessor

import os
import csv


class WriteVectorsToCsv(TrajectoryProcessor):

    def __init__(self,
                 vectors_selector: Callable[[Frame], Tuple[AtomSelection, AtomSelection]],
                 output_directory,
                 filename_format="{atom2.residue.id.serial:02d}_{atom2.name}.csv"):
        self.filename_format = filename_format
        self.output_directory = output_directory
        self.vector_selector = vectors_selector

        self._files = []
        self._csv_files = []
        self._sel_1 = None
        self._sel_2 = None

    def copy(self):
        raise RuntimeError("WriteVectorsToCsv can't be copied")

    def before_first_iteration(self, frame: Frame):
        assert self._sel_1 is None, "WriteVectorsToCsv can't be used twice in one pipeline"
        self._sel_1, self._sel_2 = self.vector_selector(frame)
        assert len(self._sel_1) == len(self._sel_2)
        for atom1, atom2 in zip(self._sel_1, self._sel_2):
            filename = self.filename_format.format(atom1=atom1, atom2=atom2)
            file = open(os.path.join(self.output_directory, filename), "w")
            csv_file = csv.writer(file)
            csv_file.writerow(["x", "y", "z"])
            self._files.append(file)
            self._csv_files.append(csv_file)

    def after_last_iteration(self, exc_type, exc_value, traceback) -> bool:

        for file in self._files:
            file.close()

        self._files = []
        self._csv_files = []
        self._sel_1 = None
        self._sel_2 = None

        return False

    def __call__(self, frame: Frame) -> Frame:
        vectors = self._sel_1.coords.values - self._sel_2.coords.values
        for csv_file, v in zip(self._csv_files, vectors):
            csv_file.writerow(v)
        return frame


class Run:
    def __ror__(self, trajectory: Sequence[Frame]):
        for _ in trajectory:
            pass
