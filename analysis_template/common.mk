SCRIPT_DIR:=${HOME}/ccr_rates/ccr_scripts/ccr_scripts

# MD traj parameters
TRAJECTORY_PATH=${HOME}/bioinf/trj/ubq/tip4p-ew/NPT_bussi/bussi_box_8/5_run/
REFENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=2
FILETYPE:="dat"#type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
PATTERN:="run%05d"#pattern of MD run files: run00001.dat ---> "run%05d".dat

# model system parameters
N_RESIDUES:=76
VECTOR_1:=NH
VECTOR_2:=CA_HA
VECTORS:=${VECTOR_1},${VECTOR_2}

#fit parameters
FIT_LIMIT=20 #number of points (if None fit limit set automatically with moving average algorithm)

#crelaxation rates parametera
CCR_TYPE=DD-DD#type of ccr interaction DD-DD or DD-CSA
NMR_FREQ=500e6

