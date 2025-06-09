%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_7_1_3_IRC_F_prod
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(CalcAll,Cartesian,Cartesian)

Gaussian input prepared by ASE

0 1
C                 2.1689570000       -2.1896730000        0.5341830000
O                 2.0338400000       -1.1176690000        0.2320590000
C                -0.7125440000        0.6857230000        0.0336980000
F                -0.5662920000        0.3574640000        1.3230310000
F                -1.7756300000        1.4577730000       -0.0823520000
F                -0.9463850000       -0.4570990000       -0.6233420000
O                 0.3527380000        1.3395300000       -0.4477280000
H                 1.1325140000        0.7788760000       -0.3583830000


