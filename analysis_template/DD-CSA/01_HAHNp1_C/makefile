include ../../common.mk
include vars.mk

all: data/relaxation_rate/ccr*.csv

clean:
	rm -rf data


data/relaxation_rate/ccr*.csv: ${SCRIPT_DIR}/calc_dd_csa_c_rate.py data/fit/tau_2_exp.csv
	python3 "$<" \
	    --path-to-fit-dir=data/fit \
	    --nmr-freq="${NMR_FREQ}" \
	    --dipole="${DD_VECTOR}" \
	    --nmr-freq="${NMR_FREQ}" \
	    --output-directory=data/relaxation_rate \


data/fit/tau_2_exp.csv: ${SCRIPT_DIR}/fit.py data/crosscorr/*${(N_RESIDUES - 1)}*.csv
	python3 "$<" \
	    --path-to-crosscorr-csv=data/crosscorr/ \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --limit="${FIT_LIMIT}" \
	    --output-directory=data/fit/ \

data/crosscorr/*${(N_RESIDUES - 1)}*.csv: ${SCRIPT_DIR}/calc_correlation_func_dd_csa.py ../../vectors/CSA-C/z/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-metadata="../../vectors" \
	    --dipole="${DD_VECTOR}" \
		--path-to-csa-dir=../../vectors/CSA-C/ \
	    --output-directory=data/crosscorr/ \
	    --dt-ns="${DT_NS}" \
	    --shift-ind="${SHIFT}" \

../../vectors/CSA-C/z/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_csa_c_pas.py ../../vectors/C-O/${N_RESIDUES}*.csv
	python3 "$<" \
	    --path-to-CO-vectors=../../vectors/C-O \
	    --path-to-C-CA-vectors=../../vectors/C-CA \
	    --output-directory=../../vectors/CSA-C \


../../vectors/C-O/${N_RESIDUES}*.csv: ${SCRIPT_DIR}/extract_vectors.py
	python3 "$<" \
	    --path-to-trajectory="${TRAJECTORY_PATH}" \
	    --path-to-reference-pdb="${REFERENCE_PDB_PATH}" \
	    --filetype="${FILETYPE}" \
	    --pattern="${PATTERN}" \
	    --trajectory-length="${TRAJECTORY_LENGTH}" \
	    --vectors="${VECTORS}" \
	    --output-directory=../../vectors/ \
