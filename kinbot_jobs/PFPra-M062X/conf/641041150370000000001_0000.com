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
C                 1.3420289718        0.0000000000        0.0000000000
O                 1.9790678848       -0.9842526103       -0.0000757674
F                 0.0000000000        0.0000000000        0.0000000000
O                 1.7976596158        1.2414531426        0.0000000000
H                 2.3378429760        1.4014630691        0.7819568043


