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
C                 1.5691300000       -0.0045700000        0.0005070000
O                 2.1723180000       -1.0135110000        0.0027420000
O                 1.9922500000        1.2454970000       -0.0019190000
H                 2.9655130000        1.2576650000       -0.0016590000


