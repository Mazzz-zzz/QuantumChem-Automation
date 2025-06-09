%mem=28GB
%chk=761281321000200000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 2.0679880000       -0.4707650000       -0.8902850000
O                 3.1655600000       -0.9466710000       -0.9014470000
C                 0.9028940000       -1.3218030000       -0.4287950000
F                 0.4535490000       -1.9377900000       -1.4742780000
O                 1.7500470000        0.7945620000       -1.1405800000
H                 2.5628790000        1.2845280000       -1.3348920000


