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
C                 1.5700970000       -0.0045800000       -0.0006790000
O                 2.1610480000       -1.0206700000        0.0107290000
O                 2.0082040000        1.2403160000        0.0001710000
H                 2.9814690000        1.2408180000        0.0124430000


