SCRIPT_DIR:=${HOME}/ccr_rates/ccr_scripts/ccr_scripts

## MD traj parameters
TRAJECTORY_PATH=../../../tests_data/example_xtc_trj_ubq_NPT_bussi_box_8/
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=9
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=xtc
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d
#time pe frame (ns)
DT_NS=0.001

# specify all vectors that you need in all calculated CCRs
VECTOR_1=N-H
VECTOR_2=CA-HA|HA2|HA3
VECTOR_3=C-O
VECTOR_4=C-CA
VECTOR_5=H-HA|HA2|HA3
VECTORS=${VECTOR_1},${VECTOR_2},${VECTOR_3},${VECTOR_4},${VECTOR_5}
