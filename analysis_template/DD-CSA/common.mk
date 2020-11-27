SCRIPT_DIR:=${HOME}/ccr_rates/ccr_scripts/

## MD traj parameters
TRAJECTORY_PATH=${HOME}/bioinf/trj/ubq/tip4p-ew/NPT_bussi/bussi_box_8/5_run/
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=9
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=dat
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d

## Model system parameters
N_RESIDUES:=76
VECTOR_1:=NH
#other vectors -- C CSA axis
#shift parameter corresponds to the same residue SHIFT=0 (CAHA_C) or the next SHIFT=-1 (CAHA_Cm1)
SHIFT=0
#time pe frame (ns)
DT_NS=0.001

## Fit parameters
# Length of fit in ps (DT_NS * FIT_LIMIT) for example 5000 * 0.001 = 5 ns 
FIT_LIMIT=5000

## CCR parameters:
NMR_FREQ=500e6

