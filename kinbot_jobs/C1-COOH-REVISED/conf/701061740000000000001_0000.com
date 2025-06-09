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
C                -0.9936050000        0.1675980000        0.5230580000
F                -2.3008580000        0.1343230000        0.7686070000
F                -0.8029410000        0.7530830000       -0.6564230000
F                -0.5489860000       -1.0841270000        0.4469240000
H                -0.4713000000        0.7112400000        1.3079720000


