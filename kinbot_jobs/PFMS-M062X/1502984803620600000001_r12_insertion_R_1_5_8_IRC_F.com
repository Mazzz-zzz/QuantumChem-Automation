%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_1_5_8_IRC_F
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
C                -0.1261290000       -0.1051690000        0.0401710000
F                -0.7139350000        0.3754910000       -1.0381740000
F                -0.5923960000        0.5085720000        1.1103930000
F                -0.3622330000       -1.4009450000        0.1336870000
S                 1.6989710000        0.1126850000       -0.0764950000
O                 2.2699510000       -0.2847650000        1.1588570000
O                 2.1312060000       -0.4426530000       -1.3073060000
O                 1.6389200000        1.6846470000       -0.1737440000
H                 2.5261570000        2.0649630000       -0.2505140000


