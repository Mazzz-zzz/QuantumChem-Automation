%mem=28GB
%chk=641041150370000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 1.1460330000        0.1355110000        0.7597880000
O                 0.7897740000       -0.9575060000        1.0064870000
F                 0.7832220000        1.1968450000        1.4880490000
O                 1.9426930000        0.5006500000       -0.2264110000
H                 2.0327470000        1.4601910000       -0.2461810000


