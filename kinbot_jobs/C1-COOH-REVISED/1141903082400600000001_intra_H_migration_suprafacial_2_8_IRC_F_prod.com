%mem=28GB
%chk=1141903082400600000001_intra_H_migration_suprafacial_2_8_IRC_F_prod
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -0.1306450000        0.5639820000       -0.8106490000
O                -0.8362240000       -0.0108100000       -1.7739890000
C                 0.0792200000       -0.2848060000        0.4853060000
F                 1.2008720000       -0.9942340000        0.3668530000
F                 0.2101540000        0.5300180000        1.5206920000
F                -0.9188600000       -1.1228590000        0.7325110000
O                 0.3426950000        1.6465990000       -0.9365270000
H                -0.8371450000        0.6274630000       -2.5031070000


