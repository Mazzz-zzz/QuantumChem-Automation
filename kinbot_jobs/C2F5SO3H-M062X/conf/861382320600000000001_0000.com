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
C                -1.9749350000        0.1559850000       -0.2994910000
O                -0.9391340000        0.9059540000        0.1092060000
F                -2.1343870000       -0.9373460000        0.4532140000
F                -3.1317750000        0.8244790000       -0.2516740000
F                -1.7578400000       -0.2194210000       -1.5447050000
H                -1.0869640000        1.1873400000        1.0184830000


