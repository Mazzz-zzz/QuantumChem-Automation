%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_6_5_7_IRC_F
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
C                -0.2505280000       -0.0620810000        0.1497370000
F                -1.0201490000        0.5552990000       -0.7436150000
F                -0.4427380000        0.5085840000        1.3264860000
F                -0.6190720000       -1.3352090000        0.2059440000
S                 1.6056880000        0.0350580000       -0.6035670000
O                 2.0357800000       -0.6053920000        0.7051480000
O                 3.1641910000       -0.1751050000       -0.6497170000
O                 1.5479620000        1.6216660000       -0.4006900000
H                 2.4493780000        1.9700160000       -0.3928560000


