%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_3_4_IRC_R_prod
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 0.9954870000        0.0029750000        0.0675170000
O                 1.6486510000       -0.8524200000        0.6920840000
C                -0.5350560000       -0.0376030000       -0.0123270000
F                -1.0695560000        0.0263320000        1.2800380000
F                -1.0798160000        0.9997580000       -0.7592280000
F                -0.9384000000       -1.2488250000       -0.5867500000
O                 1.5160030000        1.0746330000       -0.6200710000
H                 2.4996070000        1.0843930000       -0.5570040000


