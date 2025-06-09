%mem=28GB
%chk=1502984803620600000001_intra_H_migration_suprafacial_6_9_IRC_R
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
geom(AllCheck,NoKeepConstants)
guess(Read)
irc(RCFC,reverse,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                 1.8381470000       -0.7706610000       -1.6151170000
F                 1.2007390000        0.6505510000       -2.1233390000
F                 0.7638880000       -1.5124770000       -1.7088390000
F                 2.6433620000       -1.0247890000       -2.6020590000
S                 1.3744230000        0.8596450000        0.4922790000
O                 2.3364310000       -0.5475680000       -0.4841250000
O                 0.3741260000        0.1579470000        1.2076630000
O                 2.4465660000        1.5153940000        1.1397700000
H                 1.0823800000        1.1365000000       -1.0083430000


