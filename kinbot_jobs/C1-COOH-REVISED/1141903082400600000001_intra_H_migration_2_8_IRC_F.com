%mem=28GB
%chk=1141903082400600000001_intra_H_migration_2_8_IRC_F
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
geom(AllCheck,NoKeepConstants)
guess(Read)
irc(RCFC,forward,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                 1.2946640000       -0.1932350000       -0.5188010000
O                 1.7453990000       -0.4692690000       -1.6556160000
C                 1.8629150000       -0.7561390000        0.7854790000
F                 2.5482780000       -1.8630010000        0.5604310000
F                 2.6717200000        0.1497240000        1.3240430000
F                 0.8851960000       -1.0185010000        1.6375030000
O                 0.3443740000        0.6240570000       -0.5571290000
H                 0.7650920000        0.3831950000       -1.7691280000


