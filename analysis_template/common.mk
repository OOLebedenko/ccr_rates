SCRIPT_DIR:=${HOME}/ccr_rates/ccr_scripts

## MD traj parameters
TRAJECTORY_PATH=../../example_xtc_trj_ubq_NPT_bussi_box_8/
REFERENCE_PDB_PATH:=${TRAJECTORY_PATH}/run00001.pdb
TRAJECTORY_LENGTH:=9
# type of MD run files "dat" - TrjtoolDatFile; "nc" - AmberNetCDF, "xtc" - GromacsXtcFile
FILETYPE:=xtc
# pattern of MD run files: run00001.dat ---> "run%05d".dat
PATTERN:=run%05d
#time pe frame (ns)
DT_NS=0.001
