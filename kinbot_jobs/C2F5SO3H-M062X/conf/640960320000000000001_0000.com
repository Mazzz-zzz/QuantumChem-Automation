%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
S                 1.5956970000        1.0320060000       -1.2949500000
O                 2.1743090000        0.9421910000        0.0038010000
O                 1.4132860000        2.3199700000       -1.8758860000


