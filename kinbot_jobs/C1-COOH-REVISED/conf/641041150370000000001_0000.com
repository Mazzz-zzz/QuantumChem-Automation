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
C                 1.3417410625        0.0000000000        0.0000000000
O                 1.9786574829       -0.9843257859       -0.0000203473
F                 0.0000000000        0.0000000000        0.0000000000
O                 1.7974300847        1.2413404665        0.0000000000
H                 2.3366134285        1.4017597279        0.7825190136


