%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_4_3_1_7_IRC_R_prod
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(CalcAll,Cartesian,Cartesian)

Gaussian input prepared by ASE

0 1
C                 2.8719620000        0.9852410000        0.4973090000
O                 1.8354520000        1.3704920000        0.2991350000
C                -1.0160680000       -0.3471350000       -0.0260970000
F                -1.0316930000       -0.0598120000        1.2831500000
F                -2.1149200000       -1.0188840000       -0.3221040000
F                 0.0381440000       -1.1509160000       -0.2256200000
O                -0.9635970000        0.7544640000       -0.7875260000
H                -0.1709480000        1.2564100000       -0.5600290000


