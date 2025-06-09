%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                -0.1022040000       -0.0603200000        0.0607360000
F                -0.5593700000        0.6201580000       -0.9631390000
F                -0.5336030000        0.4384830000        1.1944140000
F                -0.4002560000       -1.3333320000       -0.0429130000


