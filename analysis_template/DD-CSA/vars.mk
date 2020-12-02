

## Model system parameters
N_RESIDUES=76

# specify all vectors that you need in all calculated CCRs
VECTOR_1=N_H
VECTOR_2=CA_HA/HA2/HA3
VECTOR_3=C_O
VECTOR_4=C_CA
VECTOR_5=H_HA
VECTORS=${VECTOR_1},${VECTOR_2},${VECTOR_3},${VECTOR_4},${VECTOR_5}

# specify vector that takes part in particular DD-CSA-C CCR
DD_VECTOR_1=N_H
#other vectors -- C CSA axis

#shift parameter corresponds to the same residue SHIFT=0 (CAHA_C) or the next SHIFT=-1 (CAHA_Cm1)
SHIFT=0

## Fit parameters
#Length of fit in DT_NS units, e.g. FIT_LIMIT=5000 and DT_NS=0.001 correspond to 5 ns
FIT_LIMIT=5000

## CCR parameters:
NMR_FREQ=500e6

