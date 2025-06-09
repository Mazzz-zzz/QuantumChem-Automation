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
C                -2.9616310000       -0.8731530000        0.7390490000
F                -4.0751570000       -1.2347670000        1.2893450000
F                -2.9595700000       -1.4685510000       -0.4094140000


