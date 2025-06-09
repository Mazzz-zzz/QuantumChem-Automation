%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_5_1_3_IRC_F
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
C                -0.1413620000       -0.6060600000       -0.2446270000
F                -0.9185710000       -0.4038640000       -1.2335170000
F                 0.0831800000        1.0681070000        0.4592740000
F                -0.7524330000       -1.2312390000        0.6810010000
S                 1.6355780000        0.2488400000       -0.0212950000
O                 2.0919220000       -0.7314050000        0.8980340000
O                 1.8499500000        0.3600650000       -1.4276880000
O                 2.3517810000        1.5445400000        0.5626910000
H                 2.2704700000        2.2638540000       -0.0769970000


