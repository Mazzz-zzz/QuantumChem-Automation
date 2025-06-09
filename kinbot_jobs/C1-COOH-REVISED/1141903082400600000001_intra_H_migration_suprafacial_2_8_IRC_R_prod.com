%mem=28GB
%chk=1141903082400600000001_intra_H_migration_suprafacial_2_8_IRC_R_prod
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -0.2050530000        0.4572270000       -0.8610120000
O                -0.8362040000       -0.0436810000       -1.7345180000
C                 0.0796150000       -0.2842490000        0.4855830000
F                 1.2028810000       -0.9913250000        0.3681200000
F                 0.2111430000        0.5368230000        1.5192080000
F                -0.9142860000       -1.1216680000        0.7378160000
O                 0.3310180000        1.6626880000       -0.9837980000
H                 0.0907240000        1.9577850000       -1.8745010000


