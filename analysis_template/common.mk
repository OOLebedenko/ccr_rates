SCRIPT_DIR:=${HOME}/Projects/cross_relaxation_pyxmolpp2_v2/ccr_rates/ccr_scripts

## MD traj parameters
TRAJECTORY_PATH=${HOME}/bionmr/olebedenko/bioinf/trj/ubq/tip4p-ew/NPT_bussi/bussi_box_8/5_run/
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=2
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=dat
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d
#time pe frame (ns)
DT_NS=0.001

# specify all vectors that you need in all calculated CCRs
VECTOR_1=N_H
VECTOR_2=CA_HA/HA2/HA3
VECTOR_3=C_O
VECTOR_4=C_CA
VECTOR_5=H_HA/HA2/HA3
VECTORS=${VECTOR_1},${VECTOR_2},${VECTOR_3},${VECTOR_4},${VECTOR_5}
