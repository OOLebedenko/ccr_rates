SCRIPT_DIR:=${HOME}/ccr_rates/ccr_scripts/to_send/ccr_rates/ccr_scripts/

## MD traj parameters
TRAJECTORY_PATH=../../example_xtc_trj_ubq_NPT_bussi_box_8/
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=9
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=dat
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d

## Model system parameters
N_RESIDUES:=76
VECTOR_1:=NH
VECTOR_2:=CA_HA
#shift parameter corresponds to the same residue SHIFT=0 (CAHA_NH) or the next SHIFT=1 (CAHA_Np1Hp1)
SHIFT=0
#time pe frame (ns)
DT_NS=0.001

## Fit parameters
# Length of fit in ps (DT_NS * FIT_LIMIT) for example 5000 * 0.001 = 5 ns 
FIT_LIMIT=5000
