%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_8_7_1_IRC_R
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
C                 1.4788810000        0.3092940000       -0.0149990000
O                 2.2405650000       -0.0053700000       -0.9598000000
C                -0.0230910000        0.0184260000        0.0013250000
F                -0.6760850000        0.9954290000        0.6086580000
F                -0.4883950000       -0.1131320000       -1.2284540000
F                -0.2296670000       -1.1145340000        0.6638630000
O                 2.0842180000        0.8579420000        0.9362890000
H                 2.9332000000        0.5562170000       -0.0079670000


