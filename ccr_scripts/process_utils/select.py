from typing import Sequence, List, Union, Tuple
from pyxmolpp2 import Frame, AtomSelection, rId, aName, rName


def get_NH_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all backbone atom pairs of given frame.
    """
    return (frame.atoms.filter((rName != "PRO") & (aName == "N") & (rId > 1)),
            frame.atoms.filter((rName != "PRO") & (aName == "H") & (rId > 1)))


def get_CA_HA_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all backbone atom pairs of given frame.
    """
    return (frame.atoms.filter((aName == "CA") & (rId > 1)),
            frame.atoms.filter((aName == "HA") & (rId > 1) | (aName == "HA2")))


def get_HA_HN_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all HA and HN atom pairs of given frame.
    """
    return (frame.atoms.filter((rName != "PRO") & (aName == "HA") & (rId > 1) | (aName == "HA2")),
            frame.atoms.filter((rName != "PRO") & (aName == "H") & (rId > 1)))


def get_CO_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all HA and HN atom pairs of given frame.
    """
    return (frame.atoms.filter((aName == "C") & (rId > 1)),
            frame.atoms.filter((aName == "O") & (rId > 1)))


def get_C_CA_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all HA and HN atom pairs of given frame.
    """
    return (frame.atoms.filter((aName == "C") & (rId > 1)),
            frame.atoms.filter((aName == "CA") & (rId > 1)))


class SelectionShifter:
    def __init__(self, select_func, shift_ind):
        self.select_func = select_func
        self.shift_ind = shift_ind

    def __call__(self, frame: Frame):
        atoms_1, atoms_2 = self.select_func(frame)

        new_atoms_1 = []
        new_atoms_2 = []
        if len(atoms_1) != len(atoms_2):
            for atom_1 in atoms_1:
                for atom_2 in atoms_2:
                    if atom_2.residue.id.serial - atom_1.residue.id.serial == self.shift_ind:
                        new_atoms_1.append(atom_1)
                        new_atoms_2.append(atom_2)
        else:
            for atom_1, atom_2 in zip(atoms_1, atoms_2[self.shift_ind:]):
                if atom_2.residue.id.serial - atom_1.residue.id.serial == self.shift_ind:
                    new_atoms_1.append(atom_1)
                    new_atoms_2.append(atom_2)
        return AtomSelection(new_atoms_1), AtomSelection(new_atoms_2)


def get_HA_GLY_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all backbone atom pairs of given frame.
    """
    return (frame.atoms.filter((rName == "GLY") & (aName == "CA") & (rId > 1)),
            frame.atoms.filter((rId > 1) & (aName == "HA3")))


def get_HA_HN_GLY_selection(frame: Frame) -> Tuple[AtomSelection, AtomSelection]:
    """
    :param frame: Frame
    :return: tuple of all HA and HN atom pairs of given frame.
    """
    return (frame.atoms.filter((rName == "GLY") & (aName == "HA3")),
            frame.atoms.filter((rName != "PRO") & (aName == "H") & (rId > 1)))
