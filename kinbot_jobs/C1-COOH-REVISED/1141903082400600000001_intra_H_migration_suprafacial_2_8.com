%mem=28GB
%chk=1141903082400600000001_intra_H_migration_suprafacial_2_8
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.3847830000       -0.1225130000       -0.6415910000
O                 1.1526420000       -0.7200990000       -1.6427300000
C                 1.5984550000       -0.8721420000        0.6927120000
F                 2.5607160000       -1.7864400000        0.6044420000
F                 1.9551530000       -0.0652250000        1.6885540000
F                 0.5202340000       -1.5102250000        1.1057330000
O                 1.5365440000        1.1977330000       -0.5845950000
H                 1.0621230000        0.4505390000       -1.3949180000



