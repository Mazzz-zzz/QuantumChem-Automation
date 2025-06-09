%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_3_1_2_IRC_R
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
C                 1.5483420000        0.4512740000        0.4312170000
O                 1.5639120000       -0.1934130000       -0.6636770000
C                -0.0577680000       -0.1630610000       -0.1132480000
F                -0.8360770000        0.8068590000        0.3761980000
F                -0.5588510000       -0.3513850000       -1.3374000000
F                -0.1971290000       -1.2665730000        0.5719970000
O                 2.5987820000        1.1582690000        0.7258480000
H                 3.2584160000        1.0623040000        0.0079810000


