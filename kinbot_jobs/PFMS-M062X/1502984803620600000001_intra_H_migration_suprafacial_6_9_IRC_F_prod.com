%mem=28GB
%chk=1502984803620600000001_intra_H_migration_suprafacial_6_9_IRC_F_prod
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(CalcAll,Cartesian,Cartesian)

Gaussian input prepared by ASE

0 1
C                 0.0871170000       -1.2560250000       -1.0276180000
F                 0.0410460000        1.2700310000       -1.4340140000
F                -0.2613570000       -1.4364520000       -2.2660370000
F                 1.3813620000       -1.1493610000       -0.9643130000
S                -0.4437500000        0.6216290000        2.0409020000
O                -0.6445430000       -1.2428840000       -0.1091440000
O                 0.9631170000        0.4274230000        2.0772830000
O                -0.9667580000        1.5283900000        1.0606180000
H                -0.3166860000        1.5688030000       -0.6273730000


