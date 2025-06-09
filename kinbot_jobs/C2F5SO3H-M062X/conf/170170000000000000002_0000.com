%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
O                 2.2354210000        1.4677200000       -0.0876630000
H                 2.3460520000        1.5776900000       -1.0462340000


