include ../common.mk

## Model system parameters
N_RESIDUES:=76
VECTOR_1:=NH
VECTOR_2:=CA_HA
#shift parameter corresponds to the same residue SHIFT=0 (CAHA_NH) or the next SHIFT=1 (CAHA_Np1Hp1)
SHIFT=0

## Fit parameters
# Length of fit in DT_NS units, e.g. FIT_LIMIT=5000 and DT_NS=0.001 correspond to 5 ns
FIT_LIMIT=5000