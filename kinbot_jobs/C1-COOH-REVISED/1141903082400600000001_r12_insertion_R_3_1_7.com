%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_3_1_7
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.5729710000       -0.6587060000       -0.0204960000
O                 2.5967720000       -1.2326760000        0.0513260000
C                 0.0812440000        0.0920340000       -0.0254650000
F                -0.0998800000        0.8649750000        1.0102670000
F                -0.1361250000        0.6951690000       -1.1610880000
F                -0.7854230000       -0.8708110000        0.0825070000
O                 1.6626680000        1.1292920000       -0.2076300000
H                 2.4273930000        1.4849980000        0.2694910000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


