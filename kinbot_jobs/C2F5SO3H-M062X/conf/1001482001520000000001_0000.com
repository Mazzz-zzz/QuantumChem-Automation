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
C                 0.9221500000       -1.8613450000       -0.5906450000
C                 1.6533130000       -0.7706280000       -0.6826240000
F                 1.6603340000        0.1722030000        0.2286280000
F                 2.4479350000       -0.5179000000       -1.6945550000
F                 0.9151250000       -2.8041600000       -1.5018970000
F                 0.1275320000       -2.1140950000        0.4212830000


