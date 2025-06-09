%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 2.0633120000       -0.1152230000       -0.6659530000
O                 2.1123050000       -0.6906090000       -1.6482150000
O                 2.0151960000        0.4600960000        0.3160630000


