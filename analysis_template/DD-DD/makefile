include common.mk

all: data/relaxation_rate/ccr*.csv

clean:
	rm -rf data

data/relaxation_rate/ccr*.csv: ${SCRIPT_DIR}/calc_dd_dd_rate.py data/fit/*.csv
	python3 "$<" \
	    --path-to-fit-dir=data/fit \
	    --dipole-1="${VECTOR_1}" \
	    --dipole-2="${VECTOR_2}" \
	    --output-directory=data/relaxation_rate \

data/fit/*.csv: ${SCRIPT_DIR}/fit_vectors.py data/crosscorr/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-crosscorr-csv=data/crosscorr \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --limit="${FIT_LIMIT}" \
	    --output-directory=data/fit \


data/crosscorr/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/calc_ccr_func.py data/vectors/${VECTOR_2}/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-vect-csv-1=data/vectors/"${VECTOR_1}" \
	    --path-to-vect-csv-2=data/vectors/"${VECTOR_2}" \
	    --output-directory=data/crosscorr \


data/vectors/${VECTOR_2}/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_vectors.py
	mkdir -p data/vectors/${VECTORS}
	python3 "$<" \
	    --path-to-trajectory="${TRAJECTORY_PATH}" \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --filetype="${FILETYPE}" \
	    --pattern="${PATTERN}" \
	    --trajectory-length="${TRAJECTORY_LENGTH}" \
	    --vectors="${VECTORS}" \
	    --output-directory=data/vectors/ \

