from pyxmolpp2 import Frame
from pyxmolpp2.pipe import TrajectoryProcessor


class ScaleBonds(TrajectoryProcessor):

    def __init__(self, pair_selector, bond_length):
        self.pair_selector = pair_selector
        self.bond_length = bond_length
        self.pair_vector = None

    def before_first_iteration(self, frame: Frame):
        self.pair_vector = self.pair_selector(frame)

    def __call__(self, frame: Frame):
        for atom1, atom2 in self.pair_vector:
            current_vector = atom2.r - atom1.r
            rescaled_vector = current_vector * (self.bond_length / current_vector.len())
            atom2.r = rescaled_vector + atom1.r
        return frame
