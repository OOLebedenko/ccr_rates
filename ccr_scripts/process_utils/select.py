from pyxmolpp2 import Residue, AtomSelection, Frame, aName
from typing import Union, List


def has_atoms(atom_names):
    def predicate(residue: Residue):
        if set(atom_names).intersection(set([atom.name for atom in residue.atoms])):
            return True
        else:
            return False

    return predicate


def atom_pairs_from_consequent_residues(atom_names_1: Union[str, List[str]], atom_names_2: Union[str, List[str]]):
    if isinstance(atom_names_1, str):
        atom_names_1 = [atom_names_1]
    if isinstance(atom_names_2, str):
        atom_names_2 = [atom_names_2]

    def to_atoms(residue):
        if residue is not None:
            return residue.atoms
        return AtomSelection()

    def selector(frame: Frame):
        residues = frame.residues.filter(has_atoms(atom_names_1))

        return [
            (first_atom, second_atom)
            for res in residues[:-1]
            for first_atom in res.atoms.filter(aName.is_in(*atom_names_1))
            for second_atom in to_atoms(res.next).filter(aName.is_in(*atom_names_2))
        ]

    return selector


def atom_pairs_from_one_residue(atom_names_1: Union[str, List[str]], atom_names_2: Union[str, List[str]]):
    if isinstance(atom_names_1, str):
        atom_names_1 = [atom_names_1]
    if isinstance(atom_names_2, str):
        atom_names_2 = [atom_names_2]

    def selector(frame: Frame):
        residues = frame.residues.filter(has_atoms(atom_names_1))
        return [
            (first_atom, second_atom)
            for r in residues
            for first_atom in r.atoms.filter(aName.is_in(*atom_names_1))
            for second_atom in r.atoms.filter(aName.is_in(*atom_names_2))
        ]

    return selector
