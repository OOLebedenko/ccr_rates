SCRIPT_DIR:=${HOME}/Projects/cross_relaxation_pyxmolpp2_v2/ccr_rates/ccr_scripts

## Protein parameters:
# specify number of residues
N_RESIDUES=76

## NMR parameters:
NMR_FREQ=500e6

## MD traj parameters
TRAJECTORY_PATH=${HOME}/Projects/cross_relaxation_pyxmolpp2_v2/ccr_rates/tests/example_xtc_trj_ubq_NPT_bussi_box_8
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=9
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=xtc
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d
#time pe frame (ns)
DT_NS=0.001

## Fit cross-correlation function parameters
#Length of fit in DT_NS units, e.g. FIT_LIMIT=5000 and DT_NS=0.001 correspond to 5 ns
FIT_LIMIT=5000

# specify all vectors that you need in all calculated CCRs
VECTOR_1=N-H_one_residue
VECTOR_2=CA-HA|HA2|HA3_one_residue
VECTOR_3=C-O_one_residue
VECTOR_4=C-CA_one_residue
VECTOR_5=HA|HA2|HA3-H_one_residue
VECTOR_6=HA|HA2|HA3-H_next_residue
VECTORS=${VECTOR_1},${VECTOR_2},${VECTOR_3},${VECTOR_4},${VECTOR_5},${VECTOR_6}
