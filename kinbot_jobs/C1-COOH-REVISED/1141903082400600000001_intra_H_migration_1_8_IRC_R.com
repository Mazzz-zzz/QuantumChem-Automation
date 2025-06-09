%mem=28GB
%chk=1141903082400600000001_intra_H_migration_1_8_IRC_R
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
C                 1.4833130000        0.2864600000        0.0152610000
O                 2.3383930000       -0.5417750000       -0.3785000000
C                -0.0218320000        0.0122970000        0.0131220000
F                -0.6266220000        0.7220160000        0.9501010000
F                -0.5137280000        0.3558990000       -1.1724450000
F                -0.2612190000       -1.2713360000        0.2208180000
O                 1.9898990000        1.3757610000        0.3741850000
H                 2.9314190000        0.5649520000       -0.0236290000


