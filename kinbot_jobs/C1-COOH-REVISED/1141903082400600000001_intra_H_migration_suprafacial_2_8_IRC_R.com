%mem=28GB
%chk=1141903082400600000001_intra_H_migration_suprafacial_2_8_IRC_R
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
C                 1.3667090000       -0.1288470000       -0.5034340000
O                 0.7159210000       -0.5823170000       -1.4744650000
C                 1.6095410000       -0.9080740000        0.7906200000
F                 2.7306950000       -1.6090860000        0.6591520000
F                 1.7382260000       -0.0817810000        1.8145820000
F                 0.6097020000       -1.7393980000        1.0289330000
O                 1.8304310000        1.0157590000       -0.7201890000
H                 1.1694250000        0.6053710000       -1.7675930000


