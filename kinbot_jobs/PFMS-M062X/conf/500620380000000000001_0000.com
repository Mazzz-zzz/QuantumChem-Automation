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
C                -1.7195760000       -1.3659810000        0.1223480000
F                -1.1449310000       -2.2366490000        0.8873480000
F                -2.6960920000       -0.9040040000        0.8340480000


