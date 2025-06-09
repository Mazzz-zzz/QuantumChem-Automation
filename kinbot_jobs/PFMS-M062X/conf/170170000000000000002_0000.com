%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
O                 1.9125600000        1.6305650000        0.1031570000
H                 1.9600030000        2.0014580000       -0.7931210000


