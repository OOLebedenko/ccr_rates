SCRIPT_DIR:=${HOME}/ccr_rates/ccr_scripts/

## MD traj parameters
TRAJECTORY_PATH=${HOME}/bioinf/trj/ubq/tip4p-ew/NPT_bussi/bussi_box_8/5_run/
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=2
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=dat
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d

## Model system parameters
N_RESIDUES:=76
VECTOR_1:=NH
VECTOR_2:=CA_HA

## Fit parameters
# Number of points (if None fit limit set automatically with moving average algorithm)
FIT_LIMIT=20
