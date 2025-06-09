%mem=28GB
%chk=1502984803620600000001_intra_H_migration_5_9_IRC_F
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
C                -0.1197800000       -0.0356620000        0.1030030000
F                -0.6575940000        0.6949950000       -0.8534090000
F                -0.6339460000        0.3059960000        1.2680830000
F                -0.3485050000       -1.3132340000       -0.1293840000
S                 1.6999520000        0.2489510000        0.1452260000
O                 2.2212870000       -0.5542390000        1.1814500000
O                 2.1724300000        0.0840080000       -1.2667570000
O                 1.8808140000        1.7359620000        0.1600270000
H                 2.2558560000        1.3460570000       -1.0113640000


