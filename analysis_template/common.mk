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
