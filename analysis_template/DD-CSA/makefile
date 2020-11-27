include ../common.mk
include vars.mk

all: data/relaxation_rate/ccr*.csv

clean:
	rm -rf data


data/relaxation_rate/ccr*.csv: ${SCRIPT_DIR}/calc_dd_csa_c_rate.py data/fit/z/*.csv
	python3 "$<" \
	    --path-to-fit-dir=data/fit \
	    --nmr-freq="${NMR_FREQ}" \
	    --dipole="${VECTOR_1}" \
	    --nmr-freq="${NMR_FREQ}" \
	    --output-directory=data/relaxation_rate \


data/fit/z/*.csv: ${SCRIPT_DIR}/fit_ccr_dd_csa.py data/crosscorr/z/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-crosscorr-csv=data/crosscorr/ \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --limit="${FIT_LIMIT}" \
	    --output-directory=data/fit/ \

data/crosscorr/z/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/calc_ccr_func_dd_csa.py ../vectors/CSA_C/z/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-vect-csv-1=../vectors/"${VECTOR_1}" \
	    --path-to-vect-csv-2=../vectors/CSA_C/ \
	    --output-directory=data/crosscorr/ \
	    --dt-ns="${DT_NS}" \
	    --shift-ind="${SHIFT}" \

../vectors/CSA_C/z/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_csa_c_pas.py ../vectors/${VECTOR_1}/${N_RESIDUES}*.csv ../vectors/CO/${N_RESIDUES}*.csv ../vectors/C_CA/${N_RESIDUES}*.csv:
	python3 "$<" \
	    --path-to-CO-vectors=../vectors/CO \
	    --path-to-C-CA-vectors=../vectors/C_CA \
	    --output-directory=../vectors/CSA_C \


../vectors/${VECTOR_1}/${N_RESIDUES}*.csv ../vectors/CO/${N_RESIDUES}*.csv ../vectors/C_CA/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_vectors.py
	mkdir -p ../vectors/${VECTOR_1}
	python3 "$<" \
	    --path-to-trajectory="${TRAJECTORY_PATH}" \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --filetype="${FILETYPE}" \
	    --pattern="${PATTERN}" \
	    --trajectory-length="${TRAJECTORY_LENGTH}" \
	    --vectors=CO,C_CA,"${VECTOR_1}" \
	    --output-directory=../vectors/ \
