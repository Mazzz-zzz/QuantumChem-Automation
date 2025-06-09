%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_7_1_2_IRC_R
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
C                 1.4752060000       -0.0713420000        0.4342990000
O                 2.2950730000       -0.4542980000       -0.7069170000
C                -0.0052730000       -0.0558930000        0.0893610000
F                -0.6340860000        0.7732070000        0.9213110000
F                -0.2727510000        0.3524730000       -1.1560340000
F                -0.5069350000       -1.2770180000        0.2322890000
O                 2.0327840000        1.0927000000       -0.0816040000
H                 2.9356030000        1.1444490000        0.2662070000


