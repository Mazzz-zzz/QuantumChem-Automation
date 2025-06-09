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
C                -1.2663080000        0.1185000000       -0.8539230000
F                -2.3876210000       -0.1711600000       -0.2775210000
F                -1.1438340000       -0.7677150000       -1.7883140000


