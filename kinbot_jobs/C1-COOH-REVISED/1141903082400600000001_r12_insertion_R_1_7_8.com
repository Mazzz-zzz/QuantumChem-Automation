%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_1_7_8
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.5329720000       -0.3139650000        0.1860670000
O                 2.3601500000       -1.0798540000        0.3781410000
C                 0.0789490000       -0.0376730000       -0.0166770000
F                -0.4722640000        0.5918020000        1.0309490000
F                -0.1567420000        0.7313570000       -1.0881190000
F                -0.6370460000       -1.1406750000       -0.1972350000
O                 2.4161020000        1.6988710000        0.2786250000
H                 2.1975050000        1.0544130000       -0.5728390000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


