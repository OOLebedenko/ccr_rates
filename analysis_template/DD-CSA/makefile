include ../common.mk
include vars.mk

all: data/relaxation_rate/ccr*.csv

clean:
	rm -rf data


data/relaxation_rate/ccr*.csv: ${SCRIPT_DIR}/calc_dd_csa_c_rate.py data/fit/tau_2_exp.csv
	python3 "$<" \
	    --path-to-fit-dir=data/fit \
	    --nmr-freq="${NMR_FREQ}" \
	    --dipole="${VECTOR_1}" \
	    --nmr-freq="${NMR_FREQ}" \
	    --output-directory=data/relaxation_rate \


data/fit/tau_2_exp.csv: ${SCRIPT_DIR}/fit.py data/crosscorr/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-crosscorr-csv=data/crosscorr/ \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --limit="${FIT_LIMIT}" \
	    --output-directory=data/fit/ \

data/crosscorr/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/calc_ccr_func_dd_csa.py ../vectors/CSA_C/z/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-metadata-vect-1=../vectors/${DD_VECTOR}.csv \
	    --path-to-csa-dir=../vectors/CSA_C/ \
	    --output-directory=data/crosscorr/ \
	    --dt-ns="${DT_NS}" \
	    --shift-ind="${SHIFT}" \

../vectors/CSA_C/z/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_csa_c_pas.py ../vectors/C_O/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-CO-vectors=../vectors/C_O \
	    --path-to-C-CA-vectors=../vectors/C_CA \
	    --output-directory=../vectors/CSA_C \


../vectors/C_O/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_vectors.py
	mkdir -p ../vectors/${VECTOR_1}
	python3 "$<" \
	    --path-to-trajectory="${TRAJECTORY_PATH}" \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --filetype="${FILETYPE}" \
	    --pattern="${PATTERN}" \
	    --trajectory-length="${TRAJECTORY_LENGTH}" \
	    --vectors=C_O,C_CA,"${VECTOR_1}" \
	    --output-directory=../vectors/ \
